# -*- coding: utf-8 -*-
"""
Created on Mon May 26th 2019

A script to run and post-process the Italy Calliope 20-node model based on a NOS (near-optimal solutions) logic

@author: F.Lombardi
"""
#%% Initialisation
import calliope
from static_plots import power_plot, horizontal_loc_cap_plot
from nos_utils import cap_loc_calc_min, vres_diff_per_loc, cap_loc_score, cap_loc_score_systemwide, cap_loc_calc, update_nos_score_params
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import copy

#%% 
'''
Initialising NOS stuff
'''

cost_list = []
co2_list = []
slacks = [1.01, 1.05, 1.1]

def cap_loc_score_simple(model_new,model_ref,techs=['wind_offshore','wind_new','pv_farm_new','pv_rooftop_new','battery','inter_zonal_new:NORD','inter_zonal_new:CNOR','inter_zonal_new:CSUD','inter_zonal_new:SUD','inter_zonal_new:SARD','inter_zonal_new:SICI']):
    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    diff = cap_per_loc_new - cap_per_loc_ref
    diff[diff>0] = 1
    diff[diff==0] = 0
    diff[diff<0] = 0
    
    return(diff)

def cap_loc_score_pure(model_new,model_ref,techs=['wind_offshore','wind_new','pv_farm_new','pv_rooftop_new','battery','inter_zonal_new:NORD','inter_zonal_new:CNOR','inter_zonal_new:CSUD','inter_zonal_new:SUD','inter_zonal_new:SARD','inter_zonal_new:SICI']):
    cap_per_loc_new = model_new.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    cap_per_loc_ref = model_ref.get_formatted_array('energy_cap').loc[{'techs':techs}].to_pandas()
    diff = cap_per_loc_new - cap_per_loc_ref
    diff[diff==0] = 0
    diff[diff<0] = 0
    
    return(diff)

def regionwide_simple_score(cumulated_simple_score):
    new_score = pd.DataFrame(columns=cumulated_simple_score.columns)
    new_score.loc['NORD'] = cumulated_simple_score.loc[['NORD','R1','R2','R3','R4','R5','R6','R7','R8']].sum().rename('NORD') 
    new_score.loc['CNOR'] = cumulated_simple_score.loc[['CNOR','R9','R10','R11']].sum().rename('NORD') 
    new_score.loc['CSUD'] = cumulated_simple_score.loc[['CSUD','R12','R13','R14']].sum().rename('CSUD')
    new_score.loc['SUD'] = cumulated_simple_score.loc[['SUD','R15','R16','R17','R18']].sum().rename('SUD')
    new_score.loc['SARD'] = cumulated_simple_score.loc[['SARD']].sum().rename('NORD') 
    new_score.loc['SICI'] = cumulated_simple_score.loc[['SICI']].sum().rename('NORD') 
    
    return(new_score)

def regionwide_freq_score(frequency_dict, techs):
    freq_dict = copy.deepcopy(frequency_dict)
    freq_df = pd.DataFrame(columns=freq_dict.keys(), index=freq_dict[techs[0]].index)
    for i in freq_dict:
        freq_dict[i][freq_dict[i]>0] = 1
        freq_dict[i][freq_dict[i]==0] = 0
        freq_dict[i][freq_dict[i]<0] = 0
        freq_dict[i] = freq_dict[i].sum(axis=1)/len(freq_dict)
        freq_df[i] = freq_dict[i]
        
    return(freq_df)

def curt_exp_vresshare(model):
    curt_exp = -model.get_formatted_array('carrier_con').loc[{'techs':['el_export','el_curtailment']}].sum(['locs','timesteps']).to_pandas()
    vres_prod = model.get_formatted_array('carrier_prod').loc[{'techs':['pv_farm','pv_rooftop','wind','pv_farm_new','pv_rooftop_new','wind_new','wind_offshore']}].sum(['locs','timesteps']).to_pandas().T
    tot_prod = model.get_formatted_array('carrier_prod').loc[{'techs':['wind_offshore','wind','pv_farm','pv_rooftop','wind_new','pv_farm_new','pv_rooftop_new','ccgt','coal','coal_usc','oil_&_other','hydro_ror','hydro_dam','biomass_wood','biogas','biofuel','wte','geothermal','el_import']}].sum(['locs','timesteps']).to_pandas().T.sum()
    vres_share = (vres_prod.sum()/tot_prod.sum()).to_frame().T
    vres_share.columns = ['vres_share']
    vres_share.index = ['electricity']
    complete_info = curt_exp.join(vres_share)
    el_import = model.get_formatted_array('carrier_prod').loc[{'techs':'el_import'}].sum(['locs','timesteps']).to_pandas().T.to_frame()
    el_import.columns = ['el_import']
    complete_info = complete_info.join(el_import)
    
    return(complete_info)
    
