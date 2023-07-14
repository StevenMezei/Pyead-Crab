# Milestone 1 #

## Discussion with TA:
UML with just static checking might not be enough

We need to think of other use cases or user story requirements to augment our project idea

A suggestion from TA is to add interactivity to the UML diagram; when clicking on a method, show the flow of data and control in a tree like visualization. Ex. Which functions classes or modules get executed for a given input

We can have visualization (UML DIAGRAM) with static checking, and also reason about dynamic properties (the tree like visualization described above)

## Things to do by next milestone
Brainstorm more use cases and settle on an idea

# Milestone 2 #

Based on feedback and suggestions from our TA, we have decided not to move forward with the UML diagram and instead will be doing a program analysis of function calls.

## Use case ##
Aimed at developers who are trying to debug a program with little to advanced knowledge of it. We will create a call graph which can help determine the importance of each function and where it's called. For example, if we change one function, we can look at the graph to see what functions are called by it and see if they need to be changed as well.

## Brief description of the project ##
After getting the AST, we can make a call graph for functions potentially calling each other (we can generate a call graph statically) ; when we run the code we can record the calls sequences, and those can be considered random walks on the graph. From this information, we can determine which functions are important, as well as the edges (we can also assess the importance of call sites; the edges represent function calls). After processing we can do graph embedding to provide a sufficient visualization.


## Planned division of responsibliities ##
### Frontend ###
Alex <br>
Len <br>

### Backend ###
Lian <br>
Steven <br>
Nathan

## Tentative Roadmap ##
Milestone 3: Bootstrapping and Setup (TBD) <br>
Milestone 4: Functional mockup and first prototype study (TBD) <br>
Milestone 5: Close to full completion of the project and perform user study (TBD) <br>
November 29: Complete project. (TBD)
