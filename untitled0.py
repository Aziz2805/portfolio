# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 22:27:59 2023

@author: azizc
"""

import numpy as np
import matplotlib.pyplot as plt

def f(x,y):
    return np.sin(x)**10 + np.cos(x*y)*np.cos(x)

X=np.linspace(0,5,500)
Y=np.linspace(0,5,500)
XX,YY=np.meshgrid(X,Y)

ZZ = f(XX,YY)

plt.plot(ZZ)