def vres_shannon_index(model):
    pv_prod = model.get_formatted_array('carrier_prod').loc[{'techs':['pv_farm','pv_rooftop','pv_farm_new','pv_rooftop_new']}].sum(['techs','timesteps']).to_pandas().T
    wind_prod = model.get_formatted_array('carrier_prod').loc[{'techs':['wind','wind_new','wind_offshore']}].sum(['techs','timesteps']).to_pandas().T
    tot_vres_prod = pv_prod + wind_prod
    share_pv = pv_prod / tot_vres_prod.sum()
    share_wind = wind_prod / tot_vres_prod.sum()
    shannon_index = pd.DataFrame(index=tot_vres_prod.index, columns=['Shannon_index'])
    for r in tot_vres_prod.index:
        shannon_index.loc[r] = max(0,(-share_pv.loc[r].values[0] * np.log(share_pv.loc[r].values[0]))) + max(0,(-share_wind.loc[r].values[0] * np.log(share_wind.loc[r].values[0])))
    shannon_index = shannon_index.sum()
    
    return(shannon_index)

def vres_new_shannon_index(model,model0):
    pv_prod = model.get_formatted_array('carrier_prod').loc[{'techs':['pv_farm_new','pv_rooftop_new']}].sum(['techs','timesteps']).to_pandas().T
    wind_prod = model.get_formatted_array('carrier_prod').loc[{'techs':['wind_new','wind_offshore']}].sum(['techs','timesteps']).to_pandas().T
    tot_vres_prod = pv_prod + wind_prod 
    share_pv = pv_prod / tot_vres_prod.sum()
    share_wind = wind_prod / tot_vres_prod.sum()
    shannon_index = pd.DataFrame(index=tot_vres_prod.index, columns=['Shannon_index'])
    for r in tot_vres_prod.index:
        shannon_index.loc[r] = max(0,(-share_pv.loc[r].values[0] * np.log(share_pv.loc[r].values[0]))) + max(0,(-share_wind.loc[r].values[0] * np.log(share_wind.loc[r].values[0])))
    shannon_index = shannon_index.sum()
    
    return(shannon_index)

def tot_vres_prod(model):
    pv_prod = model.get_formatted_array('carrier_prod').loc[{'techs':['pv_farm','pv_rooftop','pv_farm_new','pv_rooftop_new']}].sum(['techs','timesteps']).to_pandas().T
    wind_prod = model.get_formatted_array('carrier_prod').loc[{'techs':['wind','wind_new','wind_offshore']}].sum(['techs','timesteps']).to_pandas().T
    tot_vres_prod = pv_prod + wind_prod
   
    return(tot_vres_prod)
   
config_name = 'test'
os.chdir('NetCDFs/%s' %config_name)
techs=['inter_zonal_new:NORD','inter_zonal_new:CNOR','inter_zonal_new:CSUD','inter_zonal_new:SUD','inter_zonal_new:SARD','inter_zonal_new:SICI',
       'wind_offshore','wind_new','pv_farm_new','pv_rooftop_new','phs','phs_new','wind','pv_farm','pv_rooftop','ccgt','coal','coal_usc','oil_&_other','battery',
       'inter_zonal:NORD','inter_zonal:CNOR','inter_zonal:CSUD','inter_zonal:SUD','inter_zonal:SARD','inter_zonal:SICI']
techs_new = ['inter_zonal_new:NORD','inter_zonal_new:CNOR','inter_zonal_new:CSUD','inter_zonal_new:SUD','inter_zonal_new:SARD','inter_zonal_new:SICI',
       'wind_offshore','wind_new','pv_farm_new','pv_rooftop_new','phs_new','battery']

#%%
'''
Reading Iterations 0 and 1
'''
#model = calliope.read_netcdf('NetCDFs/results_0.nc')
#model.run(build_only=True, force_rerun=True)
model_0 = calliope.read_netcdf('results_0.nc')
model_1 = calliope.read_netcdf('results_1.nc')

'''
Extrapolation of relevant indicators
'''
#Cost class
costs_0 =  model_0.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()
costs_1 =  model_1.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()
cost_list.append(costs_0)
cost_list.append(costs_1)

#CO2 class
co2_0 = model_0.get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()
co2_1 = model_1.get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()
co2_list.append(co2_0)
co2_list.append(co2_1)

