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
from nos_utils import cap_share_calc, update_nos_score, vres_diff_per_loc, cap_loc_calc
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
--------------------------------------------------------
---------------ITERATION 0---------------(min total_cost)
--------------------------------------------------------
'''

'''
Model creation, run and saving to netCDF - Iteration 0
'''
#model_base = calliope.Model('Model/model_20_base.yaml', scenario='no_heat') #this version only includes the power sector
#model_base.run()

model_plan_0 = calliope.Model('Model/model_20_nos_score.yaml', scenario='no_heat') #this version only includes the power sector
model_plan_0.run()
model_plan_0.to_netcdf('results_0.nc')

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
#slacked_costs = pd.DataFrame(slacks*cost_list[0])
#for i in range(len(slacked_costs)):
#    slacked_costs[0][i].to_csv('slack%d' %(i+1))

#%%
'''
--------------------------------------------------------
---------------ITERATION 1---------------(min co2_prod, within 5% total_cost slack)
--------------------------------------------------------
'''

'''
Model creation, run and saving to netCDF - NOS 1
'''
model_plan_1 = calliope.Model('Model/model_20_nos_score.yaml', scenario='no_heat,min_co2,max_cost5') #this version only includes the power sector
model_plan_1.run()
model_plan_1.to_netcdf('results_1.nc')

'''
Computation of nos_scores per location, and nos_overrides writing
'''

cap_loc_score_1 = cap_loc_calc(model_plan_1,model_plan_0)
#cap_share_per_loc_1 = cap_share_calc(model_plan_1)
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
---------------ITERATIONS 2:n---------------(min cap_in_same_locs, within 10% total_cost slack)
--------------------------------------------------------
'''

'''
Model creation and run - NOS 2:n
'''
nos_dict = {}
cap_share_dict = {}
cap_loc_score_dict = {}
incremental_score = {}
incremental_score[1] = cap_loc_score_1

n = 4
for j in range(2,(n+1)):
    nos_dict[j] = calliope.Model('Model/model_20_nos_score.yaml', scenario='no_heat,max_diff,max_cost10,nos')
    nos_dict[j].run()
    cap_loc_score_dict[j] = cap_loc_calc(nos_dict[j],model_plan_1)
#   cap_share_dict[j] = cap_share_calc(nos_dict[j])
    incremental_score[j] = cap_loc_score_dict[j].add(incremental_score[j-1])
    update_nos_score(incremental_score[j])

    '''
    Extrapolation of relevant indicators
    '''
    cost_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas())
    co2_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas())
    
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
for j in range(2,(n+1)):
    power_plot(nos_dict[j],start,stop)

'''
Performing deeper comparisons about installed caps in each loc
'''
vres_diff_list = []
for j in range(2,(n+1)):
    vres_diff_list.append(vres_diff_per_loc(nos_dict[j],model_plan_1))
