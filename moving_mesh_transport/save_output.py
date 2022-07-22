#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 07:35:06 2022

@author: bennett
"""
import numpy as np
import h5py
from pathlib import Path

class save_output:
    def __init__(self, tfinal, N_spaces, Ms, source_type, moving, uncollided, major,
                 thermal_couple, temp_function, c, sigma, x0, cv_const, problem_type):
        data_folder = Path("moving_mesh_transport")
        self.solution_file_path = data_folder / 'run_data.h5'
        self.problem_type = problem_type              
        self.Ms = Ms
        self.tfinal = tfinal
        self.moving = moving
        self.uncollided = uncollided
        self.major = major
        self.N_spaces = N_spaces
        self.x0 = x0
        self.thermal_couple = thermal_couple
        self.temp_function = temp_function
        self.c = c
        self.sigma = sigma
        self.cv_const = cv_const

        if self.problem_type == 'transport':
            self.config_file_path = data_folder / 'run_data_transport_RMS.h5'
        elif self.problem_type in ['su_olson, su_olson_s2, su_olson_thick, su_olson_thick_s2']:
            self.config_file_path = data_folder / 'run_data_su_olson_RMS.h5'

        source_name_list = ["plane_IC", "square_IC", "square_s", "gaussian_IC", "MMS", "gaussian_s"]
        gaussian_sources = ["gaussian_IC", "gaussian_s"]
        index_of_source_name = np.argmin(np.abs(np.array(source_type)-1))
        self.source_name = source_name_list[index_of_source_name]  
              
    def save_RMS(self, RMS_list, energy_RMS_list, N_angles, r_times):
        if (self.tfinal == 1 or self.tfinal == 5 or self.tfinal == 10) or (self.thermal_couple == 1 and self.tfinal == 31.6228) :
            saving_condition = True
        else:
            saving_condition = False
            
        if self.major == 'cells':
            if saving_condition == True:
                print("saving")
                f = h5py.File(self.config_file_path, 'a')
                dest_str = str(self.source_name + "/" + "t="  + str(int(self.tfinal)) + "/" + "RMS")
                destination = f[dest_str]
                rms_str = self.uncollided * ("uncollided_")  + (not(self.uncollided))  * ("no_uncollided_")  + self.moving * ("moving_") + (not(self.moving)) * ("static_") + "M_" + str(self.Ms[0])
                if destination.__contains__(rms_str):
                    del destination[rms_str]
                dset = destination.create_dataset(rms_str, (6, len(self.N_spaces)) )
                dset[0] = self.N_spaces
                dset[1] = RMS_list
                dset[2] = N_angles
                dset[3] = r_times
                dset[4] = self.Ms
                dset[5] = energy_RMS_list
                f.close()
                
        elif self.major == 'Ms':
            if saving_condition == True :
                print("saving")
                f = h5py.File(self.config_file_path, 'a')
                dest_str = str(self.source_name + "/" + "t="  + str(int(self.tfinal)) + "/" + "RMS")
                
                if not f.__contains__(dest_str):
                    f.create_group(dest_str)
                destination = f[dest_str]
                
                destination = f[dest_str]
                rms_str = 'Ms_' + self.uncollided * ("uncollided_")  + (not(self.uncollided))  * ("no_uncollided_")  + self.moving * ("moving") + (not(self.moving)) * ("static")
                if destination.__contains__(rms_str):
                    del destination[rms_str]
                dset = destination.create_dataset(rms_str, (6, len(self.N_spaces)) )
                dset[0] = self.Ms
                dset[1] = RMS_list
                dset[2] = N_angles
                dset[3] = r_times
                dset[4] = self.N_spaces
                dset[5] = energy_RMS_list
                f.close()
            
    def save_RMS_P1_su_olson(self, RMS_list, energy_RMS_list, N_angles, r_times, ang):
        saving_condition = True
        if int(self.sigma) == 300:
            self.source_name = 'gaussian_s_thick' 
        elif self.x0[0] == 400.0:
            self.source_name = 'su_olson_thick'
        print("saving source name", self.source_name)
        if saving_condition == True :
            if self.major == 'cells':
                print("saving RMSE")
                f = h5py.File(self.config_file_path, 'a')
                if self.tfinal != 31.6228:
                    self.tfinal = int(self.tfinal)
                dest_str = str(self.source_name + "/" + "t="  + str(int(self.tfinal)) + "/" + "RMS" + "/" + f"S{ang}")
                
                if not f.__contains__(dest_str):
                    f.create_group(dest_str)
                destination = f[dest_str]
                
                rms_str =  self.uncollided * ("uncollided_")  + (not(self.uncollided))  * ("no_uncollided_")  + self.moving * ("moving_") + (not(self.moving)) * ("static_") + "M_" + str(self.Ms[0])
                if destination.__contains__(rms_str):
                    del destination[rms_str]
                dset = destination.create_dataset(rms_str, (6, len(self.N_spaces)) )
                dset[0] = self.N_spaces
                dset[1] = RMS_list
                dset[2] = N_angles
                dset[3] = r_times
                dset[4] = self.Ms
                dset[5] = energy_RMS_list
                f.close()
            
            elif self.major == 'Ms':
                print("saving RMSE")
                f = h5py.File(self.config_file_path, 'a')
                dest_str = str(self.source_name + "/" + "t="  + str(int(self.tfinal)) + "/" + "RMS" + "/" + f"S{ang}")
                print(dest_str)
                
                if not f.__contains__(dest_str):
                    f.create_group(dest_str)
                destination = f[dest_str]
                
                destination = f[dest_str]
                rms_str = 'Ms_' + self.uncollided * ("uncollided_")  + (not(self.uncollided))  * ("no_uncollided_")  + self.moving * ("moving") + (not(self.moving)) * ("static")
                if destination.__contains__(rms_str):
                    del destination[rms_str]
                dset = destination.create_dataset(rms_str, (6, len(self.N_spaces)))
                dset[0] = self.Ms
                dset[1] = RMS_list
                dset[2] = N_angles
                dset[3] = r_times
                dset[4] = self.N_spaces
                dset[5] = energy_RMS_list
                f.close()
                
    def save_solution(self, xs, phi, e, sol_matrix, x0_or_sigma, ws, N_space, s2):
        "transport or transfer/source_name/t = {tfinal}/c = {c}/ x0(or sigma) = {val}"
        
        f = h5py.File(self.solution_file_path, 'a')
        
        if self.problem_type == 'transport':
            folder_name = "transport"
        elif self.problem_type == 'rad_transfer_constant_cv':
            folder_name =  f"transfer_const_cv={self.cv_const}"
        elif self.problem_type == "su_olson_s2":
            folder_name = "su_olson_s2"
        elif self.problem_type == "su_olson_thick_s2":
            folder_name = "su_olson_thick_s2"
        elif self.problem_type == "su_olson_thick":
            folder_name = "su_olson_thick"
        elif self.problem_type == "su_olson":
            folder_name = "su_olson"
        else:
            folder_name = 'none'
        if not f.__contains__(folder_name):
            f.create_group(folder_name)
        full_str = ''

        

        
        full_str += "/" + str(self.source_name) + '_uncollided_' * (self.uncollided) + 'moving_mesh_' * (self.moving) + 'N_space = ' + str(N_space) + '_t = ' + str(int(self.tfinal)) + '_c = ' + str(self.c) + '_x0_or_sigma = ' + str(x0_or_sigma)
        print(full_str)
        if f[folder_name].__contains__(full_str):
            del f[folder_name][full_str]
        
        dset = f[folder_name].create_dataset(full_str, (4, len(xs)))
        
        print("saving solution")
        dset[0] = xs
        dset[1] = phi
        dset[2] = e
        # dset[2] = self.ws
        # dset[3] = sol_matrix
        
        if f[folder_name].__contains__('coefficients/' + full_str):
            del f[folder_name]['coefficients/' + full_str]
        
        size = np.shape(sol_matrix)
        dset2  = f[folder_name].create_dataset('coefficients/' + full_str, data = sol_matrix)
        
        if f[folder_name].__contains__('weights/' + full_str):
            del f[folder_name]['weights/' + full_str]
            
        dset3  = f[folder_name].create_dataset('weights/' + full_str, data = ws) 

     
        
        f.close()        
     
   
        
    
        
        
        
        
        
            
        
        
        
        
        
            
            
            
            
            
    

            
            