'''
Creation and saving of a list of slacked neighbourhoods of the optimal cost of Iteration 0
'''
slacked_costs_list = slacks*costs_0 
slacked_costs = {'max_cost1': slacked_costs_list[0], 'max_cost5': slacked_costs_list[1], 'max_cost10': slacked_costs_list[2]}

cap_loc_score_1 = cap_loc_score(model_1,model_0,techs=techs)

#%%
'''
Reading near-optimal n-th iterations
'''

'''
Creation of variables to store the NOS results
'''
nos_dict = {}
nos_dict[0] = model_0
nos_dict[1] = model_1
cap_per_loc_dict = {}
cap_loc_score_dict = {}
incremental_score = {}

cap_loc_score_dict[1] = cap_loc_score(nos_dict[1],model_0,techs=techs)
incremental_score[1] = cap_loc_score_dict[1]
cap_per_loc_dict[1] = cap_loc_calc(nos_dict[1])

'''
Reading form netCDFs
'''
n = 100
for j in range(2,(n+1)):
    try:
        nos_dict[j] = calliope.read_netcdf('results_nos_%d.nc' % j)
    except:
        break
    cap_loc_score_dict[j] = cap_loc_score(nos_dict[j],model_0,techs=techs)
    incremental_score[j] = cap_loc_score_dict[j].add(incremental_score[j-1])
    cap_per_loc_dict[j] = cap_loc_calc(nos_dict[j])

    cost_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas())
    co2_list.append(nos_dict[j].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas())

#%%
'''
Relevant indicators
'''

curtailment = {}
import_el = {}
export_el = {}
cap_per_loc_dict = {}
cap_per_loc_vres_dict = {}
cap_loc_score_simple_dict_0 = {}
cap_loc_score_supersimple_dict_0 = {}
cumulated_simple_score_0 =  {}
cumulated_simple_score_0[0] = cap_loc_score(nos_dict[0],nos_dict[0])
cumulated_supersimple_score_0 =  {}
cumulated_supersimple_score_0[0] = cap_loc_score(nos_dict[0],nos_dict[0])
curt_exp_vresshare_dict = {}

scoring_method = cap_loc_score_pure
for m in range(len(nos_dict)):
    curtailment[m] = nos_dict[m].get_formatted_array('carrier_con').loc[{'techs':'el_curtailment','carriers':'electricity'}].sum(['locs','timesteps']).to_pandas().T
    import_el[m] = nos_dict[m].get_formatted_array('carrier_prod').loc[{'techs':'el_import','carriers':'electricity'}].sum(['locs','timesteps']).to_pandas().T
    export_el[m] = nos_dict[m].get_formatted_array('carrier_con').loc[{'techs':'el_export','carriers':'electricity'}].sum(['locs','timesteps']).to_pandas().T
    cap_loc_score_simple_dict_0[m] = scoring_method(nos_dict[m],nos_dict[0])
    cap_loc_score_supersimple_dict_0[m] = cap_loc_score_simple(nos_dict[m],nos_dict[0])
    cap_per_loc_dict[m] = regionwide_simple_score(cap_loc_calc(nos_dict[m], i=techs))
    cap_per_loc_vres_dict[m] = cap_loc_calc(nos_dict[m], i=['wind_offshore','wind_new','pv_farm_new','pv_rooftop_new','phs_new','battery'])
    cap_per_loc_vres_dict[m]['pv_new'] = cap_per_loc_vres_dict[m][['pv_farm_new','pv_rooftop_new']].sum(axis=1)
    cap_per_loc_vres_dict[m] = cap_per_loc_vres_dict[m].drop(['pv_farm_new','pv_rooftop_new'], axis=1)
    cap_per_loc_vres_dict[m] = cap_per_loc_vres_dict[m].drop(['NORD','CNOR','CSUD','SUD'], axis=0)
    curt_exp_vresshare_dict[m] = curt_exp_vresshare(nos_dict[m])
    
frequency_dict = {}
for t in techs:
    frequency_dict[t] = (cap_per_loc_dict[0][t]-cap_per_loc_dict[0][t]).to_frame(name='0')
for m in range(1,len(nos_dict)):
    for t in techs:
        frequency_dict[t] = frequency_dict[t].join((cap_per_loc_dict[m][t]-cap_per_loc_dict[0][t]).to_frame(name='%d' %m))
        
