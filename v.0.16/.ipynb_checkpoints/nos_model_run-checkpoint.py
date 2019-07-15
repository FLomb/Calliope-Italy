# -*- coding: utf-8 -*-
"""
Created on Mon May 26th 2019

A script to run and post-process the Italy Calliope 20-node model based on a NOS (near-optimal solutions) logic

@author: F.Lombardi
"""
#%% Initialisation
import calliope
from static_plots import power_plot, per_loc_cap_plot, horizontal_loc_cap_plot
from nos_utils import update_nos_score, update_cap_max, update_slack_costs, vres_diff_per_loc, cap_loc_score, cap_loc_score_systemwide, cap_loc_calc
import numpy as np
import pandas as pd


calliope.set_log_level('SOLVER') #sets the level of verbosity of Calliope's operations

#%% 
'''
Initialising NOS stuff
'''
cost_list = []
co2_list = []
slacks = [1.01, 1.05, 1.1]

#%% 
'''
--------------------------------------------------------
---------------ITERATION 0---------------(min total_cost)
--------------------------------------------------------
'''

'''
Model creation, run and saving to netCDF - Iteration 0
'''
#model_base = calliope.Model('Model/model_20_base.yaml', scenario='no_heat') #this version only includes the power sector
#model_base.run()

model_plan_0 = calliope.Model('Model/model.yaml', scenario='battery_storage,no_heat,cap_max_tim') #this version only includes the power sector
model_plan_0.run()
model_plan_0.to_netcdf('NetCDFs/results_0.nc')

'''
Alternatively, previously run solutions can be read from netCDF files
'''
#model_plan_0 = calliope.read_netcdf('NetCDFs/results_0.nc')

'''
Extrapolation of relevant indicators
'''
#Cost class
costs_0 =  model_plan_0.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()
cost_list.append(costs_0)

#CO2 class
co2_0 = model_plan_0.get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()
co2_list.append(co2_0)

'''
Creation and saving of a list of slacked neighbourhoods of the optimal cost
'''
slacked_costs_list = slacks*costs_0 
slacked_costs = {'max_cost1': slacked_costs_list[0], 'max_cost5': slacked_costs_list[1], 'max_cost10': slacked_costs_list[2]}
update_slack_costs(slacked_costs)

#%%
'''
--------------------------------------------------------
---------------ITERATION 1---------------(min co2_prod, within 1% total_cost slack)
--------------------------------------------------------
'''

'''
Model creation, run and saving to netCDF - NOS 1
'''
model_plan_1 = calliope.Model('Model/model.yaml', scenario='battery_storage,no_heat,min_co2,max_cost1') #this version only includes the power sector
model_plan_1.run()
model_plan_1.to_netcdf('NetCDFs/results_1.nc')

'''
Alternatively, previously run solutions can be read from netCDF files
'''
#model_plan_1 = calliope.read_netcdf('NetCDFs/results_1.nc')

'''
Computation of nos_scores per location, and nos_overrides writing
'''

cap_loc_score_1 = cap_loc_score(model_plan_1,model_plan_0)
#cap_loc_score_1 = cap_loc_score_distributed(model_plan_1,model_plan_0)
update_nos_score(cap_loc_score_1)

'''
Extrapolation of relevant indicators
'''
#Cost class
costs_1 =  model_plan_1.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()
cost_list.append(costs_1)

#CO2 class
co2_1 = model_plan_1.get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()
co2_list.append(co2_1)


#%%
'''
--------------------------------------------------------
---------------ITERATIONS 2:n---------------(min cap_in_same_locs, within 5% total_cost slack)
--------------------------------------------------------
'''

'''
Model creation and run - NOS 2:n
'''
nos_dict = {}
nos_dict[1] = model_plan_1
cap_per_loc_dict = {}
cap_loc_score_dict = {}
incremental_score = {}
incremental_score[1] = cap_loc_score_1

