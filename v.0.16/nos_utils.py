# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:07:21 2019

Script for some utility functions that help bringing to life the NOS algorithm

@author: F.Lombardi
"""

'''
Calculation of the loch::tech score on a 
'''

#def cap_loc_score(model_new,model_ref,techs=['wind','pv_farm','pv_rooftop','ccgt','ccgt_new','coal','coal_usc','oil_&_other','battery','inter_zonal:NORD','inter_zonal:CNOR','inter_zonal:CSUD','inter_zonal:SUD','inter_zonal:SARD','inter_zonal:SICI']):
#    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
#    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
#    diff = cap_per_loc_new - cap_per_loc_ref
#    diff[diff>0] = 1
#    diff[diff==0] = 0
#    diff[diff<0] = 0
#    regionwide_score = {'NORD': {'wind':1, 'pv_farm': 1, 'pv_rooftop': 1, 'ccgt': 1, 'ccgt_new': 1, 'coal': 1, 'coal_usc': 1, 'oil_&_other': 1, 'battery': 1, 'inter_zonal:NORD': 1, 'inter_zonal:CNOR': 1, 'inter_zonal:CSUD': 1, 'inter_zonal:SUD': 1, 'inter_zonal:SARD': 1, 'inter_zonal:SICI': 1},
#                        'CNOR': {'wind':1, 'pv_farm': 1, 'pv_rooftop': 1, 'ccgt': 1, 'ccgt_new': 1, 'coal': 1, 'coal_usc': 1, 'oil_&_other': 1, 'battery': 1, 'inter_zonal:NORD': 1, 'inter_zonal:CNOR': 1, 'inter_zonal:CSUD': 1, 'inter_zonal:SUD': 1, 'inter_zonal:SARD': 1, 'inter_zonal:SICI': 1},
#                        'CSUD': {'wind':1, 'pv_farm': 1, 'pv_rooftop': 1, 'ccgt': 1, 'ccgt_new': 1, 'coal': 1, 'coal_usc': 1, 'oil_&_other': 1, 'battery': 1, 'inter_zonal:NORD': 1, 'inter_zonal:CNOR': 1, 'inter_zonal:CSUD': 1, 'inter_zonal:SUD': 1, 'inter_zonal:SARD': 1, 'inter_zonal:SICI': 1},
#                        'SUD': {'wind':1, 'pv_farm': 1, 'pv_rooftop': 1, 'ccgt': 1, 'ccgt_new': 1, 'coal': 1, 'coal_usc': 1, 'oil_&_other': 1, 'battery': 1, 'inter_zonal:NORD': 1, 'inter_zonal:CNOR': 1, 'inter_zonal:CSUD': 1, 'inter_zonal:SUD': 1, 'inter_zonal:SARD': 1, 'inter_zonal:SICI': 1},
#                        'SICI': {'wind':1, 'pv_farm': 1, 'pv_rooftop': 1, 'ccgt': 1, 'ccgt_new': 1, 'coal': 1, 'coal_usc': 1, 'oil_&_other': 1, 'battery': 1, 'inter_zonal:NORD': 1, 'inter_zonal:CNOR': 1, 'inter_zonal:CSUD': 1, 'inter_zonal:SUD': 1, 'inter_zonal:SARD': 1, 'inter_zonal:SICI': 1},
#                        'SARD': {'wind':1, 'pv_farm': 1, 'pv_rooftop': 1, 'ccgt': 1, 'ccgt_new': 1, 'coal': 1, 'coal_usc': 1, 'oil_&_other': 1, 'battery': 1, 'inter_zonal:NORD': 1, 'inter_zonal:CNOR': 1, 'inter_zonal:CSUD': 1, 'inter_zonal:SUD': 1, 'inter_zonal:SARD': 1, 'inter_zonal:SICI': 1}}
#    for i in diff.columns:
#        regionwide_score['NORD'][i] = diff.loc[['NORD','R1','R2','R3','R4','R5','R6','R7','R8']].sum(axis=0)[i]
#        regionwide_score['CNOR'][i] = diff.loc[['CNOR','R9','R10','R11']].sum(axis=0)[i]
#        regionwide_score['CSUD'][i] = diff.loc[['CSUD','R12','R13','R14']].sum(axis=0)[i]
#        regionwide_score['SUD'][i] = diff.loc[['SUD','R15','R16','R17','R18']].sum(axis=0)[i]
#        regionwide_score['SICI'][i] = diff.loc[['SICI']].sum(axis=0)[i]
#        regionwide_score['SARD'][i] = diff.loc[['SARD']].sum(axis=0)[i]
#    
#    diff.loc[['NORD','R1','R2','R3','R4','R5','R6','R7','R8']] = diff.loc[['NORD','R1','R2','R3','R4','R5','R6','R7','R8']]*regionwide_score['NORD']
#    diff.loc[['CNOR','R9','R10','R11']] = diff.loc[['CNOR','R9','R10','R11']]*regionwide_score['CNOR']
#    diff.loc[['CSUD','R12','R13','R14']] = diff.loc[['CSUD','R12','R13','R14']]*regionwide_score['CSUD']
#    diff.loc[['SUD','R15','R16','R17','R18']] = diff.loc[['SUD','R15','R16','R17','R18']]*regionwide_score['SUD']
#    diff.loc[['SICI']] = diff.loc[['SICI']]*regionwide_score['SICI']
#    diff.loc[['SARD']] = diff.loc[['SARD']]*regionwide_score['SARD']
#    
#    return(diff)
   
def cap_loc_score(model_new,model_ref,techs=['wind','pv_farm','pv_rooftop','ccgt','coal','coal_usc','oil_&_other','battery','inter_zonal:NORD','inter_zonal:CNOR','inter_zonal:CSUD','inter_zonal:SUD','inter_zonal:SARD','inter_zonal:SICI']):
    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    diff = cap_per_loc_new - cap_per_loc_ref
    diff[diff>0] = 1
    diff[diff==0] = 0
    diff[diff<0] = 0
    
    return(diff)

def cap_loc_score_systemwide(model_new,model_ref,techs=['wind','pv_farm','pv_rooftop','ccgt']):
    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    diff = cap_per_loc_new - cap_per_loc_ref
    diff[diff>0] = 1
    diff[diff==0] = 0
    diff[diff<0] = 0
    systemwide_score = {'wind':1, 'pv_farm': 1, 'pv_rooftop': 1, 'ccgt': 1}
    
    for i in diff.columns:
        systemwide_score[i] = diff.sum(axis=0)[i]
        diff[i]=systemwide_score[i]
    
    return(diff)

def update_cap_max_vres(model, i=['pv_rooftop','pv_farm','wind'], max_increase=2e+6):
        
    cap_min_ref = model.get_formatted_array('energy_cap_min').loc[{'techs': i }].to_pandas()
    cap_max_new = cap_min_ref+max_increase
    
    loc_tech_cap_dict = {}
    for j in cap_max_new.columns.values:
        for i in cap_max_new.index.values:
            loc_tech_cap_dict[('{}::{}'.format(i,j))] = cap_max_new.loc[i][j]
    
    for k in loc_tech_cap_dict.keys():
        try:
            model.backend.update_param('energy_cap_max', {(k) : loc_tech_cap_dict[k]})
        except:
            continue


def cap_loc_calc(model, i=['wind_new','pv_farm_new','pv_rooftop_new', 'battery', 'phs_new']):
    cap_per_loc = model.get_formatted_array('energy_cap').loc[{'techs':i}].to_pandas()
    return(cap_per_loc)
    
def cap_loc_calc_min(model, i=['wind','pv_farm','pv_rooftop','ccgt','battery']):
    cap_per_loc_min = model.get_formatted_array('energy_cap_min').loc[{'techs':i}].to_pandas()
    return(cap_per_loc_min)
   
def vres_diff_per_loc(model1,model2):
    vres_cap_per_loc1 = model1.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
    vres_cap_per_loc2 = model2.get_formatted_array('energy_cap').loc[{'techs': ['pv_farm','pv_rooftop','wind']}].to_pandas()
    vres_diff = vres_cap_per_loc1 - vres_cap_per_loc2
    return(vres_diff)
    
    
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

def update_cap_params(model, energy_cap_loc):
    loc_tech_cap_dict = {}
    for j in energy_cap_loc.columns.values:
        for i in energy_cap_loc.index.values:
            loc_tech_cap_dict[('{}::{}'.format(i,j))] = energy_cap_loc.loc[i][j]
    
    for k in loc_tech_cap_dict.keys():
        try:
            model.backend.update_param('energy_cap_max', {(k) : loc_tech_cap_dict[k]})
            model.backend.update_param('energy_cap_min', {(k) : 0})
        except:
            continue
                      
    
    