for m in range(1,len(nos_dict)):
    cumulated_simple_score_0[m] = cumulated_simple_score_0[m-1].add(cap_loc_score_simple_dict_0[m]) 
    cumulated_supersimple_score_0[m] = cumulated_supersimple_score_0[m-1].add(cap_loc_score_supersimple_dict_0[m])

frequency_vres_dict = {}
for t in ['wind_offshore','wind_new','pv_new','phs_new','battery']:
    frequency_vres_dict[t] = (cap_per_loc_vres_dict[0][t]).to_frame(name='0')
for m in range(1,len(nos_dict)):
    for t in ['wind_offshore','wind_new','pv_new','phs_new','battery']:
        frequency_vres_dict[t] = frequency_vres_dict[t].join((cap_per_loc_vres_dict[m][t]).to_frame(name='%d' %m))


cap_per_loc_vres_min = cap_loc_calc_min(nos_dict[0], i=['wind_offshore','wind_new','pv_farm_new','pv_rooftop_new','phs_new','battery'])
cap_per_loc_vres_min['pv_new'] = cap_per_loc_vres_min[['pv_farm_new','pv_rooftop_new']].sum(axis=1)
cap_per_loc_vres_min = cap_per_loc_vres_min.drop(['pv_farm_new','pv_rooftop_new'], axis=1)
cap_per_loc_vres_min = cap_per_loc_vres_min.drop(['NORD','CNOR','CSUD','SUD'], axis=0)
frequency_vres_min_dict = {}
for t in ['wind_offshore','wind_new','pv_new', 'phs_new', 'battery']:
    frequency_vres_min_dict[t] = (cap_per_loc_vres_min[t]).to_frame(name='min')
frequency_vres_min_dict['battery'][:] = 0
frequency_vres_min_dict['phs_new'][:] = 0

    #%% Second stage of post-processing
'''
Generating summary tables
'''

summary_table = pd.DataFrame(index=range(len(nos_dict)),columns=['wind_cap', 'wind_offshore_cap', 'pv_cap', 'tot_vres_cap', 'fossil_dispatchable_cap', 'battery_cap', 'phs_cap', 'transmission_cap', 'vres_prod_share', 'vres_prod_curtailment_fraction', 'export_import_ratio', 'locs_new_vres', 'vres_diversity', 'vres_new_diversity', 'cost', 'co2'])
for m in range(len(nos_dict)):
        summary_table['wind_cap'].loc[m] = (cap_per_loc_dict[m][['wind','wind_new']].sum(axis=1).sum(axis=0))/1e6
        summary_table['wind_offshore_cap'].loc[m] = (cap_per_loc_dict[m][['wind_offshore']].sum(axis=1).sum(axis=0))/1e6
        summary_table['pv_cap'].loc[m] = float(cap_per_loc_dict[m][['pv_rooftop','pv_farm','pv_rooftop_new','pv_farm_new']].sum(axis=1).sum(axis=0))/1e6
        summary_table['tot_vres_cap'].loc[m] =  summary_table['wind_cap'].loc[m] + summary_table['wind_offshore_cap'].loc[m] + summary_table['pv_cap'].loc[m]
        summary_table['fossil_dispatchable_cap'].loc[m] = float(cap_per_loc_dict[m][['ccgt','coal','coal_usc','oil_&_other']].sum(axis=1).sum(axis=0))/1e6
        summary_table['battery_cap'].loc[m] = float(cap_per_loc_dict[m]['battery'].sum(axis=0))/1e6
        summary_table['phs_cap'].loc[m] = float(cap_per_loc_dict[m][['phs','phs_new']].sum(axis=1).sum(axis=0))/1e6
        summary_table['transmission_cap'].loc[m] = float(cap_per_loc_dict[m][['inter_zonal:NORD','inter_zonal:CNOR','inter_zonal:CSUD','inter_zonal:SUD','inter_zonal:SARD','inter_zonal:SICI','inter_zonal_new:NORD','inter_zonal_new:CNOR','inter_zonal_new:CSUD','inter_zonal_new:SUD','inter_zonal_new:SARD','inter_zonal_new:SICI']].sum(axis=1).sum(axis=0))/2/1e6
        summary_table['vres_prod_share'].loc[m] = (curt_exp_vresshare_dict[m]['vres_share']).values[0]*100
        summary_table['vres_prod_curtailment_fraction'].loc[m] = ( (curt_exp_vresshare_dict[m]['el_curtailment']).values[0] / tot_vres_prod(nos_dict[m]).sum().values[0] ) *100
        summary_table['export_import_ratio'].loc[m] = ( (curt_exp_vresshare_dict[m]['el_export']) / (curt_exp_vresshare_dict[m]['el_import']) ).values[0]
        summary_table['locs_new_vres'].loc[m] = (cap_per_loc_vres_dict[m] - cap_per_loc_vres_dict[0])[['wind_offshore','wind_new','pv_new']].astype(bool).sum(axis=0).sum()
        summary_table['vres_diversity'].loc[m] = (vres_shannon_index(nos_dict[m]).values[0])
        summary_table['vres_new_diversity'].loc[m] = (vres_new_shannon_index(nos_dict[m],nos_dict[0]).values[0])
        summary_table['cost'].loc[m] = nos_dict[m].get_formatted_array('cost').loc[{'costs': 'monetary'}].sum(['locs','techs']).to_pandas()/1e6
        summary_table['co2'].loc[m] = nos_dict[m].get_formatted_array('cost').loc[{'costs': 'co2'}].sum(['locs','techs']).to_pandas()/1e6
