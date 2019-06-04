# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:07:21 2019

Script for some utility functions that help bringing to life the NOS algorithm

@author: F.Lombardi
"""

'''
Calculation of the loch::tech score on a 
'''

def cap_loc_score(model_new,model_ref):
    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':['wind','pv_farm','pv_rooftop','ccgt','biomass_wood','biofuel','biogas']}].to_pandas()
    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':['wind','pv_farm','pv_rooftop','ccgt','biomass_wood','biofuel','biogas']}].to_pandas()
    diff = cap_per_loc_new - cap_per_loc_ref
    diff[diff>0] = 1
    diff[diff==0] = 0
    diff[diff<0] = 0
    regionwide_score = {'NORD': {'wind':0, 'pv_farm': 0, 'pv_rooftop': 0, 'ccgt': 0, 'biomass_wood': 0, 'biofuel': 0, 'biogas': 0},
                        'CNOR': {'wind':0, 'pv_farm': 0, 'pv_rooftop': 0, 'ccgt': 0, 'biomass_wood': 0, 'biofuel': 0, 'biogas': 0},
                        'CSUD': {'wind':0, 'pv_farm': 0, 'pv_rooftop': 0, 'ccgt': 0, 'biomass_wood': 0, 'biofuel': 0, 'biogas': 0},
                        'SUD': {'wind':0, 'pv_farm': 0, 'pv_rooftop': 0, 'ccgt': 0, 'biomass_wood': 0, 'biofuel': 0, 'biogas': 0},
                        'SICI': {'wind':0, 'pv_farm': 0, 'pv_rooftop': 0, 'ccgt': 0, 'biomass_wood': 0, 'biofuel': 0, 'biogas': 0},
                        'SARD': {'wind':0, 'pv_farm': 0, 'pv_rooftop': 0, 'ccgt': 0, 'biomass_wood': 0, 'biofuel': 0, 'biogas': 0}}
    for i in diff.columns:
        regionwide_score['NORD'][i] = diff.loc[['NORD','R1','R2','R3','R4','R5','R6','R7','R8']].sum(axis=0)[i]
        regionwide_score['CNOR'][i] = diff.loc[['CNOR','R9','R10','R11']].sum(axis=0)[i]
        regionwide_score['CSUD'][i] = diff.loc[['CSUD','R12','R13','R14']].sum(axis=0)[i]
        regionwide_score['SUD'][i] = diff.loc[['SUD','R15','R16','R17','R18']].sum(axis=0)[i]
        regionwide_score['SICI'][i] = diff.loc[['SICI']].sum(axis=0)[i]
        regionwide_score['SARD'][i] = diff.loc[['SARD']].sum(axis=0)[i]
    
    diff.loc[['NORD','R1','R2','R3','R4','R5','R6','R7','R8']] = diff.loc[['NORD','R1','R2','R3','R4','R5','R6','R7','R8']]*regionwide_score['NORD']
    diff.loc[['CNOR','R9','R10','R11']] = diff.loc[['CNOR','R9','R10','R11']]*regionwide_score['CNOR']
    diff.loc[['CSUD','R12','R13','R14']] = diff.loc[['CSUD','R12','R13','R14']]*regionwide_score['CSUD']
    diff.loc[['SUD','R15','R16','R17','R18']] = diff.loc[['SUD','R15','R16','R17','R18']]*regionwide_score['SUD']
    diff.loc[['SICI']] = diff.loc[['SICI']]*regionwide_score['SICI']
    diff.loc[['SARD']] = diff.loc[['SARD']]*regionwide_score['SARD']
    
    return(diff)
    
def cap_loc_score_systemwide(model_new,model_ref):
    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':['wind','pv_farm','pv_rooftop','ccgt','biomass_wood','biofuel','biogas']}].to_pandas()
    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':['wind','pv_farm','pv_rooftop','ccgt','biomass_wood','biofuel','biogas']}].to_pandas()
    diff = cap_per_loc_new - cap_per_loc_ref
    diff[diff>0] = 1
    diff[diff==0] = 0
    diff[diff<0] = 0
    systemwide_score = {'wind':0, 'pv_farm': 0, 'pv_rooftop': 0, 'ccgt': 0, 'biomass_wood': 0, 'biofuel': 0, 'biogas': 0}
    
    for i in diff.columns:
        systemwide_score[i] = diff.sum(axis=0)[i]
        diff[i]=systemwide_score[i]
    
    return(diff)

def update_cap_max(model, i=['pv_rooftop'], max_increase=2e+6):
        
    cap_min_ref = model.get_formatted_array('energy_cap_min').loc[{'techs': i }].to_pandas()
    cap_max_new = cap_min_ref+max_increase
    
    import yaml
    
    pointer = open('Model/cap_max_overrides.yaml','r') #opens and reads the nos_overrides file
    cap_max_overrides = yaml.load(pointer)
    
    for ii in i:
        for r in cap_max_overrides.get('overrides').get('cap_max').get('locations'):
            cap_max_overrides.get('overrides').get('cap_max').get('locations')[r].get('techs')[ii]['constraints.energy_cap_max'] = float(cap_max_new[ii][r])
        with open('Model/cap_max_overrides.yaml','w') as pointer_w:
            yaml.dump(cap_max_overrides,pointer_w) #updates the nos_overrides file



def cap_loc_calc(model):
    cap_per_loc = model.get_formatted_array('energy_cap').loc[{'techs':['wind','pv_farm','pv_rooftop','ccgt','battery']}].to_pandas()
    return(cap_per_loc)
    

    
    
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
        
def update_slack_costs(slacked_costs):
    import yaml
    
    pointer = open('Model/slack_overrides.yaml','r') #opens and reads the nos_overrides file
    slack_overrides = yaml.load(pointer)
    
    for r in slack_overrides.get('overrides'):
        slack_overrides.get('overrides')[r]['group_constraints.systemwide_max_slacked_cost.cost_max.monetary'] = float(slacked_costs[r])
    with open('Model/slack_overrides.yaml','w') as pointer_w:
        yaml.dump(slack_overrides,pointer_w) #updates the nos_overrides file
        
def vres_diff_per_loc(model1,model2):
    vres_cap_per_loc1 = model1.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
    vres_cap_per_loc2 = model2.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
    vres_diff = vres_cap_per_loc1 - vres_cap_per_loc2
    return(vres_diff)
    
    
