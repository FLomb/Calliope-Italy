# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:07:21 2019

Script for some utility functions that help bringing to life the NOS algorithm

@author: F.Lombardi
"""

'''
Calculation of the cap_share on a per_tech and per_location basis
'''

def cap_loc_calc(model_new,model_ref):
    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':['wind','pv_farm','pv_rooftop','ccgt']}].to_pandas()
    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':['wind','pv_farm','pv_rooftop','ccgt']}].to_pandas()
    diff = cap_per_loc_new - cap_per_loc_ref
    diff[diff>0] = 1
    diff[diff<0] = 0
    return(diff)
    


def cap_share_calc(model):
    cap_per_loc = model.get_formatted_array('energy_cap').loc[{'techs':['wind','pv_farm','pv_rooftop','ccgt']}].to_pandas()
    tot_cap_per_loc = model.get_formatted_array('energy_cap').loc[{'techs':['biofuel', 'biogas', 'biomass_wood', 'ccgt', 'coal', 
                                                      'coal_usc', 'geothermal', 'hydro_dam', 'hydro_ror', 'oil_&_other', 'phs', 'pv_farm', 
                                                      'pv_rooftop', 'wind', 'wte']}].sum('techs').to_pandas()
    cap_share_per_loc = cap_per_loc/tot_cap_per_loc.sum()
    return(cap_share_per_loc)
    
    
def update_nos_score(cap_share_per_loc):
    import yaml
    
    pointer = open('Model/nos_overrides.yaml','r') #opens and reads the nos_overrides file
    nos_overrides = yaml.load(pointer)
    
    for r in nos_overrides.get('overrides').get('nos').get('locations'):
        nos_overrides.get('overrides').get('nos').get('locations')[r].get('techs')['wind']['costs.nos_score.energy_cap'] = float(cap_share_per_loc['wind'][r])
        nos_overrides.get('overrides').get('nos').get('locations')[r].get('techs')['pv_farm']['costs.nos_score.energy_cap'] = float(cap_share_per_loc['pv_farm'][r])
        nos_overrides.get('overrides').get('nos').get('locations')[r].get('techs')['pv_rooftop']['costs.nos_score.energy_cap'] = float(cap_share_per_loc['pv_rooftop'][r])
    with open('Model/nos_overrides.yaml','w') as pointer_w:
        yaml.dump(nos_overrides,pointer_w) #updates the nos_overrides file
        
def vres_diff_per_loc(model1,model2):
    vres_cap_per_loc1 = model1.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
    vres_cap_per_loc2 = model2.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
    vres_diff = vres_cap_per_loc1 - vres_cap_per_loc2
    return(vres_diff)