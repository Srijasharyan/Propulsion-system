# -*- coding: utf-8 -*-
"""Rocket propulsion

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jkMDqh5apQN1E4fGRQgl998CaFdJTUYl
"""

# importing libraries
import numpy as np
import sympy as smp
import scipy as sp
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math

# considering one stage rocket
Mu=3 # typical mass of payload(in %)
Ms=17 #typical mass of structure(in %)
Mp=80 #typical mass of propellent(in %)
Mi=Mu+Ms+Mp # initial mass of rocket
g = 9.81 # gravity assumed to be constant
vg = 500 # fuel emitted at 800m/s
b = [0,0.2] # friction coefficient b[0] implies zero, b[1]=1
t, n = smp.symbols('t n')
f =Mp* pow(math.exp(1),-1*n*t) # assume 'f' (fuel) as a exponential function of a time and some factor
dfdt = smp.diff(f, t).simplify() #fuel loss rate
f = smp.lambdify([t, n], f)
dfdt = smp.lambdify([t, n], dfdt)

t = np.linspace(1e-4, 10, 1500)
f1 = f(t, 0.3)
f2 = f(t, 1)
f3 = f(t, 2)
plt.figure(figsize=(10,8))
plt.plot(t, f1, label='e^-0.3')
plt.plot(t, f2, label='e^-0.4')
plt.plot(t, f3, label='e^-1')
plt.ylabel('$M_p(t)$')
plt.xlabel('$t$')
plt.title('Fuel depletion vs time')
plt.legend()
plt.show() # plot showing fuel depletion as function of time

#CASE_III
def dSdt(t,S,vg,Mu,Ms,n): 
    x, v = S[0], S[1]
    dxdt= v
    dvdt = -g- b[1]/(Mu+Ms+f(t,n))*v**2  - vg/(Mu+Ms+f(t,n))*dfdt(t,n)
    if (dvdt<0)*(dxdt<0)*(x<=0):
        dxdt=0
        dvdt=0
    return [dxdt,dvdt]

#case_II
def dS2dt(t,S,vg,Mu,Ms,n):
    x, v = S[0], S[1]
    dxdt= v
    dvdt = -g- vg/(Mu+Ms+f(t,n))*dfdt(t,n)
    return [dxdt,dvdt]

#CASE_I
def dS3dt(t,S,vg,Mu,Ms,n):
    x, v = S[0], S[1]
    dxdt= v
    dvdt =  - vg/(Mu+Ms+f(t,n))*dfdt(t,n)
    return [dxdt,dvdt]

#case_I
n1, n2, n3= 0.3,1,2
sol1 = solve_ivp(dS3dt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000), args=(vg,Mu,Ms,n1))
sol2 = solve_ivp(dS3dt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000),  args=(vg,Mu,Ms,n2))
sol3 = solve_ivp(dS3dt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000),  args=(vg,Mu,Ms,n3))

fig, axes = plt.subplots(1, 2, figsize=(10,3))
ax = axes[0]
ax.plot(sol1.t, sol1.y[0], label='n={}'.format(n1))
ax.plot(sol2.t, sol2.y[0], label='n={}'.format(n2))
ax.plot(sol3.t, sol3.y[0], label='n={}'.format(n3))
ax.axvline(1, ls='--', color='k')
ax.set_ylabel('$x(t)$')
ax.set_title('Position')
ax.legend()
ax = axes[1]
ax.plot(sol1.t, sol1.y[1], label='n=1')
ax.plot(sol2.t, sol2.y[1], label='n=0.7')
ax.plot(sol3.t, sol3.y[1], label='n=1.3')
ax.axvline(1, ls='--', color='k')
ax.set_ylabel('$v(t)$')
ax.set_title('Velocity')
fig.text(0.5, -0.04, '$t$', ha='center', fontsize=20)
fig.tight_layout()

#Case_II
n1, n2, n3 = 0.3,1,2
sol1 = solve_ivp(dS2dt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000), args=(vg,Mu,Ms,n1))
sol2 = solve_ivp(dS2dt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000),  args=(vg,Mu,Ms,n2))
sol3 = solve_ivp(dS2dt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000),  args=(vg,Mu,Ms,n3))

fig, axes = plt.subplots(1, 2, figsize=(10,3))
ax = axes[0]
ax.plot(sol1.t, sol1.y[0], label='n={}'.format(n1))
ax.plot(sol2.t, sol2.y[0], label='n={}'.format(n2))
ax.plot(sol3.t, sol3.y[0], label='n={}'.format(n3))
ax.axvline(1, ls='--', color='k')
ax.set_ylabel('$x(t)$')
ax.set_title('Position')
ax.legend()
ax = axes[1]
ax.plot(sol1.t, sol1.y[1], label='n=1')
ax.plot(sol2.t, sol2.y[1], label='n=0.7')
ax.plot(sol3.t, sol3.y[1], label='n=1.3')
ax.axvline(1, ls='--', color='k')
ax.set_ylabel('$v(t)$')
ax.set_title('Velocity')
fig.text(0.5, -0.04, '$t$', ha='center', fontsize=20)
fig.tight_layout()

#Case_III
n1, n2, n3 = 0.3,1,2
sol1 = solve_ivp(dSdt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000), args=(vg,Mu,Ms,n1))
sol2 = solve_ivp(dSdt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000),  args=(vg,Mu,Ms,n2))
sol3 = solve_ivp(dSdt, [1e-4, 3], y0=[0,0], t_eval=np.linspace(1e-4,3,1000),  args=(vg,Mu,Ms,n3))
fig, axes = plt.subplots(1, 2, figsize=(10,3))
ax = axes[0]
ax.plot(sol1.t, sol1.y[0], label='n={}'.format(n1))
ax.plot(sol2.t, sol2.y[0], label='n={}'.format(n2))
ax.plot(sol3.t, sol3.y[0], label='n={}'.format(n3))
ax.axvline(1, ls='--', color='k')
ax.set_ylabel('$x(t)$')
ax.set_title('Position')
ax.legend()
ax = axes[1]
ax.plot(sol1.t, sol1.y[1], label='n=1')
ax.plot(sol2.t, sol2.y[1], label='n=0.7')
ax.plot(sol3.t, sol3.y[1], label='n=1.3')
ax.axvline(1, ls='--', color='k')
ax.set_ylabel('$v(t)$')
ax.set_title('Velocity')
fig.text(0.5, -0.04, '$t$', ha='center', fontsize=20)
fig.tight_layout()