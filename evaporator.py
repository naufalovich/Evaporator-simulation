"""
Created on Sun May 30 20:54:10 2021
@author: Naufal Hadi
"""
# This python file are compute material and energy balance on 
# triple effect evaporator

# import necessary modules
import numpy as np
import scipy.linalg

# define feed and product condition
F = 10000 # feed flow, kg/h
xf = 0.28 # feed concentration, mass fraction
xp = 0.88 # product concentration, mass fraction

# define steam properties
P = 3.5 # steam pressure, bar
Ts = 133 # steam temperature, deg celsius

# temperature of feed and each effect
T = np.array([75, 123, 113, 103]) # deg celcius

# define enthalpy of saturated vapor and saturated liquid from steam tables
# enthalpy of saturated vapor at 133, 123, 113, 98, and 50 deg C
Hv = np.array([2731.63, 2705.9, 2695.77, 2672.8]) # kJ/kg

# enthalpy of saturated liquid at 133, 123, 113, 98, and 50 deg C
Hl = np.array ([559.93, 516.41, 475.2, 410.44]) # kJ/kg

# specific heat (respectively to F, F1, F2, F3, and P)
cp = np.array([3.70, 3.39, 2.82, 2.64]) #kJ/kg C

# overall heat transfer coefficient each effect
U = np.array([1230, 895, 895]) # W/(m2 C)
#---------This is computation section---------------------
# solving material balance for glycerine and water
P = F*xf/xp # final product flow, kg/h
V = F-P # overall vapor flow, kg/h

# calculate enthalpy of feed and intermediate product
Tref = np.ones(4)*25 #set reference temperature, deg C
H = cp*(T-Tref)

# calculate heat duty on heat exchanger region
qs = U[0]* (Ts - T[1])
q1 = U[1]* (T[1] - T[2])
q2 = U[2]* (T[2] - T[3])
q = np.array([qs, q1, q2])

# calculate latent heat of vaporization of steam (Hv - Hl) for heat exchanger
lamda = Hv - Hl # kJ/kg

# construct the matrix
eq1 = np.array([0, 1, 1, 1, 0, 0])
eq2 = np.array([lamda[0]*q[1], lamda[1]*q[0]*(-1), 0, 0, 0, 0])
eq3 = np.array([0, lamda[1]*q[2], lamda[2]*q[1]*(-1), 0, 0, 0])
eq4 = np.array([lamda[0]*(-1), Hv[1], 0, 0, H[1], 0])
eq5 = np.array([0, lamda[1], Hv[2]*(-1), 0, H[1], H[2]*(-1)])
eq6 = np.array([0, 0, lamda[2], Hv[3]*(-1), 0, H[2]])

#now make it matrix form
A = np.array([eq1, eq2, eq3, eq4, eq5, eq6])
B = np.array([V, 0, 0, F*H[0], 0, P*H[3]])

# start computing
C = flows =scipy.linalg.solve(A,B) # solver for linear algebra

# store all solution
S, V1, V2, V3, F1, F2 = C[0], C[1], C[2], C[3], C[4], C[5]

# calculate other parameters
x1 = F*xf/F1 # concentration in 1st effect, mass fraction
x2 = F1*x1/F2 # concentration in 2nd effect, mass fraction
Se = (V1 + V2 + V3)/S # steam economy
C = S + V1 + V2

# print all solutions
print("Simulation Report :")
print("----------------------------------------------------------------")
print("Steam consumption, S                  :" , S, "kg/h")
print("Vapor flow in 1st effect, V1          :" , V1, "kg/h")
print("Vapor flow in 2nd effect, V2          :" , V2, "kg/h")
print("Vapor flow in 3rd effect, V3          :" , V3, "kg/h")
print("Total water removed, V                :" , V, "kg/h")
print("Intermediate flow in 1st effect, F1   :" , F1, "kg/h")
print("Intermediate flow in 2nd effect, F    :" , F2, "kg/h")
print("Final product flow, P                 :" , P, "kg/h")
print("Total condensate recovery, C          :" , C, "kg/h")
print("Concentration leaving 1st effect, x1  :" , x1)
print("Concentration leaving 2nd effect, x2  :" , x2)
print("Steam economy                         :" , Se, "kg water/ kg steam")