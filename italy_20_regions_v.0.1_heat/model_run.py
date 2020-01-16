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

from dispatch_plots import power_plot

p2h_size = pd.read_csv('p2h_size.csv', index_col=0)
os.chdir('calliope_model')
calliope.set_log_verbosity('INFO') #sets the level of verbosity of Calliope's operations

calliope_columns = ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10',
                    'R11','R12','R13','R14','R15','R16','R17','R18','SICI','SARD']
start = '2015-01-12 00:00:00'
stop = '2015-01-18 23:59:00'

#%% Model creation and run
model_base = calliope.Model('model.yaml') 
model_base.run()

model_p2h_tcl = calliope.Model('model.yaml', scenario='p2h_tcl')
model_p2h_tcl.run()

model_p2h_pvtcl = calliope.Model('model.yaml', scenario='p2h_pvtcl')
model_p2h_pvtcl.run()

model = calliope.Model('model.yaml', scenario='p2h_dlc')
model.run(build_only=True)
for reg in calliope_columns:
    model.backend.update_param('energy_cap_equals', {'%s::ashp' %reg : p2h_size.loc[reg]['hp'] })
    model.backend.update_param('energy_cap_equals', {'%s::tes' %reg : p2h_size.loc[reg]['hp']})
    model.backend.update_param('storage_cap_equals', {'%s::tes' %reg : p2h_size.loc[reg]['tes']})

model_p2h_dlc = model.backend.rerun()

#%% Saving model results to netCDF and to CSVs
model_base.to_netcdf('NetCDFs/model_base.nc')
model_p2h_tcl.to_netcdf('NetCDFs/model_p2h_tcl.nc')
model_p2h_pvtcl.to_netcdf('NetCDFs/model_p2h_pvtcl.nc')
model_p2h_dlc.to_netcdf('NetCDFs/model_p2h_dlc.nc')

#%% Alternatively, previously run solutions can be read from netCDF files

# model_base = calliope.read_netcdf('NetCDFs/model_base.nc')
# model_p2h_tcl = calliope.read_netcdf('NetCDFs/model_p2h_tcl.nc')
# model_p2h_pvtcl = calliope.read_netcdf('NetCDFs/model_p2h_pvtcl.nc')
# model_p2h_dlc = calliope.read_netcdf('NetCDFs/model_p2h_dlc.nc')

#%%
# Plotting
###

power_plot(model_base,start,stop)
power_plot(model_p2h_tcl,start,stop)
power_plot(model_p2h_pvtcl,start,stop)
power_plot(model_p2h_dlc,start,stop)
