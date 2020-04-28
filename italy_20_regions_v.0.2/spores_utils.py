# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:07:21 2019

Script for some utility functions that help bringing to life the nos algorithm

@author: F.Lombardi
"""

import math
import pandas as pd
import numpy as np
import copy

'''
Calculation of the loch::tech score based on maxima potentials
'''
def cap_loc_score_potential(model,techs=['tech1','tech2']):
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
def cap_loc_calc(model, techs=['tech1','tech2']):
    cap_per_loc = model.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    
    return(cap_per_loc)

'''
Calculation of the energy produced/consumed in each location  
'''
def energy_loc_calc(model, techs=['tech1','tech2']):
    energy_per_loc = model.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':techs}].sum('timesteps').to_pandas()
    
    return(energy_per_loc)
    
def energycon_loc_calc(model, techs=['tech1','tech2']):
    energycon_per_loc = model.get_formatted_array('carrier_con').loc[{'carriers':'electricity', 'techs':techs}].sum('timesteps').to_pandas()
    
    return(energycon_per_loc)       
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

'''
Updating backend excl_score parameters  
'''    
def update_excl_score_params(model, tech, cap_per_loc, value):
    for j in cap_per_loc.index.values:
        try:
            model.backend.update_param('cost_energy_cap', {('excl_score',('{}::{}'.format(j,tech))) : value})
        except:
            continue
