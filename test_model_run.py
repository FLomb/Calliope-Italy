# -*- coding: utf-8 -*-
"""
Created on Mon May 26th 2019

A script to run and post-process the Italy Calliope 20-node model in the direction
of implementing NOS algorithms

@author: F.Lombardi
"""
#%% Initialisation
import calliope
from static_plots import power_plot, dhw_plot

calliope.set_log_level('ERROR') #sets the level of verbosity of Calliope's operations

#%% 
'''
Initialising NOS stuff
'''
cost_list = []
slack = 1.1

#%% 
'''
Model creation and run
'''
model_test = calliope.Model('Model/model_20.yaml') #this version of the model includes both power and DHW supplied by P2H
model_test.run()

#model_test2 = calliope.Model('model_20.yaml', scenario='no_heat') #this version only includes the power sector
#model_test2.run()

#%% 
'''
Saving model results to netCDF and to CSVs
'''
#model_test.to_netcdf('test_results_p2h.nc')
#model_test2.to_netcdf('test_results_bau.nc')

#%% 
'''
Alternatively, previously run solutions can be read from netCDF files
'''
#model_test = calliope.read_netcdf('test_results_p2hSmallSto.nc')
#model_test2 = calliope.read_netcdf('test_results_bau.nc')

#%% 
'''
Extrapolation of relevant indicators
'''
#Cost class
costs =  model_test.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()
cost_list.append(costs)
slacked_cost = slack*cost_list[0]

#CO2 class
co2 = model_test.get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()

#%%
'''
Plotting the operation
'''
start = '2015-01-01 00:00:00'
stop = '2015-01-07 23:00:00'

power_plot(model_test,start,stop)
dhw_plot(model_test,start,stop)
