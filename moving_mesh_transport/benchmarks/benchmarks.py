#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 11:58:28 2022

@author: bennett
"""
import numpy as np
import matplotlib.pyplot as plt

from .benchmark_functions import make_benchmark_file_structure, write_to_file
from .benchmark_functions import check_gaussian_tail

from .uncollided import uncollided_class
from .collided import collided_class

from ..main_functions import plot_p1_su_olson_mathematica
from .test_benchmarks import test_P1_against_mathematica

###############################################################################

class make_benchmark:
    def __init__(self, source_type, x0, t0, sigma):
        self.x0 = x0
        self.t0 = t0
        self.source_type = source_type
        
        self.call_uncollided = uncollided_class(source_type, self.x0, self.t0)
        self.call_collided = collided_class(source_type, self.x0, self.t0, sigma)
        self.gaussian_type_sources = ['gaussian_IC', 'gaussian_source', 'gaussian_IC_2D', 
                                      'P1_gaussian_rad', 'P1_gaussian_mat']
        self.sigma = sigma
    
    def integrate(self, t, npnts):
        self.t = t
        print("t = ", t)
        self.npnts = npnts
        self.xs = np.linspace(0, t + self.x0, npnts)
        if self.source_type == "gaussian_IC_2D":
            if t == 1:
                self.xs = np.linspace(0.0, 3.7, npnts)
            elif t == 5:
                self.xs = np.linspace(0.0, 7.3, npnts)
            elif t == 10:
                self.xs = np.linspace(0.0, 12.4, npnts)
            
        elif self.source_type == "gaussian_IC":
            if t == 1:
                self.xs = np.linspace(0.0, 3.85, npnts)
            elif t == 5:
                self.xs = np.linspace(0.0, 7.7, npnts)
            elif t == 10:
                self.xs = np.linspace(0.0, 12.4, npnts)
        elif self.source_type == "gaussian_source":
            if t == 1:
                self.xs = np.linspace(0.0, 3.75, npnts)
            elif t == 5:
                self.xs = np.linspace(0.0, 7.5, npnts)
            elif t == 10:
                self.xs = np.linspace(0.0, 12.2, npnts)
        
        elif self.source_type == "P1_gaussian_rad" or self.source_type == "P1_gaussian_mat" and self.sigma == 300:
            if t == 1:
                self.xs = np.linspace(0.0, 1600, npnts)
            elif t == 5:
                self.xs = np.linspace(0.0, 1700, npnts)
            elif t == 10:
                self.xs = np.linspace(0.0, 1800, npnts)
        elif self.source_type == 'P1_su_olson_mat' or self.source_type == 'P1_su_olson_rad' and self.x0 == 400:
            if t == 100:
                self.xs = np.linspace(0.0, 423, npnts)
            if t == 500:
                self.xs = np.linspace(0.0, 460, npnts)
            if t == 1000:
                self.xs = np.linspace(0.0, 473, npnts)
                
            
            
        self.uncollided_sol = self.call_uncollided(self.xs, t)
        self.collided_sol = self.call_collided(self.xs, t)
        
        
        if self.source_type in self.gaussian_type_sources:
            self.gaussian = True
            tol = 1e-16
            index_of_zero_phi = check_gaussian_tail(self.uncollided_sol + self.collided_sol, tol)
            print(f"solution goes to {tol} at", self.xs[index_of_zero_phi])
        else:
            self.gaussian = False
        
        
    def save(self):
        phi = self.uncollided_sol + self.collided_sol
        if self.gaussian == True:
            x0_or_sigma = self.sigma
        else:
            x0_or_sigma = self.x0
        write_to_file(self.xs, phi, self.uncollided_sol, self.t, self.source_type, self.npnts, x0_or_sigma)
        
    
    def clear_file(self):
        make_benchmark_file_structure()
        
    def plot(self, fign):
        plt.ion()
        plt.figure(fign)
        plt.plot(self.xs, self.uncollided_sol, "--k")
        plt.plot(self.xs, self.uncollided_sol + self.collided_sol, "-k")
        if self.source_type == "P1_su_olson_rad" and self.t == 1:
                test_P1_against_mathematica(self.t, self.xs, self.collided_sol, "rad")
        elif self.source_type == "P1_su_olson_mat" and self.t == 1:
            test_P1_against_mathematica(self.t, self.xs, self.collided_sol, "mat")
            
        plt.show()
    
        
        
    
        
        
        
        
        
        
    
    