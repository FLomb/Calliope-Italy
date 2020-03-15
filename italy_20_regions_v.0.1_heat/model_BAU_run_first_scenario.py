# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 11:23:25 2020

@author: enrico
"""
#%% Initialisation

import calliope
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from dispatch_plots_first_scenario import power_plot
from dispatch_plots_first_scenario import heat_only_DHW_plot
from dispatch_plots_first_scenario import heat_DHW_plot
from dispatch_plots_first_scenario import heat_SH_plot
#from dispatch_plots_first_scenario import operatività_pompe_di_calore

p2h_size_only_DHW = pd.read_csv('p2h_size_only_DHW.csv', index_col=0)
p2h_size_primo_scenario = pd.read_csv('p2h_size_scenario_DHW_and_floor_heating.csv', index_col=0)
os.chdir('calliope_model')
calliope.set_log_verbosity('INFO') #sets the level of verbosity of Calliope's operations

calliope_columns = ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10',
                    'R11','R12','R13','R14','R15','R16','R17','R18','SICI','SARD']

start = '2015-01-01 00:00:00'
stop = '2015-01-07 23:59:00'

#%% model creation and run

model_base = calliope.Model('model.yaml') 
model_base.run()

# model = calliope.Model('model.yaml', scenario='p2h_dlc_only_DHW')
# model.run(build_only=True)

# for reg in calliope_columns:
#     model.backend.update_param('energy_cap_equals', {'%s::ashp_DHW' %reg : p2h_size_only_DHW.loc[reg]['hp'] })
#     model.backend.update_param('energy_cap_equals', {'%s::tes_DHW' %reg : p2h_size_only_DHW.loc[reg]['hp']})
#     model.backend.update_param('storage_cap_equals', {'%s::tes_DHW' %reg : p2h_size_only_DHW.loc[reg]['tes']})

# model_p2h_dlc_only_DHW = model.backend.rerun()

model = calliope.Model('model.yaml', scenario='p2h_dlc_DHW_and_floor_heating')
model.run(build_only=True)

for reg in calliope_columns:
    model.backend.update_param('energy_cap_equals', {'%s::ashp_DHW' %reg : p2h_size_primo_scenario.loc[reg]['hp_DHW'] })
    model.backend.update_param('energy_cap_equals', {'%s::tes_DHW' %reg : p2h_size_primo_scenario.loc[reg]['hp_DHW']})
    model.backend.update_param('storage_cap_equals', {'%s::tes_DHW' %reg : p2h_size_primo_scenario.loc[reg]['tes_DHW']})
    model.backend.update_param('energy_cap_equals', {'%s::ashp_SH_DHW_floor' %reg : p2h_size_primo_scenario.loc[reg]['hp_SH_DHW_floor'] })
    model.backend.update_param('energy_cap_equals', {'%s::ashp_SH_floor' %reg : p2h_size_primo_scenario.loc[reg]['hp_SH_floor']})
    model.backend.update_param('energy_cap_equals', {'%s::tes_floor_heating' %reg : p2h_size_primo_scenario.loc[reg]['tes_floor_energy_cap']})
    model.backend.update_param('storage_cap_equals', {'%s::tes_floor_heating' %reg : p2h_size_primo_scenario.loc[reg]['tes_floor_heating']})

model_p2h_dlc_DHW_and_floor_heating = model.backend.rerun()

#%% plotting

power_plot (model_base,start,stop)
#power_plot(model_p2h_dlc_only_DHW,start,stop)
power_plot(model_p2h_dlc_DHW_and_floor_heating,start,stop)

#heat_only_DHW_plot(model_p2h_dlc_only_DHW,start,stop,'R1')
heat_DHW_plot(model_p2h_dlc_DHW_and_floor_heating,start,stop,'R3')
heat_SH_plot(model_p2h_dlc_DHW_and_floor_heating,start,stop,'R1')
#operatività_pompe_di_calore(model_p2h_dlc_DHW_and_floor_heating,start,stop,'R3')

#%% quantification Hydro effects

def Power_output (model_inst, start, stop):
    
    locs_dict = {}
    
    locs_dict['NORD'] = ['NORD','R1','R2','R3','R4','R5','R6','R7','R8']
    locs_dict['CNOR'] = ['CNOR','R9','R10','R11']
    locs_dict['CSUD'] = ['CSUD','R12','R13','R14']
    locs_dict['SUD'] = ['SUD','R15','R16','R17','R18']
    locs_dict['SICI'] = ['SICI']
    locs_dict['SARD'] = ['SARD']
    
    hydro_dam_dict = {}
    hydro_ror_dict = {}
    pv_dict = {}
    wind_dict = {}
    ccgt_dict = {}
    coal_dict = {}
    oil_dict = {}
    bioenergy_dict = {}
    geothermal_dict = {}
    
    for zone in locs_dict.keys():
        
        ccgt_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'ccgt','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        coal_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['coal','coal_usc'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        oil_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'oil_&_other','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        bioenergy_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['biomass_wood','biofuel','biogas','wte'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        geothermal_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'geothermal','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        pv_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['pv_rooftop','pv_farm'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        wind_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['wind'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        hydro_dam_dict[zone]=model_base.get_formatted_array('carrier_prod').loc[{'techs':'hydro_dam','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        hydro_ror_dict[zone]=model_base.get_formatted_array('carrier_prod').loc[{'techs':'hydro_ror','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        #hydro_dam = hydro_dam_dict[zone].sum()
        #hydro_ror = hydro_ror_dict[zone].sum()
    
    return (hydro_dam_dict, hydro_ror_dict, pv_dict, wind_dict, ccgt_dict, coal_dict, oil_dict, bioenergy_dict, geothermal_dict)

Power_output_tuple = Power_output(model_base,start,stop)

dates = pd.date_range(start=start, end=stop, freq = 'H')
regions = ['NORD', 'CNOR', 'CSUD', 'SUD', 'SICI', 'SARD']
Power_production = pd.DataFrame(index=['hydro_dam','hydro_ror','pv','wind','ccgt','coal','oil','bioenergy','geothermal'],columns=regions)

for r in regions:
    Power_production.loc['hydro_dam'][r]=Power_output_tuple[0][r].sum()/(1e6)
    Power_production.loc['hydro_ror'][r]=Power_output_tuple[1][r].sum()/(1e6)
    Power_production.loc['pv'][r]=Power_output_tuple[2][r].sum()/(1e6)
    Power_production.loc['wind'][r]=Power_output_tuple[3][r].sum()/(1e6)
    Power_production.loc['ccgt'][r]=Power_output_tuple[4][r].sum()/(1e6)
    Power_production.loc['coal'][r]=Power_output_tuple[5][r].sum()/(1e6)
    Power_production.loc['oil'][r]=Power_output_tuple[6][r].sum()/(1e6)
    Power_production.loc['bioenergy'][r]=Power_output_tuple[7][r].sum()/(1e6)
    Power_production.loc['geothermal'][r]=Power_output_tuple[8][r].sum()/(1e6)
    
print(Power_production)

#%% 
# Quantifying P2H effects
###

def impact_metrics(model_base, model_inst, start, stop):
    # variable_costs = model_inst.get_formatted_array('cost_var').loc[{'costs':'monetary'}].sum(['locs','techs','timesteps']).to_pandas()
    # variable_costs_base = model_base.get_formatted_array('cost_var').loc[{'costs':'monetary'}].sum(['locs','techs','timesteps']).to_pandas()
    curtailment = model_inst.get_formatted_array('carrier_con').loc[{'carriers':'electricity','techs':'el_curtailment'}].sum(['locs','timesteps']).to_pandas()

    supply_techs = ['biofuel','biogas','biomass_wood','ccgt','coal','coal_usc','el_import','geothermal','hydro_dam','hydro_ror','oil_&_other','phs','pv_farm','pv_rooftop','wind','wte']
    el_prod_base = model_base.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':supply_techs}].sum(['locs','timesteps']).to_pandas().T 
    el_prod_p2h = model_inst.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':supply_techs}].sum(['locs','timesteps']).to_pandas().T 
    diff_el_prod = el_prod_p2h - el_prod_base
    eff_powerpl = model_base.get_formatted_array('energy_eff').loc[{'techs':supply_techs}].to_pandas().T.mean(axis=1).fillna(1)

    # if model_inst.model_config['name'] == model_p2h_dlc_only_DHW.model_config['name']:
    #     heat_demand = (-pd.read_csv('timeseries_data/demand_regions_heating_DHW_only.csv', index_col=0)).fillna(0).loc[start:stop].sum().sum()
    # else:
    #     heat_demand = (-pd.read_csv('timeseries_data/demand_regions_heating_DHW_only.csv', index_col=0)-pd.read_csv('timeseries_data/demand_regions_heating_floor.csv', index_col=0)).fillna(0).loc[start:stop].sum().sum()
    heat_demand = (-pd.read_csv('timeseries_data/demand_regions_heating_DHW_only.csv', index_col=0)-pd.read_csv('timeseries_data/demand_regions_heating_floor.csv', index_col=0)).fillna(0).loc[start:stop].sum().sum()    
    el_boilers_demand = (-pd.read_csv('timeseries_data/demand_zones_terna.csv', index_col=0)+pd.read_csv('timeseries_data/demand_zones_noboiler.csv', index_col=0)).fillna(0).loc[start:stop].sum().sum()
    only_gas_substitution = heat_demand-el_boilers_demand
    if model_inst.model_config['name'] == model_base.model_config['name']:
        gas_saving = 0
    else:
        gas_saving = only_gas_substitution/0.81 # average boilers efficiency
    delta_primary_en_power = (np.divide(diff_el_prod,eff_powerpl))
    
    delta_tpes = gas_saving - delta_primary_en_power.sum() #kWh
    
    ramp_base = {}
    ramp_p2h = {}
    ramping_techs = ['ccgt','coal','coal_usc','oil_&_other']
    ramp_costs = {'ccgt': 87.1, 'coal': 211.3, 'coal_usc': 92.8, 'oil_&_other': 87.1}
    for rt in ramping_techs:
        ramp_base[rt] = model_base.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':rt}].to_pandas().dropna()
        ramp_p2h[rt] = model_inst.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':rt}].to_pandas().dropna()
        cum_ramp = 0
        cum_ramp_p2h = 0
        for t in range(len(ramp_base[rt].columns[1:])):
            cum_ramp += abs(ramp_base[rt].iloc[:,t]-ramp_base[rt].iloc[:,t-1])
            cum_ramp_p2h += abs(ramp_p2h[rt].iloc[:,t]-ramp_p2h[rt].iloc[:,t-1])
        ramp_base[rt] = cum_ramp.sum()*ramp_costs[rt]/1e3
        ramp_p2h[rt] = cum_ramp_p2h.sum()*ramp_costs[rt]/1e3  
    
    tot_ramping_cost_p2h = sum(ramp_p2h.values())
    tot_ramping_cost_base = sum(ramp_base.values())
    delta_ramping_costs = (tot_ramping_cost_p2h - tot_ramping_cost_base)/tot_ramping_cost_base*100
    
    return(delta_ramping_costs,curtailment,delta_tpes)

metrics = {}
metrics['base'] = impact_metrics(model_base, model_base, start, stop)
#metrics['dlc_only_DHW'] = impact_metrics(model_base, model_p2h_dlc_only_DHW, start, stop)
metrics['DHW_SH_floor'] = impact_metrics(model_base, model_p2h_dlc_DHW_and_floor_heating, start, stop)

#%%
# Quantifying costs
###

def impact_costs (model_base,model_inst,start,stop):
    costs = model_inst.get_formatted_array('cost').loc[{'costs':'monetary'}].sum(['locs','techs']).to_pandas()
    costs_base = model_base.get_formatted_array('cost').loc[{'costs':'monetary'}].sum(['locs','techs']).to_pandas()
    delta_costs = costs - costs_base

    variable_costs = model_inst.get_formatted_array('cost_var').loc[{'costs':'monetary'}].sum(['locs','techs','timesteps']).to_pandas()
    variable_costs_base = model_base.get_formatted_array('cost_var').loc[{'costs':'monetary'}].sum(['locs','techs','timesteps']).to_pandas()
    delta_variable_costs = variable_costs - variable_costs_base
    
    costs_co2 = model_inst.get_formatted_array('cost').loc[{'costs':'co2'}].sum(['locs','techs']).to_pandas()
    costs_co2_base = model_base.get_formatted_array('cost').loc[{'costs':'co2'}].sum(['locs','techs']).to_pandas()
    delta_costs_co2 = costs_co2 - costs_co2_base

    # variable_costs_co2 = model_inst.get_formatted_array('cost_var').loc[{'costs':'co2'}].sum(['locs','techs','timesteps']).to_pandas()
    # variable_costs_co2_base = model_base.get_formatted_array('cost_var').loc[{'costs':'co2'}].sum(['locs','techs','timesteps']).to_pandas()
    # delta_variable_costs_co2 = variable_costs_co2 - variable_costs_co2_base
    
    investment_costs = model_inst.get_formatted_array('cost_investment').loc[{'costs':'monetary'}].sum(['locs','techs']).to_pandas()
    investment_costs_base = model_base.get_formatted_array('cost_investment').loc[{'costs':'monetary'}].sum(['locs','techs']).to_pandas()
    delta_investment_costs = investment_costs - investment_costs_base
    
    return(delta_costs,delta_variable_costs,delta_costs_co2,delta_investment_costs)

costs = {}
costs['base'] = impact_costs(model_base, model_base, start, stop)
#costs['dlc_only_DHW'] = impact_costs(model_base, model_p2h_dlc_only_DHW, start, stop)
costs['DHW_SH_floor'] = impact_costs(model_base, model_p2h_dlc_DHW_and_floor_heating, start, stop)
   
