import sys
import os
import ast
import json
# from tqdm import tqdm

# This is a function class map we use to confirm our data
functionClassMap = []
functionDefinitions = []
variableMap = []

# Parser function from https://stackoverflow.com/questions/72064609/how-can-i-retrieve-function-names-and-attributes-from-python-code-with-ast 
# for getting function calls, 

def parse(d, c):
  def parse_chain(d, c, p=[]):
     if isinstance(d, ast.Name):
        return [d.id]+p
     if isinstance(d, ast.Call):
        for i in d.args:
           parse(i, c)
        return parse_chain(d.func, c, p)
     if isinstance(d, ast.Attribute):
        return parse_chain(d.value, c, [d.attr]+p)
  if isinstance(d, (ast.Call, ast.Attribute)):
     c.append('.'.join(parse_chain(d, c)))
  else:
     for i in getattr(d, '_fields', []):
       if isinstance(t:=getattr(d, i), list):
          for i in t:
             parse(i, c)
       else:
          parse(t, c)

def parseVariables(d, ret):
    root = ast.parse(d)
    ret += sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)})


def functionGrab(className ,functionAst):
    functionName = functionAst.name
    # Add to function definitions map
    functionDefinitions.append(functionName)
    # Grab the parameters
    functionArgs = []
    for arg in functionAst.args.args:
        functionArgs.append(arg.arg)
    callsArr = []
    
    parse(functionAst, callsArr)
    parseVariables(functionAst, variableMap)
    # Raw List of functions calls checked against our defined functions module
    finalFuncs = []
    for function in callsArr:
        for definition in functionDefinitions:
            if definition in function:
                if definition not in finalFuncs:
                    finalFuncs.append(definition)
    # Creates our object
    functionObj = {
        "className": className,
        "functionName": functionName,
        "args": functionArgs,
        "functionCalls": finalFuncs
    }
    # Appends to the map
    functionClassMap.append(functionObj)

def classGrab(classAst):
    iterateClass(classAst)

def iterateClass(classAst):
    className = classAst.name
    for x in classAst.body:
        match x.__class__:
            case ast.FunctionDef:
                functionGrab(className, x)
            case ast.ClassDef:
                classGrab(x)

def readRepo(repo):
    # Open the module with the trace function and retrieve its AST
    directoryArr = os.listdir(repo)
    # pbar = tqdm(directoryArr)
    # pbar.set_description("processing static files")

    for fileName in directoryArr:
        try:
            file = repo+fileName
            tracerFile = open(file,'r').read()
            tracerTree = ast.parse(tracerFile)
            for x in tracerTree.body:
                match x.__class__:
                    case ast.FunctionDef:
                        functionGrab(fileName,x)
                    case ast.ClassDef:
                        classGrab(x)
        except:
            pass
    # print(functionClassMap)
    # print(functionDefinitions)
    # print(variableMap)

def createForceGraphStructure(): 
    nodes = []
    links = []
    # A map where key is function id, and value is number of times it is called
    countMap = {}

    for function in functionClassMap:
        nodeObj = {
        "id": function.get("className")+"."+function.get("functionName")+"("+', '.join(function.get("args"))+")",
        "name": function.get("functionName"),
        "params": ', '.join(function.get("args")),
        "class": function.get("className"),
        "calls": 0
        }
        nodes.append(nodeObj)

    for function in functionClassMap:
        for functionCall in function.get("functionCalls"):
            for node in nodes:
                if functionCall in node.get("name"):
                    linkObj = {
                        "source": function.get("className")+"."+function.get("functionName")+"("+', '.join(function.get("args"))+")",
                        "target": node.get("id")
                    }
                    links.append(linkObj)
                    target = linkObj["target"]
                    if countMap.get(target) != None:
                        countMap[target] = countMap[target] + 1
                    else:
                        countMap[target] = 1
    # Afterwards, iterate through the countMap keys and update call values in the graph
    for key in countMap.keys():
        for node in nodes:
            if node["id"] == key:
                node["calls"] = countMap.get(key)
                break
    
    staticGraph = {
        "nodes": nodes,
        "links": links
    }
    return staticGraph

def execute(repo):
    readRepo(repo)
    ret = createForceGraphStructure()
    # print(ret)
    jsonOutput = json.dumps(ret, indent=4)
    with open('../frontend/src/data/static.json', 'w+') as outfile:
        outfile.write(jsonOutput)

            
# def main():
#     args = sys.argv[1:]
#     readRepo(sys.argv[1])
#     ret = createForceGraphStructure()
#     print(ret)
#     jsonOutput = json.dumps(ret, indent=4)
#     with open('../frontend/src/data/tempStatic.json', 'w+') as outfile:
#         outfile.write(jsonOutput)
