# -*- coding: utf-8 -*-
"""
Created on Mon May 26th 2019

A script to run and post-process the Italy Calliope 20-node model based on a NOS (near-optimal solutions) logic

@author: F.Lombardi
"""
#%% Initialisation
import calliope
from static_plots import power_plot, horizontal_loc_cap_plot
from nos_utils import update_cap_params, update_cap_max_vres, vres_diff_per_loc, cap_loc_score, cap_loc_score_systemwide, cap_loc_calc, update_nos_score_params
import numpy as np
import pandas as pd
import calliope.core.io


calliope.set_log_verbosity('INFO') #sets the level of verbosity of Calliope's operations

#%% 
'''
Initialising NOS stuff
'''
cost_list = []
co2_list = []
slacks = [1.01, 1.05, 1.1]
techs=['inter_zonal_new:NORD','inter_zonal_new:CNOR','inter_zonal_new:CSUD','inter_zonal_new:SUD','inter_zonal_new:SARD','inter_zonal_new:SICI',
       'wind_new','pv_farm_new','pv_rooftop_new','phs_new','wind','pv_farm','pv_rooftop','ccgt','coal','coal_usc','oil_&_other','battery',
       'inter_zonal:NORD','inter_zonal:CNOR','inter_zonal:CSUD','inter_zonal:SUD','inter_zonal:SARD','inter_zonal:SICI']
techs_new = ['inter_zonal_new:NORD','inter_zonal_new:CNOR','inter_zonal_new:CSUD','inter_zonal_new:SUD','inter_zonal_new:SARD','inter_zonal_new:SICI',
       'wind_new','pv_farm_new','pv_rooftop_new','phs_new','battery']

#%% 
'''
--------------------------------------------------------
---------------ITERATION 0---------------(min total_cost)
--------------------------------------------------------
'''

'''
Model creation, run and saving to netCDF - Iteration 0
'''

model = calliope.Model('Model/model.yaml', scenario='2050_lowgr') #this version only includes the power sector
model.run()
model.to_netcdf('NetCDFs/results_0.nc')

'''
Alternatively, previously run solutions can be read from netCDF files
'''
#model = calliope.read_netcdf('NetCDFs/results_0.nc')
#model.run(build_only=True, force_rerun=True)
model_0 = calliope.read_netcdf('NetCDFs/results_0.nc')

'''
Extrapolation of relevant indicators
'''
#Cost class
costs_0 =  model.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()
cost_list.append(costs_0)

#CO2 class
co2_0 = model.get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()
co2_list.append(co2_0)

'''
Creation and saving of a list of slacked neighbourhoods of the optimal cost
'''
slacked_costs_list = slacks*costs_0 
slacked_costs = {'max_cost1': slacked_costs_list[0], 'max_cost5': slacked_costs_list[1], 'max_cost10': slacked_costs_list[2]}

#%%
'''
--------------------------------------------------------
---------------ITERATION 1---------------(min co2_prod, within 5% total_cost slack)
--------------------------------------------------------
'''

'''
Updating pyomo parameters
'''
model.backend.update_param('objective_cost_class', {'monetary' : 0})
model.backend.update_param('objective_cost_class', {'co2' : 1})
model.backend.update_param('group_cost_max', {('monetary','systemwide_max_slacked_cost') : slacked_costs['max_cost5']})
#model.backend.update_param('group_supply_share_min', {('electricity','vres_min_prod_share') : 0.80})

#update_cap_params(model,ccgt_0)

'''
Model re-run and saving to netCDF - NOS 1
'''
model_1 = model.backend.rerun()
for v in model_1._model_data.data_vars:
    if (isinstance(model_1._model_data[v].values.flatten()[0],(np.bool_,bool))):
        model_1._model_data[v] = model_1._model_data[v].astype(float)
model_1.to_netcdf('NetCDFs/results_1.nc')

'''
Alternatively, previously run solutions can be read from netCDF files
'''
#model_1 = calliope.read_netcdf('NetCDFs/results_1.nc')

'''
Computation of nos_scores per location, and nos_overrides writing
'''