n = 5
for j in range(2,(n+1)):
    nos_dict[j] = calliope.Model('Model/model.yaml', scenario='battery_storage,no_heat,max_diff,max_cost5,nos,cap_max_tim')
    nos_dict[j].run()
    cap_loc_score_dict[j] = cap_loc_score(nos_dict[j],model_plan_1)
#    cap_loc_score_dict[j] = cap_loc_score_distributed(nos_dict[j],model_plan_1)
    incremental_score[j] = cap_loc_score_dict[j].add(incremental_score[j-1])
    update_nos_score(incremental_score[j])
    cap_per_loc_dict[j] = cap_loc_calc(nos_dict[j])

    '''
    Extrapolation of relevant indicators, and saving to NetCDFs
    '''
    cost_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas())
    co2_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas())
#    nos_dict[j].to_netcdf('NetCDFs/results_nos_%d.nc' % j)

    '''
    Stopping criterion: when all locations have been explored
    '''
#    if (incremental_score[j].all()[{'wind','pv_farm','pv_rooftop'}].all() > 0) == True:
#        break
#    else:
#        continue

#%%
'''
--------------------------------------------------------
---------------ITERATIONS n+1:m---------------(min already_chosen_plants_systemwide, within 5% total_cost slack)
--------------------------------------------------------
'''

'''
Reset scoring to Iteration 1, and (if required) eventually set cap_max to force homogeneous distribution
'''
update_nos_score(cap_loc_score_1)
#update_cap_max(model_plan_1, i=['pv_farm','pv_rooftop','biomass_wood','biofuel','biomass_wood'])

'''
Model creation and run - NOS n+1:m
'''
nos_dict_2 = {}
nos_dict_2[1] = model_plan_1
cap_per_loc_dict_2 = {}
cap_loc_score_dict_2 = {}
incremental_score_2 = {}
incremental_score_2[1] = cap_loc_score_1

m = 5
for j in range(2,(m+1)):
    nos_dict_2[j] = calliope.Model('Model/model.yaml', scenario='battery_storage,no_heat,max_diff,max_cost5,nos,cap_max_tim')
    nos_dict_2[j].run()
    cap_loc_score_dict_2[j] = cap_loc_score_systemwide(nos_dict_2[j],model_plan_1)
#    cap_loc_score_dict[j] = cap_loc_score_distributed(nos_dict[j],model_plan_1)
    incremental_score_2[j] = cap_loc_score_dict_2[j].add(incremental_score_2[j-1])
    update_nos_score(incremental_score_2[j])
    cap_per_loc_dict_2[j] = cap_loc_calc(nos_dict_2[j])

    '''
    Extrapolation of relevant indicators, and saving to NetCDFs
    '''
    cost_list.append(nos_dict_2[j].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas())
    co2_list.append(nos_dict_2[j].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas())
    nos_dict_2[j].to_netcdf('NetCDFs/results_nos_2_%d.nc' % j)

    '''
    Stopping criterion: when all locations have been explored
    '''
#    if (incremental_score[j].all()[{'wind','pv_farm','pv_rooftop'}].all() > 0) == True:
#        break
#    else:
#        continue

#%%
'''
Plotting the operation
'''
start = '2015-03-30 00:00:00'
stop = '2015-04-05 23:00:00'

power_plot(model_plan_0,start,stop)
power_plot(model_plan_1,start,stop)
for j in range(2,(n+1)):
    power_plot(nos_dict[j],start,stop)
#    per_loc_cap_plot(cap_per_loc_dict[j])
    horizontal_loc_cap_plot(cap_per_loc_dict[j])
for jj in range(2,(m+1)):
    power_plot(nos_dict_2[jj],start,stop)
#    per_loc_cap_plot(cap_per_loc_dict[j])
    horizontal_loc_cap_plot(cap_per_loc_dict_2[jj]) 

'''
Performing deeper comparisons about installed caps in each loc
'''
#vres_diff_list = []
#for j in range(2,(n+1)):
#    vres_diff_list.append(vres_diff_per_loc(nos_dict[j],nos_dict[j-1]))