summary_table.to_csv('H:/Lombardi/ETH - Calliope/v.0.18 - off-shore and more/Pics/%s/summary_table.csv' %config_name)

n = config_name
os.chdir('H:/Lombardi/ETH - Calliope/v.0.18 - off-shore and more/Pics/%s' %n)
summary_table = pd.read_csv('summary_table.csv')
summary_table = summary_table.drop(['Unnamed: 0'], axis=1)

largest_labels = ['wind_offshore_cap', 'wind_cap', 'pv_cap', 'tot_vres_cap', 'battery_cap', 'transmission_cap', 'vres_prod_share', 'vres_prod_curtailment_fraction', 'export_import_ratio', 'locs_new_vres', 'vres_diversity', 'vres_new_diversity']
smallest_labels = ['fossil_dispatchable_cap']
best_dict = {}

for l in largest_labels:
    best_dict[l] = summary_table[l].nlargest(n=1).index.values
for s in smallest_labels:
    best_dict[s] = summary_table[s].nsmallest(n=1).index.values

indexes_set = set()
for k in best_dict:
    indexes_set = indexes_set | set(best_dict[k])
indexes_list = list(indexes_set)

cleaned_up_summary_table = summary_table.loc[indexes_list]
cleaned_up_summary_table.to_csv('clean_summary.csv')

titles_list = []
for i in indexes_list:
    for k,v in best_dict.items():
        if i in v:
            titles_list.append((i,k))
    
#%% Plotting scatter of wind and pv
        