cap_loc_score_1 = cap_loc_score(model_1,model,techs=techs)

'''
Extrapolation of relevant indicators
'''
#Cost class
costs_1 =  model_1.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()
cost_list.append(costs_1)

#CO2 class
co2_1 = model_1.get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()
co2_list.append(co2_1)


#%%
'''
--------------------------------------------------------
---------------ITERATIONS 2:n---------------(min cap_in_same_locs, within 5% total_cost slack)
--------------------------------------------------------
'''

'''
Creation of variables to store the NOS results
'''
nos_dict = {}
nos_dict[1] = model_1
cap_per_loc_dict = {}
cap_loc_score_dict = {}
incremental_score = {}
incremental_score[1] = cap_loc_score_1
cost_dict = {}

'''
Updating pyomo parameters
'''
model.backend.update_param('objective_cost_class', {'nos_score' : 1e+3})
model.backend.update_param('objective_cost_class', {'co2' : 0.01})
model.backend.update_param('group_cost_max', {('monetary','systemwide_max_slacked_cost') : slacked_costs['max_cost5']})
update_nos_score_params(model, cap_loc_score_1)

'''
Model creation and run - NOS 2:n
'''
n = 100
for j in range(2,(n+1)):
    try:
        nos_dict[j] = calliope.read_netcdf('NetCDFs/results_nos_%d.nc' % j)
        for v in nos_dict[j]._model_data.data_vars:
            if (isinstance(nos_dict[j]._model_data[v].values.flatten()[0],(np.bool_,bool))):
                nos_dict[j]._model_data[v] = nos_dict[j]._model_data[v].astype(float)
        cap_loc_score_dict[j] = cap_loc_score(nos_dict[j],model_1, techs=techs)
        incremental_score[j] = cap_loc_score_dict[j].add(incremental_score[j-1])
        update_nos_score_params(model,incremental_score[j])
        cap_per_loc_dict[j] = cap_loc_calc(nos_dict[j], i=techs_new)
    
        '''
        Extrapolation of relevant indicators, and saving to NetCDFs
        '''
        cost_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas())
        co2_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas())    
    except:
        nos_dict[j] = model.backend.rerun()
        for v in nos_dict[j]._model_data.data_vars:
            if (isinstance(nos_dict[j]._model_data[v].values.flatten()[0],(np.bool_,bool))):
                nos_dict[j]._model_data[v] = nos_dict[j]._model_data[v].astype(float)
        cap_loc_score_dict[j] = cap_loc_score(nos_dict[j],model_1, techs=techs)
        incremental_score[j] = cap_loc_score_dict[j].add(incremental_score[j-1])
        update_nos_score_params(model,incremental_score[j])
        cap_per_loc_dict[j] = cap_loc_calc(nos_dict[j], i=techs_new)
    
        '''
        Extrapolation of relevant indicators, and saving to NetCDFs
        '''
        cost_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas())
        co2_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas())
        nos_dict[j].to_netcdf('NetCDFs/results_nos_%d.nc' % j)
    #    cost
        
        '''
        Stopping criterion: when all locations have been explored
        '''
        if (cap_loc_score_dict[j][list(techs)].any().any() !=0) == False:
            break
        else:
            continue

#%%
'''
--------------------------------------------------------
---------------ITERATIONS n+1:m---------------(min already_chosen_plants_systemwide, within 5% total_cost slack)
--------------------------------------------------------
'''

'''
Reset scoring to Iteration 1, and (if required) eventually set cap_max to force homogeneous distribution
'''

