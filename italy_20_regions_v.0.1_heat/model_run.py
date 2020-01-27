# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 2018

A script to run and post-process the Italy Calliope 20-node model

@author: F.Lombardi
"""
#%% Initialisation
import calliope
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from dispatch_plots import power_plot

p2h_size = pd.read_csv('p2h_size.csv', index_col=0)
os.chdir('calliope_model')
calliope.set_log_verbosity('INFO') #sets the level of verbosity of Calliope's operations

calliope_columns = ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10',
                    'R11','R12','R13','R14','R15','R16','R17','R18','SICI','SARD']
start = '2015-06-15 00:00:00'
stop = '2015-06-21 23:59:00'

#%% Model creation and run
# model_base = calliope.Model('model.yaml') 
# model_base.run()

# model_p2h_tcl = calliope.Model('model.yaml', scenario='p2h_tcl')
# model_p2h_tcl.run()

# model_p2h_pvtcl = calliope.Model('model.yaml', scenario='p2h_pvtcl')
# model_p2h_pvtcl.run()

# model = calliope.Model('model.yaml', scenario='p2h_dlc')
# model.run(build_only=True)
# for reg in calliope_columns:
#     model.backend.update_param('energy_cap_equals', {'%s::ashp' %reg : p2h_size.loc[reg]['hp'] })
#     model.backend.update_param('energy_cap_equals', {'%s::tes' %reg : p2h_size.loc[reg]['hp']})
#     model.backend.update_param('storage_cap_equals', {'%s::tes' %reg : p2h_size.loc[reg]['tes']})

# model_p2h_dlc = model.backend.rerun()

#%% Saving model results to netCDF and to CSVs
# model_base.to_netcdf('NetCDFs/model_base.nc')
# model_p2h_tcl.to_netcdf('NetCDFs/model_p2h_tcl.nc')
# model_p2h_pvtcl.to_netcdf('NetCDFs/model_p2h_pvtcl.nc')
# model_p2h_dlc.to_netcdf('NetCDFs/model_p2h_dlc.nc')

# model_base.to_netcdf('NetCDFs/model_base_summer.nc')
# model_p2h_tcl.to_netcdf('NetCDFs/model_p2h_tcl_summer.nc')
# model_p2h_pvtcl.to_netcdf('NetCDFs/model_p2h_pvtcl_summer.nc')
# model_p2h_dlc.to_netcdf('NetCDFs/model_p2h_dlc_summer.nc')

#%% Alternatively, previously run solutions can be read from netCDF files

# model_base = calliope.read_netcdf('NetCDFs/model_base.nc')
# model_p2h_tcl = calliope.read_netcdf('NetCDFs/model_p2h_tcl.nc')
# model_p2h_pvtcl = calliope.read_netcdf('NetCDFs/model_p2h_pvtcl.nc')
# model_p2h_dlc = calliope.read_netcdf('NetCDFs/model_p2h_dlc.nc')

# model_base = calliope.read_netcdf('NetCDFs/model_base_summer.nc')
# model_p2h_tcl = calliope.read_netcdf('NetCDFs/model_p2h_tcl_summer.nc')
# model_p2h_pvtcl = calliope.read_netcdf('NetCDFs/model_p2h_pvtcl_summer.nc')
model_p2h_dlc = calliope.read_netcdf('NetCDFs/model_p2h_dlc_summer.nc')

#%%
# Plotting
###

# power_plot(model_base,start,stop)
# power_plot(model_p2h_tcl,start,stop)
# power_plot(model_p2h_pvtcl,start,stop)
# power_plot(model_p2h_dlc,start,stop)

# heat_plot(model_p2h_dlc,start,stop,'R9')

#%%
# Quantifying P2H effects
###

# def impact_metrics(model_base, model_inst, start, stop):
#     variable_costs = model_inst.get_formatted_array('cost_var').loc[{'costs':'monetary'}].sum(['locs','techs','timesteps']).to_pandas()
#     variable_costs_base = model_base.get_formatted_array('cost_var').loc[{'costs':'monetary'}].sum(['locs','techs','timesteps']).to_pandas()
#     curtailment = model_inst.get_formatted_array('carrier_con').loc[{'carriers':'electricity','techs':'el_curtailment'}].sum(['locs','timesteps']).to_pandas()

#     supply_techs = ['biofuel','biogas','biomass_wood','ccgt','coal','coal_usc','el_import','geothermal','hydro_dam','hydro_ror','oil_&_other','phs','pv_farm','pv_rooftop','wind','wte']
#     el_prod_base = model_base.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':supply_techs}].sum(['locs','timesteps']).to_pandas().T 
#     el_prod_p2h = model_inst.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':supply_techs}].sum(['locs','timesteps']).to_pandas().T 
#     diff_el_prod = el_prod_p2h - el_prod_base
#     eff_powerpl = model_base.get_formatted_array('energy_eff').loc[{'techs':supply_techs}].to_pandas().T.mean(axis=1).fillna(1)

#     heat_demand = -pd.read_csv('timeseries_data/demand_regions_heat.csv', index_col=0).fillna(0).loc[start:stop].sum().sum()
#     el_boilers_demand = (-pd.read_csv('timeseries_data/demand_zones_terna.csv', index_col=0)+pd.read_csv('timeseries_data/demand_zones_noboil.csv', index_col=0)).fillna(0).loc[start:stop].sum().sum()
#     only_gas_substitution = heat_demand-el_boilers_demand
#     if model_inst.model_config['name'] == model_base.model_config['name']:
#         gas_saving = 0
#     else:
#         gas_saving = only_gas_substitution/0.81
#     delta_primary_en_power = (np.divide(diff_el_prod,eff_powerpl))
    
#     delta_tpes = gas_saving - delta_primary_en_power.sum() #kWh
    
#     ramp_base = {}
#     ramp_p2h = {}
#     ramping_techs = ['ccgt','coal','coal_usc','oil_&_other']
#     ramp_costs = {'ccgt': 87.1, 'coal': 211.3, 'coal_usc': 92.8, 'oil_&_other': 87.1}
#     for rt in ramping_techs:
#         ramp_base[rt] = model_base.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':rt}].to_pandas().dropna()
#         ramp_p2h[rt] = model_inst.get_formatted_array('carrier_prod').loc[{'carriers':'electricity', 'techs':rt}].to_pandas().dropna()
#         cum_ramp = 0
#         cum_ramp_p2h = 0
#         for t in range(len(ramp_base[rt].columns[1:])):
#             cum_ramp += abs(ramp_base[rt].iloc[:,t]-ramp_base[rt].iloc[:,t-1])
#             cum_ramp_p2h += abs(ramp_p2h[rt].iloc[:,t]-ramp_p2h[rt].iloc[:,t-1])
#         ramp_base[rt] = cum_ramp.sum()*ramp_costs[rt]/1e3
#         ramp_p2h[rt] = cum_ramp_p2h.sum()*ramp_costs[rt]/1e3  
    
#     tot_ramping_cost_p2h = sum(ramp_p2h.values())
#     tot_ramping_cost_base = sum(ramp_base.values())
#     delta_ramping_costs = (tot_ramping_cost_p2h - tot_ramping_cost_base)/tot_ramping_cost_base*100
    
#     return(delta_ramping_costs,curtailment,delta_tpes)

# metrics = {}
# metrics['base'] = impact_metrics(model_base, model_base, start, stop)
# metrics['tcl'] = impact_metrics(model_base, model_p2h_tcl, start, stop)
# metrics['pv-tcl'] = impact_metrics(model_base, model_p2h_pvtcl, start, stop)
# metrics['dlc'] = impact_metrics(model_base, model_p2h_dlc, start, stop)


# pv_cap_per_us = model_base.get_formatted_array('energy_cap').loc[{'techs':'pv_rooftop'}].to_pandas().T
# for reg in reg_dict.keys():
#     subset_users = len(regional_prof_matr[reg].columns)
#     pv_cap_per_us[reg_dict[reg]] = pv_cap_per_us[reg_dict[reg]]/(subset_users*100)
# pv_cap_per_us.dropna().to_csv('pv_cap_us.csv')
