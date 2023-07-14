# Code taken and adapted from https://www.geeksforgeeks.org/python-sys-settrace/
from functools import lru_cache
from sys import setprofile
from os import path
import inspect
from pathlib import Path
import copy
import random

callTrace = []
classFunctionMap = None

def tracer(frame, event, arg = None):

    global callTrace

    if event == 'call':

        code = frame.f_code
        #Try to get name of calling function from the outer frame
        outerFrame = None
        caller = None
        callerClass = None
        try:
            outerFrame = frame.f_back
            caller = outerFrame.f_code.co_name
            # Construct caller function name with arguments included
            posArgs = inspect.getargvalues(outerFrame).args
            varArgs = inspect.getargvalues(outerFrame).varargs
            keywordArgs = inspect.getargvalues(outerFrame).keywords
            caller = constructFuncName(caller, posArgs, varArgs, keywordArgs)
            # Get caller function class if it exists from the outer frame
            callerClass = outerFrame.f_locals['self'].__class__.__name__
        except KeyError:
            # If we get a key error, that means the function does not belong to a class, but a module
            outerFrame = frame.f_back
            caller = outerFrame.f_code.co_name
            posArgs = inspect.getargvalues(outerFrame).args
            varArgs = inspect.getargvalues(outerFrame).varargs
            keywordArgs = inspect.getargvalues(outerFrame).keywords
            caller = constructFuncName(caller, posArgs, varArgs, keywordArgs)
            callerClass = outerFrame.f_code.co_filename
            callerClass = Path(callerClass).name
        except:
            # Any other error means that the outer frame does not exist
            pass

        # Get name of callee function from current frame
        callee = code.co_name
        # Construct callee function name with arguments included
        posArgs = inspect.getargvalues(frame).args
        varArgs = inspect.getargvalues(frame).varargs
        keywordArgs = inspect.getargvalues(frame).keywords
        callee = constructFuncName(callee, posArgs, varArgs, keywordArgs)
        calleeClass = None
        # Get caller function class or module from the current frame
        try:
            calleeClass = frame.f_locals['self'].__class__.__name__
        except:
            calleeClass = code.co_filename
            calleeClass = Path(calleeClass).name


        callTraceDict = {
            "callee": callee,
            "calleeClass": calleeClass,
            "caller": caller,
            "callerClass": callerClass
        }
        
        res = isUserDefined(callTraceDict)
        if res != None:
            callTrace.append(res)
        

def constructFuncName(funcName, posArgs = [], varArgs = None, keywordArgs = None):
    if funcName == "<module>":
        return funcName
    
    constructFunc = funcName + "("

    # If function has *args, add * in front of it
    if varArgs is not None:
        varArgs = "*" + varArgs
    # If function has **args, add ** in front of it
    if keywordArgs is not None:
        keywordArgs = "**" + keywordArgs
    
    # If function has positional arguments, add them first to parameters string
    if len(posArgs) > 0:
        for i in range(len(posArgs)):
            if i == 0:
                constructFunc = constructFunc + posArgs[i]
            else:
                constructFunc = constructFunc + "," + posArgs[i]
    
    # If function has both positional arguments and *args, then add "," when adding *args to parameters string
    if varArgs is not None and len(posArgs) > 0:
        constructFunc = constructFunc + "," + varArgs
    # Else if function only has *args, add them without "," to parameters string
    elif varArgs is not None:
        constructFunc = constructFunc + varArgs
    
    # If function has positional arguments or *args, and **args, then add "," when adding **args to parameters string
    if keywordArgs is not None and (varArgs is not None or len(posArgs) > 0):
        constructFunc = constructFunc + "," + keywordArgs
    # Else if function only has **args, add them without "," to parameters string
    elif keywordArgs is not None:
        constructFunc = constructFunc +  keywordArgs

    return constructFunc + ")"