'''
Creation of variables to store the NOS results
'''
#nos_dict = {}
#nos_dict[1] = model_1
#cap_per_loc_dict = {}
#cap_loc_score_dict = {}
#incremental_score = {}
#incremental_score[1] = cap_loc_score_1
#cost_dict = {}
#
#'''
#Updating pyomo parameters
#'''
#model.backend.update_param('objective_cost_class', {'nos_score' : 1e+3})
#model.backend.update_param('objective_cost_class', {'co2' : 0.01})
#model.backend.update_param('group_cost_max', {('monetary','systemwide_max_slacked_cost') : slacked_costs['max_cost10']})
#update_cap_max_vres(model)
#update_nos_score_params(model, cap_loc_score_1)
#
#'''
#Model creation and run - NOS 2:n
#'''
#n = 5
#for j in range(2,(n+1)):
#    try:
#        nos_dict[j] = calliope.read_netcdf('NetCDFs/results_nos_%d.nc' % j)
##        nos_dict[j] = model.backend.rerun()
#        for v in nos_dict[j]._model_data.data_vars:
#            if (isinstance(nos_dict[j]._model_data[v].values.flatten()[0],(np.bool_,bool))):
#                nos_dict[j]._model_data[v] = nos_dict[j]._model_data[v].astype(float)
#        cap_loc_score_dict[j] = cap_loc_score(nos_dict[j],model_1)
#    #    cap_loc_score_dict[j] = cap_loc_score_distributed(nos_dict[j],model_plan_1)
#        incremental_score[j] = cap_loc_score_dict[j].add(incremental_score[j-1])
#        update_nos_score_params(model,incremental_score[j])
#        cap_per_loc_dict[j] = cap_loc_calc(nos_dict[j])
#    
#        '''
#        Extrapolation of relevant indicators, and saving to NetCDFs
#        '''
#        cost_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas())
#        co2_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas())
##        nos_dict[j].to_netcdf('NetCDFs/results_nos_%d.nc' % j)
#    #    cost_dict[j] = nos_dict[j].get_formatted_array('cost_investment').loc[{'costs':'nos_score'}].sum(['locs']).to_pandas().T
#    except:
#        nos_dict[j] = model.backend.rerun()
#        for v in nos_dict[j]._model_data.data_vars:
#            if (isinstance(nos_dict[j]._model_data[v].values.flatten()[0],(np.bool_,bool))):
#                nos_dict[j]._model_data[v] = nos_dict[j]._model_data[v].astype(float)
#        cap_loc_score_dict[j] = cap_loc_score(nos_dict[j],model_1)
#    #    cap_loc_score_dict[j] = cap_loc_score_distributed(nos_dict[j],model_plan_1)
#        incremental_score[j] = cap_loc_score_dict[j].add(incremental_score[j-1])
#        update_nos_score_params(model,incremental_score[j])
#        cap_per_loc_dict[j] = cap_loc_calc(nos_dict[j])
#    
#        '''
#        Extrapolation of relevant indicators, and saving to NetCDFs
#        '''
#        cost_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas())
#        co2_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas())
#        nos_dict[j].to_netcdf('NetCDFs/results_nos_%d.nc' % j)
#    #    cost
#        
#        '''
#        Stopping criterion: when all locations have been explored
#        '''
#        if (cap_loc_score_dict[j][list(techs)].any().any() !=0) == False:
#            break
#        else:
#            continue
#
#%%
'''
Plotting the operation
'''
#start = '2015-03-24' # 00:00:00'
#stop = '2015-03-31' # 23:00:00'
#
#power_plot(model_0,start,stop)
##horizontal_loc_cap_plot(cap_loc_calc(model_0))
#power_plot(model_1,start,stop)
#horizontal_loc_cap_plot(cap_loc_calc(model_1))
#    
#for j in range(2,(n+1)):
#    power_plot(nos_dict[j],start,stop)
##    per_loc_cap_plot(cap_per_loc_dict[j])
#    horizontal_loc_cap_plot(cap_per_loc_dict[j])
##for jj in range(2,(m+1)):
##    power_plot(nos_dict_2[jj],start,stop)
###    per_loc_cap_plot(cap_per_loc_dict[j])
##    horizontal_loc_cap_plot(cap_per_loc_dict_2[jj]) 
#
#'''
#Performing deeper comparisons about installed caps in each loc
#'''
##vres_diff_list = []
##for j in range(2,(n+1)):
##    vres_diff_list.append(vres_diff_per_loc(nos_dict[j],nos_dict[j-1]))
