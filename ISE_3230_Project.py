#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 12:10:29 2020

CVXPY code for the LP production schedule example.

@author: Sam
"""

import pandas as pan

import cvxpy as cp

players = pan.read_excel("C:/Users/ryand/Downloads/ISE_Fantasy.xls") # file location

x = cp.Variable(200, boolean = True)

points = 0

for i in players.index:
    points += x[i]*players['DK points'][i]

obj_func = points

cost = 0

for i in players.index:
    cost += x[i]*players['DK salary'][i]

constraints = []
constraints.append(sum(x[0:23]) == 1) # Defenses
constraints.append(sum(x[23:51]) == 1) # Quarterbacks
constraints.append(sum(x[51:93]) <= 3) # Runningbacks
constraints.append(sum(x[93:132]) <= 2) # Tightends
constraints.append(sum(x[132:200]) <= 4) # Widereceivers
constraints.append(sum(x[51:200]) == 7) # Accounts for Flex
constraints.append(cost <= 50000) # Salary


problem = cp.Problem(cp.Maximize(obj_func), constraints)
#problem.solve(solver=cp.CVXOPT,verbose = True)
#problem.solve(verbose = True)
problem.solve(solver=cp.GUROBI,verbose = True)

for i in players.index:
    if x.value[i] == 1:
        print(players.iloc()[i])
        

print("Total cost")
print(cost.value)
print("Total points")
print(points.value)