# Returns a dictionary if user defined functions are involved, returns None otherwise
def isUserDefined(traceObj):
    traceCopy = traceObj.copy()
    callee = traceCopy["callee"]
    calleeClass = traceCopy["calleeClass"]
    caller = traceCopy["caller"]
    callerClass  = traceCopy["callerClass"]

    # If callerClass is <string> then it is possible that the entry point script is calling a function
    if callerClass == "<string>":
        # Check if the function being called is a user defined function
        if caller == "<module>":
            # If caller is <module> then we know for sure that it is the entry point script calling a function
            # Check if the callee function is a user defined one
            userDefinedClass1 = findClassOfFunction(callee)
            # If the class of the callee is user defined, set it and return the object
            if userDefinedClass1 != None:
                if calleeClass[0] != "<":
                    return traceCopy
                else:
                    traceCopy["calleeClass"] = userDefinedClass1
                    return traceCopy
            else:
                return None
        else:
            # If caller is not <module>, check if it is user defined. If not user defined, then we discard it
            userDefinedClass2 = findClassOfFunction(caller)
            if userDefinedClass2 != None:
                # If caller is user defined, set the caller class and check callee
                traceCopy["callerClass"] = userDefinedClass2
                userDefinedClass3 = findClassOfFunction(callee)
                if userDefinedClass3 != None:
                    if calleeClass[0] != "<":
                        return traceCopy
                    else:
                        traceCopy["calleeClass"] = userDefinedClass3
                        return traceCopy
                else:
                    return None
            else:
                return None
    else:
        # If we are here that means that callerClass is an actual class or module, so we have to check if it is user defined
        validClass1 = searchClassFunctionMap(callerClass)
        if validClass1 != None:
            if caller == "<module>":
                # Check if the callee function is a user defined one
                userDefinedClass4 = findClassOfFunction(callee)
                # If the class of the callee is user defined, set it and return the object
                if userDefinedClass4 != None:
                    if calleeClass[0] != "<":
                        return traceCopy
                    else:
                        traceCopy["calleeClass"] = userDefinedClass4
                        return traceCopy
                else:
                    return None
            else:
                # Check if caller function is user defined
                userDefinedClass5 = findClassOfFunction(caller)
                if userDefinedClass5 != None:
                    # Check if callee function is user defined
                    userDefinedClass6 = findClassOfFunction(callee)
                    if userDefinedClass6 != None:
                        if calleeClass[0] != "<":
                            return traceCopy
                        else:
                            traceCopy["calleeClass"] = userDefinedClass6
                            return traceCopy
                    else:
                        return None
                else:
                    return None
        else:
            return None

@lru_cache(None)
def findClassAndFunction(className,functionName):
    for classFunc in classFunctionMap:
        funcName = functionName[0:functionName.find("(")]
        args = functionName[functionName.find("(")+1:functionName.rfind(")")]
        args = args.split(",")
        if (args == ['']):
            args = []
        if classFunc["class"] == className and classFunc["functionName"] == funcName and args == classFunc["args"]:
            return True
    return False

def fillInEntry(entryModule):
    global callTrace
    for traceObj in callTrace:
        if traceObj["caller"] == "<module>" and traceObj["callerClass"] == "<string>":
            
            traceObj["callerClass"] = entryModule
            
@lru_cache(None)
def searchClassFunctionMap(className):
    if className in classSet:
        return className
    return None

@lru_cache(None)
def findClassOfFunction(function):
    valClasses = classFunctionMap.get(function)
    if valClasses != None:
        if len(valClasses) == 1:
            return valClasses[0]
        else:
            # Randomly guess otherwise. valClasses will never be empty
            arrLen = len(valClasses)
            randomGuess = random.randint(0,arrLen-1)
            return valClasses[randomGuess]
    else:
        return None



        
def setGlobals(map, set):
    
    global classFunctionMap

    global classSet

    classFunctionMap = map
    classSet = set

def start():
    setprofile(tracer)
