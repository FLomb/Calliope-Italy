# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:07:21 2019

Script for some utility functions that help bringing to life the NOS algorithm

@author: F.Lombardi
"""

import math

'''
Calculation of the loch::tech score  
'''
def cap_loc_score_smart(model_new,model_ref,techs=['wind','pv_farm','pv_rooftop','ccgt','coal','coal_usc','oil_&_other','battery','inter_zonal:NORD','inter_zonal:CNOR','inter_zonal:CSUD','inter_zonal:SUD','inter_zonal:SARD','inter_zonal:SICI']):
    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    diff = cap_per_loc_new - cap_per_loc_ref
    for t in techs:
        for l in diff.index:
            if diff[t].loc[l] < -1e3:
                diff[t].loc[l] = 0
            elif diff[t].loc[l] > 1e3:
                diff[t].loc[l] = round(diff[t].loc[l]/1e6,1)
            elif (diff[t].loc[l] == 0 or 0 < diff[t].loc[l] < 1e3 or -1e3 < diff[t].loc[l] < 0) and cap_per_loc_ref[t].loc[l] > 1:
                diff[t].loc[l] = 1
            else:
                diff[t].loc[l] = 0

    return(diff)  

'''
Calculation of the loch::tech score  
'''
def cap_loc_score_potential(model,techs=['wind','pv_farm','pv_rooftop','ccgt','coal','coal_usc','oil_&_other','battery','inter_zonal:NORD','inter_zonal:CNOR','inter_zonal:CSUD','inter_zonal:SUD','inter_zonal:SARD','inter_zonal:SICI']):
    cap_per_loc = model.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    cap_per_loc_max = model.get_formatted_array('energy_cap_max').loc[{'techs':techs}].to_pandas()
    ratio = cap_per_loc / cap_per_loc_max
    for t in techs:
        for l in ratio.index:
            if ratio[t].loc[l] < 1e-3:
                ratio[t].loc[l] = 0
            elif math.isnan(ratio[t].loc[l]):
                ratio[t].loc[l] = 0
            else:
                continue
    return(ratio)  
  
'''
Calculation of the capacity installed in each location  
'''
def cap_loc_calc(model, techs=['wind_new','pv_farm_new','pv_rooftop_new', 'battery', 'phs_new']):
    cap_per_loc = model.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    
    return(cap_per_loc)
    
'''
Calculation of the minimum capacity installable in each location  
'''    
def cap_loc_calc_min(model, techs=['wind','pv_farm','pv_rooftop','ccgt','battery']):
    cap_per_loc_min = model.get_formatted_array('energy_cap_min').loc[{'techs':techs}].to_pandas()
    cap_per_loc_min = cap_per_loc_min.fillna(value=0)
    
    return(cap_per_loc_min) 

'''
Updating backend nos_score parameters  
'''    
def update_nos_score_params(model, cap_loc_score):
    loc_tech_score_dict = {}
    for j in cap_loc_score.columns.values:
        for i in cap_loc_score.index.values:
            loc_tech_score_dict[('{}::{}'.format(i,j))] = cap_loc_score.loc[i][j]
    
    for k in loc_tech_score_dict:
        try:
            model.backend.update_param('cost_energy_cap', {('nos_score',k) : loc_tech_score_dict[k]})
        except:
            continue

                      
    
    