#wi = regionwide_simple_score(frequency_vres_dict['wind']/1e6)
#pv = regionwide_simple_score(frequency_vres_dict['pv']/1e6)
##wi = (frequency_vres_dict['wind']/1e6)
##pv = (frequency_vres_dict['pv']/1e6)
#
#regions = wi.index
##cmap_dict = {'NORD': 'Reds_r', 'CNOR': 'Purples_r', 'CSUD': 'Blues_r', 'SUD': 'Greens_r', 'SICI': 'Oranges_r', 'SARD': 'RdPu_r'}
#color_dict = {'NORD': 'r', 'CNOR': 'purple', 'CSUD': 'b', 'SUD': 'cyan', 'SICI': 'orange', 'SARD': 'green'}
###marker_dict = {'NORD': '.', 'CNOR': '^', 'CSUD': 'v', 'SUD': 's', 'SICI': '+', 'SARD': 'x'}
##color_dict = {}
##color_list = ['#8B0000', '#FF0000', '#B22222', '#DC143C', '#F08080', '#FF4500', '#FF8C00', '#FFA500',
##              '#ADFF2F', '#7FFF00', '#00FF00',
##              '#228B22', '#006400', '#3CB371',
##              '#20B2AA', '#48D1CC', '#008B8B', '#191970',
##              '#7B68EE', '#9370DB']
##k = 0
##for r in regions:
##    color_dict[r] = color_list[k]
##    k += 1
#    
#
#fig, ax = plt.subplots(figsize=(10,10))
#
#for r in regions:
#    ax.scatter(wi.loc[r].values,pv.loc[r].values, c=color_dict[r], alpha=0.6)
#    for v in range(len(wi.loc[r].values)):
#        ax.plot((wi.loc[r].values[0],wi.loc[r].values[v]),(pv.loc[r].values[0],pv.loc[r].values[v]), alpha=0.6, color=color_dict[r], linestyle='dotted')
#    ax.annotate(r, (wi['0'].loc[r],pv['0'].loc[r]), xytext=(wi['0'].loc[r]+0.1,pv['0'].loc[r]+0.1))
#ax.set_ylabel('PV installed capacity (GW)')
#ax.set_ylim(top=25)
#ax.set_xlabel('Wind installed capacity (GW)')
#ax.set_xlim(right=25)
#plt.savefig('D:/OneDrive - Politecnico di Milano/ETH - Calliope/v.0.14 - refined transmission cost and no new_ccgt/Pics/%s/scatter_plot.png' %config_name)
#     
#%% Plotting simple bars
#cumulated_simple_cap_plot = regionwide_simple_score(cumulated_simple_score_0[len(nos_dict)-1])/1e+6
#cumulated_simple_score_plot = regionwide_freq_score(frequency_dict,techs)
#
#fig, (ax1, ax2) = plt.subplots(2,1, sharex='col', gridspec_kw = {'height_ratios':[1,0.33], 'wspace':0.2, 'hspace':0.2}, figsize=(12,8))
#
#color_dict = {'wind': '#00E71F',
#             'pv_farm': '#FCCA00', 
#             'pv_rooftop': '#FCF100',
#             'ccgt': '#9E8C8C', 
#             'coal': '#544848', 'coal_usc': '#5A3838',
#             'oil_&_other': '#4F1731',
#             'battery': '#33FFB5', 
#             'inter_zonal:NORD': '#D00045',
#             'inter_zonal:CNOR': '#2A00FC', 
#             'inter_zonal:CSUD': '#A000FC', 
#             'inter_zonal:SUD': '#FD4993', 
#             'inter_zonal:SARD': '#9349FD', 
#             'inter_zonal:SICI': '#496FFD'}
#
#cumulated_simple_cap_plot.plot.bar(color=list(color_dict.values()), alpha=0.8, ax=ax1, width=1)
#cumulated_simple_score_plot.plot.bar(color=list(color_dict.values()), alpha=0.8, ax=ax2, width=1)
#ax1.legend(loc=2, bbox_to_anchor=(1,1.05))
#ax2.legend().remove()
#ax1.set_ylabel('Cumulated installed capacity (GW)')
#ax2.set_ylabel('Frequency of appearance (-)')
#plt.savefig('D:/OneDrive - Politecnico di Milano/ETH - Calliope/v.0.14 - refined transmission cost and no new_ccgt/Pics/%s/bar_plot.png' %config_name)
#     
#%% Plotting heatmaps

fig, ((ax1, ax2, ax3, ax4, ax5, ax6),(ax7, ax8, ax9, ax10, ax17, ax18), (ax11, ax12, ax13, ax14, ax15, ax16)) = plt.subplots(3,6, sharex='col', sharey='row', gridspec_kw = {'height_ratios':[1,1,1], 'wspace':0.2, 'hspace':0.25}, figsize=(20,10))

plot_dict = {}
ax_dict = {'wind_new': ax1,
           'wind_offshore': ax2,
           'pv_farm_new': ax3, 
           'pv_rooftop_new': ax4,
           'battery': ax5,
           'phs_new': ax6,
           'ccgt': ax7,  
           'coal': ax8, 
           'coal_usc': ax9,
           'oil_&_other': ax10,
           'inter_zonal_new:NORD': ax11,
           'inter_zonal_new:CNOR': ax12, 
           'inter_zonal_new:CSUD': ax13, 
           'inter_zonal_new:SUD': ax14, 
           'inter_zonal_new:SARD': ax15, 
           'inter_zonal_new:SICI': ax16}

cmap_dict = {'wind_new': 'Greens',
             'wind_offshore': 'Greens',
             'pv_farm_new': 'OrRd', 
             'pv_rooftop_new': 'OrRd',
             'ccgt': 'PRGn_r',  
             'coal': 'PRGn_r', 
             'coal_usc': 'PRGn_r',
             'oil_&_other': 'PRGn_r',
             'battery': 'Blues', 
             'phs_new': 'Blues',
             'inter_zonal_new:NORD': 'Purples',
             'inter_zonal_new:CNOR': 'Purples', 
             'inter_zonal_new:CSUD': 'Purples', 
             'inter_zonal_new:SUD': 'Purples', 
             'inter_zonal_new:SARD': 'Purples', 
             'inter_zonal_new:SICI': 'Purples'}

vmax = {'wind_new': 10,
        'wind_offshore': 10,
        'pv_farm_new': 10, 
        'pv_rooftop_new': 10,
        'ccgt': 10,  
        'coal': 10, 
        'coal_usc': 10,
        'oil_&_other': 10,
        'battery': 10, 
        'phs_new': 1,
        'inter_zonal_new:NORD': 4,
        'inter_zonal_new:CNOR': 4, 
        'inter_zonal_new:CSUD': 4, 
        'inter_zonal_new:SUD': 4, 
        'inter_zonal_new:SARD': 4, 
        'inter_zonal_new:SICI': 4}

