# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 2018

A script to run and post-process the Italy Calliope 20-node model

@author: F.Lombardi
"""
#%% Initialisation
import calliope
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

os.chdir('calliope_model')
calliope.set_log_verbosity('INFO') #sets the level of verbosity of Calliope's operations

#%% Model creation and run
model = calliope.Model('model/model.yaml', scenario='no_heat')
model.run()

#%% Saving model results to netCDF and to CSVs
#model.to_netcdf('NetCDFs/res_no_heat.nc')

#%% Alternatively, previously run solutions can be read from netCDF files

#model_test = calliope.read_netcdf('NetCDFs/res_no_heat.nc')

