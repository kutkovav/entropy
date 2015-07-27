#Finding Optimal Compatible Set of Software Components Using Integer Linear Programming

This experiment verifies performance of the integer linear programming model used
 for selecting the optimal set of component satisfying given requirements.
 
##Simulation Scenarios
Since the goal of the simulation was to provide data on the performance of the method,
 real interoperability of concrete library versions was not tested. Two variants of the
 simulation were performed to cover (1) cases in which there are multiple possible solutions 
 and (2) the cases in which there is only a limited number of possible solutions in the 
 searched space. In the first case all the versions of a particular library were considered 
 as feasible (interoperable) solution, whereas in the second case the conditions had been set
 so that only a single version was feasible.

The simulation was run for each subset of the dependency list -- i.e. the goal was to find 
a solution for each library on its own, for each pair and for all three at once. This design 
was used to show the difference between scenarios in which a single library can provide all 
the required functionality and those in which a set of libraries must be used to satisfy all 
requirements.

To test behaviour when working with larger data sets, the simulation was run multiple times 
with 1, 10, 100 and 1000 magnifier arguments applied to both the number of available 
library versions and their reference count.
 
###Source Data
The experiment is based on number of associations between *lucene* search engine and
the libraries *ant*, *ant-junit* and *junit*. The [input data](data/) are provided in form of 
a properties file per library. Its structure is:

```
[versions]
version_name=binary_size_in_kB
.
.
.
[refs]
lucene=nb_of_unique_associations
```

##Results
[Results](results/) files have the following structure:
 
```
args=[list of all library combinations that were searched for]
magnifiers=[list of all magnifier values used]
split=[true|false] //if true, simulation data were generated so that there was only a single feasible solution in the data set

//list of results for each scenario run follows
(arg)-magnifier: <mean_value> <std_deviation> <split_value>
.
.
.
```

##Source Code
The [simulation code](code/) is written in Python 2.7 using [Gurobi](www.gurobi.com) solver and its python binding.
The code is split into three modules:
* data - handles reading the source data files and generating data from them
* stats - convenience utility class for statistics
* run.py - contains the experimental model as well as the code responsible for running or requested simulation scenarios