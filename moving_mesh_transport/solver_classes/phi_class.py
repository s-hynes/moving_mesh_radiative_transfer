#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 09:26:00 2022

@author: bennett
"""
import numpy as np

from .build_problem import build

from numba import float64, int64, deferred_type
from numba.experimental import jitclass
###############################################################################
build_type = deferred_type()
build_type.define(build.class_type.instance_type)

data = [("P", float64[:]),
        ("ws", float64[:]),
        ("M", int64),
        ("u", float64[:,:]),
        ('thermal_couple', int64),
        ("vec", float64[:,:])
        ]
###############################################################################
@jitclass(data)
class scalar_flux(object):
    def __init__(self, build):
        self.P = np.zeros(build.M+1).transpose()
        self.M = build.M
        self.ws = build.ws
        self.thermal_couple = build.thermal_couple
    def make_P(self, u):
        if self.thermal_couple == 1:
            vec = u[:-1,:]
        elif self.thermal_couple == 0:
            vec = u
        for i in range(0, self.M+1):
            self.P[i]  = np.sum(np.multiply(vec[:,i],self.ws))
        return self.P
        