vmin = {'wind_new': 0,
        'wind_offshore': 0, 
        'pv_farm_new': 0, 
        'pv_rooftop_new': 0,
        'ccgt': -10,  
        'coal': -10, 
        'coal_usc': -10,
        'oil_&_other': -10,
        'battery': 0, 
        'phs_new': 0,
        'inter_zonal_new:NORD': 0,
        'inter_zonal_new:CNOR': 0, 
        'inter_zonal_new:CSUD': 0, 
        'inter_zonal_new:SUD': 0, 
        'inter_zonal_new:SARD': 0, 
        'inter_zonal_new:SICI': 0}

cbar_dict = {}

techs_heatmap=['inter_zonal_new:NORD','inter_zonal_new:CNOR','inter_zonal_new:CSUD','inter_zonal_new:SUD','inter_zonal_new:SARD','inter_zonal_new:SICI',
       'wind_offshore','wind_new','pv_farm_new','pv_rooftop_new','phs_new','ccgt','coal','coal_usc','oil_&_other','battery']

k = 0
for t in techs_heatmap:
    k += 1
    if np.isin(k,[1,2,3,4,5,6,10,16]):
        plot_dict[t] = sns.heatmap(frequency_dict[t].T/1e+6, cmap=cmap_dict[t], ax=ax_dict[t], vmin=vmin[t], vmax=vmax[t])
    else:
        plot_dict[t] = sns.heatmap(frequency_dict[t].T/1e+6, cmap=cmap_dict[t], ax=ax_dict[t], vmin=vmin[t], vmax=vmax[t], cbar=False)
    ax_dict[t].invert_yaxis()
    ax_dict[t].set_title('%s' %t, weight='bold')
ax17.axis('off')
ax18.axis('off')
#fig.savefig('D:/OneDrive - Politecnico di Milano/ETH - Calliope/v.0.14 - refined transmission cost and no new_ccgt/Pics/%s/heatmaps_plot.png' %config_name)
     

#%% Choropleth map

os.chdir(r'H:\Lombardi\ETH - Calliope\v.0.18 - off-shore and more')

max_y = []
for i in curt_exp_vresshare_dict:
    max_y.append(max(curt_exp_vresshare_dict[i][['el_export','el_curtailment']].values))

max_y = np.max(max_y)

for nos in indexes_list:
    nos_number = nos
    nos_string = ('%d' %nos_number)
    
    regions_geo = f'regioni.geojson'
    regions_pv = (frequency_vres_dict['pv_new'][nos_string] - frequency_vres_min_dict['pv_new']['min']).to_frame()/1e+6
    regions_pv.columns = [nos_string]
    regions_wind = (frequency_vres_dict['wind_new'][nos_string] - frequency_vres_min_dict['wind_new']['min']).to_frame()/1e+6
    regions_wind.columns = [nos_string]
    regions_wind_off = (frequency_vres_dict['wind_offshore'][nos_string] - frequency_vres_min_dict['wind_offshore']['min']).to_frame()/1e+6
    regions_wind_off = regions_wind_off.fillna(value=0)
    regions_wind_off.columns = [nos_string]
    regions_bat = (frequency_vres_dict['battery'][nos_string] - frequency_vres_min_dict['battery']['min']).to_frame()/1e+6
    regions_bat.columns = [nos_string]
    
    lista_regioni = ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11','R12','R13','R15','R14','R16','R17','R18','SICI','SARD']
    
    map_df = gpd.read_file(regions_geo)
    map_df['NOME_REG'] = lista_regioni
    merged_pv = map_df.set_index('NOME_REG').join(regions_pv)
    merged_wind = map_df.set_index('NOME_REG').join(regions_wind)
    merged_wind_off = map_df.set_index('NOME_REG').join(regions_wind_off)
    merged_bat = map_df.set_index('NOME_REG').join(regions_bat)
    
    suppl_info = curt_exp_vresshare_dict[nos]
    
    vmin, vmax = 0, 50
    
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1,4, sharey='row', gridspec_kw = {'height_ratios':[1], 'wspace':0.2, 'hspace':0.25}, figsize=(12,6))
    
    or_reds = plt.cm.get_cmap('OrRd', 10)
    greens = plt.cm.get_cmap('Greens', 10)
    greens_off = plt.cm.get_cmap('GnBu', 10)
    blues = plt.cm.get_cmap('Blues', 10)
            
    merged_pv.plot(column=nos_string, cmap=or_reds, vmax=vmax, linewidth=0.8, ax=ax1, edgecolor='0.6')
    merged_wind.plot(column=nos_string, cmap=greens, vmax=20, linewidth=0.8, ax=ax2, edgecolor='0.6')
    merged_wind_off.plot(column=nos_string, cmap=greens_off, vmax=20, linewidth=0.8, ax=ax3, edgecolor='0.6')
    merged_bat.plot(column=nos_string, cmap=blues, vmax=10, linewidth=0.8, ax=ax4, edgecolor='0.6')
    
