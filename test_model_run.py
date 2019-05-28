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
import numpy as np
import pandas as pd

calliope.set_log_level('ERROR') #sets the level of verbosity of Calliope's operations

#%% 
'''
Initialising NOS stuff
'''
cost_list = []
co2_list = []
slacks = [1.01, 1.05, 1.1]

#%% 
'''
Model creation, run and saving to netCDF - Iteration 0
'''
#model_base = calliope.Model('Model/model_20_base.yaml', scenario='no_heat') #this version only includes the power sector
#model_base.run()

#model_base_p2h = calliope.Model('Model/model_20_base.yaml') #this version of the model includes both power and DHW supplied by P2H
#model_base_p2h.run()

model_plan_0 = calliope.Model('Model/model_20.yaml', scenario='no_heat') #this version only includes the power sector
model_plan_0.run()
model_plan_0.to_netcdf('results_0.nc')

'''
Extrapolation of relevant indicators
'''
#Cost class
costs =  model_plan_0.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()
cost_list.append(costs)

#CO2 class
co2 = model_plan_0.get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()
co2_list.append(co2)

'''
Creation and saving of a list of slacked neighbourhoods of the optimal cost
'''
#slacked_costs = pd.DataFrame(slacks*cost_list[0])
#for i in range(len(slacked_costs)):
#    slacked_costs[0][i].to_csv('slack%d' %(i+1))

#%%
'''
Model creation, run and saving to netCDF - NOS 1,2,3
'''
##model_plan_1 = calliope.Model('Model/model_20.yaml', override_dict="{'no_heat','min_co2','maxcost1.group_constraints.systemwide_max_slacke_cost.cost_max.montery:5.45792e+08'}") #this version only includes the power sector
model_plan_1 = calliope.Model('Model/model_20.yaml', scenario='no_heat,min_co2,max_cost1') #this version only includes the power sector
model_plan_1.run()
model_plan_1.to_netcdf('results_1.nc')

model_plan_2 = calliope.Model('Model/model_20.yaml', scenario='no_heat,min_co2,max_cost2') #this version only includes the power sector
model_plan_2.run()
model_plan_2.to_netcdf('results_2.nc')

model_plan_3 = calliope.Model('Model/model_20.yaml', scenario='no_heat,min_co2,max_cost3') #this version only includes the power sector
model_plan_3.run()
model_plan_3.to_netcdf('results_03.nc')


#%% 
'''
Alternatively, previously run solutions can be read from netCDF files
'''
#model_test = calliope.read_netcdf('test_results_p2hSmallSto.nc')
#model_test2 = calliope.read_netcdf('test_results_bau.nc')


#%%
'''
Plotting the operation
'''
start = '2015-03-30 00:00:00'
stop = '2015-04-05 23:00:00'

power_plot(model_plan_0,start,stop)
power_plot(model_plan_1,start,stop)
power_plot(model_plan_2,start,stop)
power_plot(model_plan_3,start,stop)
##dhw_plot(model_test,start,stop)

#%% Checks
plants_cap_0 = model_plan_0.get_formatted_array('energy_cap').sum('locs').to_pandas().T 
plants_cap_1 = model_plan_3.get_formatted_array('energy_cap').sum('locs').to_pandas().T 
plants_cap_2 = model_plan_3.get_formatted_array('energy_cap').sum('locs').to_pandas().T 
plants_cap_3 = model_plan_3.get_formatted_array('energy_cap').sum('locs').to_pandas().T 
diff = plants_cap_3 - plants_cap_0
diff

#check delta VRES on a per-location basis
vres_0 = model_plan_0.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
vres_1 = model_plan_3.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
vres_2 = model_plan_3.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
vres_3 = model_plan_3.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
vres_diff = vres_3 - vres_0
vres_diff