#    sm_pv = plt.cm.ScalarMappable(cmap=or_reds, norm=plt.Normalize(vmin=vmin, vmax=vmax))
#    sm_wind = plt.cm.ScalarMappable(cmap=greens, norm=plt.Normalize(vmin=vmin, vmax=vmax))
#    sm_bat = plt.cm.ScalarMappable(cmap=blues, norm=plt.Normalize(vmin=vmin, vmax=10))
#    cbar = fig.colorbar(sm_pv, ax=ax1, fraction=0.045, pad=0.04)
#    cbar = fig.colorbar(sm_wind, ax=ax2, fraction=0.045, pad=0.04)
#    cbar = fig.colorbar(sm_bat, ax=ax3, fraction=0.045, pad=0.04)
    
    ax1.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    ax2.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    ax3.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    ax4.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
        
    fig_titles = []
    fig_index = []
    for t in titles_list:
        if nos in t:
            fig_titles.append(t[1])
            fig_index.append(t[0])
    fig.suptitle(('%s ' % fig_index[0] + '%s' %fig_titles), y=0.8)
    fig.tight_layout()
#    plt.savefig(r'H:\Lombardi\ETH - Calliope\v.0.17 - relaxed vres constraints\Pics\test' %(config_name,nos))
     
    
#    fig2, (ax4, ax4b) = plt.subplots(1,2, gridspec_kw = {'width_ratios':[1,0.5], 'wspace':0.3, 'hspace':0.25}, figsize=(3,3))
#        
#    ax4.bar(['curtailment','export'],suppl_info[['el_curtailment','el_export']].values[0]/1e+6, color=['r','b'], alpha=0.5, width=1)
#    ax4b.bar(['vres share'],suppl_info['vres_share'].values[0]*100, color=['g'], alpha=0.5, width=1)
#    ax4.set_ylabel('(GWh)')
#    ax4.set_ylim(top=max_y/1e+6)
#    ax4b.yaxis.tick_right()
#    ax4b.set_ylabel('(%)')  
#    ax4b.yaxis.set_label_position('right')
#    ax4b.set_ylim(top=100)
#    
#    fig2.suptitle(fig_titles, y=1.1)
#    fig2.tight_layout()
    
#    plt.savefig(r'H:\Lombardi\ETH - Calliope\v.0.17 - relaxed vres constraints\Pics\test' %(config_name,nos))
    
    start = '2015-12-15'# 00:00:00'
    stop = '2015-12-20'# 23:00:00'
    power_plot(nos_dict[nos],start,stop)
    
#    plt.savefig('D:/OneDrive - Politecnico di Milano/ETH - Calliope/v.0.14 - refined transmission cost and no new_ccgt/Pics/%s/nos_%s_zdisp.png' %(config_name,nos))
   
#%%
'''
Plotting the operation
'''
#start = '2015-03-30 00:00:00'
#stop = '2015-04-05 23:00:00'
##
#power_plot(model_0,start,stop)
#horizontal_loc_cap_plot(cap_loc_calc(model_0))
#power_plot(model_1,start,stop)
#horizontal_loc_cap_plot(cap_loc_calc(model_1))
#    
#for j in range(2,(n+1)):
#    power_plot(nos_dict[j],start,stop)
##    per_loc_cap_plot(cap_per_loc_dict[j])
#    horizontal_loc_cap_plot(cap_per_loc_dict[j])
#for jj in range(2,(m+1)):
#    power_plot(nos_dict_2[jj],start,stop)
##    per_loc_cap_plot(cap_per_loc_dict[j])
#    horizontal_loc_cap_plot(cap_per_loc_dict_2[jj]) 

'''
Performing deeper comparisons about installed caps in each loc
'''
#vres_diff_list = []
#for j in range(2,(n+1)):
#    vres_diff_list.append(vres_diff_per_loc(nos_dict[j],nos_dict[j-1]))
