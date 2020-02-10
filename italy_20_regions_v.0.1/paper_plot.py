# -*- coding: utf-8 -*-
"""
Created on Mon May 27 11:46:57 2019

Script to generate static dispatch plots, tuned on the specific case of the Italian 20-node model

@author: F.Lombardi
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

#%% 
'''
Multi-node plots pre-processing - Power sector
'''
def paper_plot(model_inst, start, stop):
        
    linestyle_dict = {'R12':'-', 'R13': '--', 'R14': '-.'}
    label_dict = {'R12':'COP-R12', 'R13': 'COP-R13', 'R14': 'COP-R14'}
    
    locs_dict = {}
    
    locs_dict['CSUD'] = ['CSUD','R12','R13','R14']
    
    ccgt_dict = {}
    coal_dict = {}
    oil_dict = {}
    bioenergy_dict = {}
    hydro_dam_dict = {}
    hydro_ror_dict = {}
    pv_dict = {}
    wind_dict = {}
    import_dict = {}
    export_dict = {}
    zonal_import_dict = {}
    zonal_export_dict = {}
    zonal_exp_dict = {}
    zonal_imp_dict = {}
    geothermal_dict = {}
    phs_supply_dict = {}
    phs_charge_dict = {}
    curtailment_dict = {}
    demand_dict = {}
    
    links_dict = {}
    eu_links_dict = {}
    
    links_dict['CSUD'] = ['inter_zonal:CNOR','inter_zonal:SUD','inter_zonal:SARD']
  
    eu_links_dict['CSUD'] = []
    
    geo_plot = {}
    ror_plot = {}
    win_plot = {}
    pv_plot = {}
    hyd_plot = {}
    bio_plot = {}
    imp_plot = {}
    oil_plot = {}
    coa_plot = {}
    gas_plot = {}
    pum_plot = {}
    zon_plot = {}
    pch_plot = {}
    zwx_plot = {}
    exp_plot = {}
    cur_plot = {}
    loa_plot = {}
    
    
    for zone in locs_dict.keys():
        
        ccgt_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'ccgt','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        coal_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['coal','coal_usc'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        oil_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'oil_&_other','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        bioenergy_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['biomass_wood','biofuel','biogas','wte'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        geothermal_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'geothermal','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        hydro_ror_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'hydro_ror','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        hydro_dam_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'hydro_dam','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        phs_supply_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['phs'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T 
        pv_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['pv_rooftop','pv_farm'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        wind_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['wind'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        import_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':eu_links_dict[zone],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        zonal_import_dict[zone] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':links_dict[zone],'carriers':'electricity','locs':locs_dict[zone]}].sum('locs').sum('techs').to_pandas().T 
        zonal_export_dict[zone] = model_inst.get_formatted_array('carrier_con').loc[{'techs':links_dict[zone],'carriers':'electricity','locs':locs_dict[zone]}].sum('locs').sum('techs').to_pandas().T
        export_dict[zone] = model_inst.get_formatted_array('carrier_con').loc[{'techs':eu_links_dict[zone],'carriers':'electricity','locs':locs_dict[zone]}].sum('locs').sum('techs').to_pandas().T
        curtailment_dict[zone] = model_inst.get_formatted_array('carrier_con').loc[{'techs': ['el_curtailment'],'carriers':'electricity','locs':locs_dict[zone]}].sum('locs').sum('techs').to_pandas().T
        demand_dict[zone] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_power','carriers':'electricity','locs':locs_dict[zone]}].sum('locs').to_pandas().T
        phs_charge_dict[zone] = model_inst.get_formatted_array('carrier_con').loc[{'techs':['phs'],'carriers':'electricity','locs':locs_dict[zone]}].sum('techs').sum('locs').to_pandas().T
        zonal_imp_dict[zone] = zonal_export_dict[zone]+zonal_import_dict[zone]
        zonal_imp_dict[zone][zonal_imp_dict[zone]<0]=0
        zonal_exp_dict[zone] = zonal_export_dict[zone]+zonal_import_dict[zone]
        zonal_exp_dict[zone][zonal_exp_dict[zone]>0]=0
        
        geo_plot[zone] = geothermal_dict[zone]/1000000
        ror_plot[zone] = geo_plot[zone] + hydro_ror_dict[zone]/1000000
        win_plot[zone] = ror_plot[zone] + wind_dict[zone]/1000000
        pv_plot[zone] = win_plot[zone] + pv_dict[zone]/1000000 
        hyd_plot[zone] = pv_plot[zone] + hydro_dam_dict[zone]/1000000
        bio_plot[zone] = hyd_plot[zone] + bioenergy_dict[zone]/1000000 
        imp_plot[zone] = bio_plot[zone] + import_dict[zone]/1000000
        oil_plot[zone] = imp_plot[zone] + oil_dict[zone]/1000000
        coa_plot[zone] = oil_plot[zone] + coal_dict[zone]/1000000
        gas_plot[zone] = coa_plot[zone] + ccgt_dict[zone]/1000000
        pum_plot[zone] = gas_plot[zone] + phs_supply_dict[zone]/1000000
        zon_plot[zone] = pum_plot[zone] + zonal_imp_dict[zone]/1000000
        pch_plot[zone] = phs_charge_dict[zone]/1000000
        zwx_plot[zone] = pch_plot[zone] + zonal_exp_dict[zone]/1000000
        exp_plot[zone] = zwx_plot[zone] + export_dict[zone]/1000000
        cur_plot[zone] = exp_plot[zone] + curtailment_dict[zone]/1000000
        loa_plot[zone] = demand_dict[zone]/1000000
        
    locs = ['R12','R13','R14']
    
    hp_dict = {}
    hp_con_dict = {}
    tes_soc_dict = {}
    tes_dis_dict = {}
    tes_ch_dict = {}
    tes_out_dict = {}
    tes_in_dict = {}
    demand_dhw_dict = {}
    cop_dict = {}
    
    hp_plot = {}
    hp_con_plot = {}
    tes_dis_plot = {}
    tes_ch_plot = {}
    demand_dhw_plot = {}
    
    
    for reg in locs:
        cop_dict[reg] = model_inst.get_formatted_array('energy_eff').loc[{'techs':'ashp','locs':reg}].to_pandas().T
        hp_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'ashp','carriers':'dhw','locs':reg}].to_pandas().T
        hp_con_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'ashp','carriers':'electricity','locs':reg}].to_pandas().T
        tes_soc_dict[reg] = model_inst.get_formatted_array('storage').loc[{'techs':'tes','locs':reg}].to_pandas().T
        demand_dhw_dict[reg] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_heat','carriers':'dhw','locs':reg}].to_pandas().T
        tes_dis_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'tes','carriers':'dhw','locs':reg}].to_pandas().T
        tes_ch_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'tes','carriers':'dhw','locs':reg}].to_pandas().T
        tes_out_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_out_dict[reg][tes_out_dict[reg]<0]=0
        tes_in_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_in_dict[reg][tes_in_dict[reg]>0]=0
        
        hp_plot[reg] = hp_dict[reg]/1e6
        hp_con_plot[reg] = -hp_con_dict[reg]/1e6
        tes_dis_plot[reg] = hp_plot[reg] + tes_out_dict[reg]/1e6
        tes_ch_plot[reg] = tes_in_dict[reg]/1e6
        demand_dhw_plot[reg] = demand_dhw_dict[reg]/1e6

    '''
    Power & Heat plots
    '''
    
    day = start #'2015-01-01 00:00:00'
    end = stop #'2015-01-07 23:00:00'
    
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1, sharex='col', gridspec_kw = {'height_ratios':[6,2,2,2,2], 'wspace':0.1, 'hspace':0.25}, figsize=(10,10))
    ax_dict = {'CSUD': ax1, 'R12': ax2, 'R13': ax3, 'R14': ax4}
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter('%m-%d')
    
    for zone in ['CSUD']:

        ax_dict[zone].set_title(zone, weight='bold')
        ax_dict[zone].plot(loa_plot[zone][day:end].index,loa_plot[zone][day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='Baseline load')
        #ax_dict[zone].plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
        ax_dict[zone].plot(geo_plot[zone][day:end].index,geo_plot[zone][day:end].values,'#873737', alpha=0.2)
        ax_dict[zone].plot(ror_plot[zone][day:end].index,ror_plot[zone][day:end].values,'#00AFE7', alpha=0.2)
        ax_dict[zone].plot(win_plot[zone][day:end].index,win_plot[zone][day:end].values,'#00E71F', alpha=0.2)
        ax_dict[zone].plot(pv_plot[zone][day:end].index,pv_plot[zone][day:end].values,'#FCF100', alpha=0.2)
        ax_dict[zone].plot(hyd_plot[zone][day:end].index,hyd_plot[zone][day:end].values,'#196AA2', alpha=0.2)
        ax_dict[zone].plot(bio_plot[zone][day:end].index,bio_plot[zone][day:end].values,'#0D631E', alpha=0.2)
        ax_dict[zone].plot(oil_plot[zone][day:end].index,oil_plot[zone][day:end].values,'#4F1731', alpha=0.2)        
        ax_dict[zone].plot(coa_plot[zone][day:end].index,coa_plot[zone][day:end].values,'#544848', alpha=0.2)
        ax_dict[zone].plot(gas_plot[zone][day:end].index,gas_plot[zone][day:end].values,'#9E8C8C', alpha=0.2)
        ax_dict[zone].plot(imp_plot[zone][day:end].index,imp_plot[zone][day:end].values,'#E68A31', alpha=0.2)
        ax_dict[zone].plot(pum_plot[zone][day:end].index,pum_plot[zone][day:end].values,'#4875A0', alpha=0.2)
        ax_dict[zone].plot(pch_plot[zone][day:end].index,pch_plot[zone][day:end].values,'#4875A0', alpha=0.2)
        ax_dict[zone].plot(zon_plot[zone][day:end].index,zon_plot[zone][day:end].values,'#D00045', alpha=0.2)
        ax_dict[zone].plot(zwx_plot[zone][day:end].index,zwx_plot[zone][day:end].values,'#D00045', alpha=0.2)
        ax_dict[zone].set_ylabel('Power (GW)',labelpad = 11)
        #ax_dict[zone].set_xlabel('UTC Time (hours)')
        #ax_dict[zone].set_ylim(bottom = -2)
        ax_dict[zone].margins(x=0)
        ax_dict[zone].margins(y=0)
        #ax_dict[zone].set_xticks(np.arange(0,24,3))
        #ax_dict[zone].set_xticklabels(['0','3','6','9','12','15','18','21','24'])
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,0,geo_plot[zone][day:end].values,facecolor = '#873737', alpha = 0.6, label = 'Geothermal')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,geo_plot[zone][day:end].values,ror_plot[zone][day:end].values,facecolor = '#00AFE7', alpha = 0.6, label = 'Run-of-river')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,ror_plot[zone][day:end].values,win_plot[zone][day:end].values,facecolor = '#00E71F', alpha = 0.6, label = 'Wind on-shore')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,win_plot[zone][day:end].values,pv_plot[zone][day:end].values,facecolor = '#FCF100', alpha = 0.6, label = 'Photovoltaic')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,pv_plot[zone][day:end].values,hyd_plot[zone][day:end].values,facecolor = '#196AA2', alpha = 0.6, label = 'Large hydro')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,hyd_plot[zone][day:end].values,bio_plot[zone][day:end].values,facecolor = '#0D631E', alpha = 0.6, label = 'Bioenergy')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,bio_plot[zone][day:end].values,imp_plot[zone][day:end].values,facecolor = '#E68A31', alpha = 0.6, label = 'Imports')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,imp_plot[zone][day:end].values,oil_plot[zone][day:end].values,facecolor = '#4F1731', alpha = 0.6, label = 'Oil & other')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,oil_plot[zone][day:end].values,coa_plot[zone][day:end].values,facecolor = '#544848', alpha = 0.6, label = 'Coal')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,coa_plot[zone][day:end].values,gas_plot[zone][day:end].values,facecolor = '#9E8C8C', alpha = 0.6, label = 'CCGT')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,gas_plot[zone][day:end].values,pum_plot[zone][day:end].values,facecolor = '#4875A0', alpha = 0.6, label = 'Pumped hydro')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,pum_plot[zone][day:end].values,zon_plot[zone][day:end].values,facecolor = '#D00045', alpha = 0.6, label = 'Inter-zonal exchange')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,0,pch_plot[zone][day:end].values,facecolor = '#4875A0', alpha = 0.6)
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,pch_plot[zone][day:end].values,zwx_plot[zone][day:end].values,facecolor = '#D00045', alpha = 0.6)
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,zwx_plot[zone][day:end].values,exp_plot[zone][day:end].values,facecolor = '#E13D09', alpha = 0.6, label = 'Exports')
        ax_dict[zone].fill_between(geo_plot[zone][day:end].index,exp_plot[zone][day:end].values,cur_plot[zone][day:end].values,facecolor = '#0F0D3E', alpha = 0.6, label = 'Curtailment')
        ax_dict[zone].xaxis.set_major_formatter(xfmt)
    lgd = ax_dict['CSUD'].legend(loc=1,  bbox_to_anchor=(1.3,1))
    
    for reg in locs:
        
        ax_dict[reg].set_title(reg, weight='bold')
        ax_dict[reg].plot(demand_dhw_plot[reg][day:end].index,demand_dhw_plot[reg][day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
        ax_dict[reg].plot(hp_plot[reg][day:end].index,hp_plot[reg][day:end].values,'#EC3623', alpha=0.2)
        ax_dict[reg].plot(tes_dis_plot[reg][day:end].index,tes_dis_plot[reg][day:end].values,'#EC8123', alpha=0.2)
        ax_dict[reg].plot(tes_ch_plot[reg][day:end].index,tes_ch_plot[reg][day:end].values,'#EC8123', alpha=0.2)
        ax_dict[reg].plot(hp_con_plot[reg][day:end].index,hp_con_plot[reg][day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
        ax_dict[reg].set_ylabel('Power (GW)',labelpad = 11)
        #ax_dict[reg].set_xlabel('UTC Time (hours)')
        #ax_dict[reg].set_ylim(ymax = 28)
        ax_dict[reg].margins(x=0)
        ax_dict[reg].margins(y=0)
        #ax_dict[reg].set_xticks(np.arange(0,24,3))
        #ax_dict[reg].set_xticklabels(['0','3','6','9','12','15','18','21','24'])
        ax_dict[reg].fill_between(demand_dhw_plot[reg][day:end].index,0,hp_plot[reg][day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
        ax_dict[reg].fill_between(demand_dhw_plot[reg][day:end].index,hp_plot[reg][day:end].values,tes_dis_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
        ax_dict[reg].fill_between(demand_dhw_plot[reg][day:end].index,0,tes_ch_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6)
        ax_dict[reg].xaxis.set_major_formatter(xfmt)
    
        ax5.plot(cop_dict[reg][day:end].index,cop_dict[reg][day:end].values,'r', alpha=0.5, linestyle = linestyle_dict[reg], label = label_dict[reg])
    lgd = ax_dict['R14'].legend(loc=1,  bbox_to_anchor=(1.32,1.1))
    lgd = ax5.legend(loc=1,  bbox_to_anchor=(1.18,1))
    
    ax5.margins(x=0)
    ax5.margins(y=0)
    
    return(fig,lgd)   

#%%
    

def paper_plot_2(model_inst, start, stop):
    
    locs = ['R13']
    
    cop_dict = {}
    hp_dict = {}
    hp_con_dict = {}
    tes_soc_dict = {}
    tes_dis_dict = {}
    tes_ch_dict = {}
    tes_out_dict = {}
    tes_in_dict = {}
    tes_soc_min = {}
    demand_dhw_dict = {}
    
    hp_plot = {}
    hp_con_plot = {}
    tes_dis_plot = {}
    tes_ch_plot = {}
    tes_soc_plot = {}
    demand_dhw_plot = {}
    
    
    for reg in locs:
        
        cop_dict[reg] = model_inst.get_formatted_array('energy_eff').loc[{'techs':'ashp','locs':reg}].to_pandas().T
        hp_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'ashp','carriers':'dhw','locs':locs}].sum('locs').to_pandas().T
        hp_con_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'ashp','carriers':'electricity','locs':locs}].sum('locs').to_pandas().T
        tes_soc_dict[reg] = model_inst.get_formatted_array('storage').loc[{'techs':'tes','locs':locs}].sum('locs').to_pandas().T
        tes_soc_min[reg] = model_inst.get_formatted_array('storage_cap_equals').loc[{'techs':'tes', 'locs':reg}].to_pandas().T * model_inst.get_formatted_array('storage_discharge_depth').loc[{'techs':'tes'}].values[0]
        demand_dhw_dict[reg] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_heat','carriers':'dhw','locs':locs}].sum('locs').to_pandas().T
        tes_dis_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'tes','carriers':'dhw','locs':locs}].sum('locs').to_pandas().T
        tes_ch_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'tes','carriers':'dhw','locs':locs}].sum('locs').to_pandas().T
        tes_out_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_out_dict[reg][tes_out_dict[reg]<0]=0
        tes_in_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_in_dict[reg][tes_in_dict[reg]>0]=0
    
    day = start #'2015-01-01 00:00:00'
    end = stop #'2015-01-07 23:00:00'
    
    fig, (ax1, ax2) = plt.subplots(2,1, sharex='col', gridspec_kw = {'height_ratios':[0.7,0.3], 'wspace':0.1, 'hspace':0.1}, figsize=(6,6))
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter('%m-%d')
    
    for reg in locs:
            
        hp_plot[reg] = hp_dict[reg]/1e6
        hp_con_plot[reg] = -hp_con_dict[reg]/1e6
        tes_dis_plot[reg] = hp_plot[reg] + tes_out_dict[reg]/1e6
        tes_ch_plot[reg] = tes_in_dict[reg]/1e6
        demand_dhw_plot[reg] = demand_dhw_dict[reg]/1e6
        tes_soc_plot[reg] = tes_soc_dict[reg]/1e6
        
       
        ax1.set_title(reg, weight='bold')
        ax1.plot(demand_dhw_plot[reg][day:end].index,demand_dhw_plot[reg][day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
        ax1.plot(hp_plot[reg][day:end].index,hp_plot[reg][day:end].values,'#EC3623', alpha=0.2)
        ax1.plot(tes_dis_plot[reg][day:end].index,tes_dis_plot[reg][day:end].values,'#EC8123', alpha=0.2)
        ax1.plot(tes_ch_plot[reg][day:end].index,tes_ch_plot[reg][day:end].values,'#EC8123', alpha=0.2)
        ax1.plot(hp_con_plot[reg][day:end].index,hp_con_plot[reg][day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
        ax1.set_ylabel('Power (GW)',labelpad = 11)
        #ax1.set_xlabel('UTC Time (hours)')
        #ax1.set_ylim(ymax = 28)
        ax1.margins(x=0)
        ax1.margins(y=0)
        #ax1.set_xticks(np.arange(0,24,3))
        #ax1.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
        ax1.fill_between(demand_dhw_plot[reg][day:end].index,0,hp_plot[reg][day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
        ax1.fill_between(demand_dhw_plot[reg][day:end].index,hp_plot[reg][day:end].values,tes_dis_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
        ax1.fill_between(demand_dhw_plot[reg][day:end].index,0,tes_ch_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6)
        ax1.xaxis.set_major_formatter(xfmt)
        
        ax1b = ax1.twinx()
        ax1b.plot(tes_soc_plot[reg][start:stop].index,tes_soc_plot[reg][start:stop].values,'#000000', alpha=0.5, linestyle = '--', label ='TES SOC')
        ax1b.set_ylabel('SOC (kWh)')
        ax1b.set_ylim(ymin=0)
        ax1b.margins(x=0)
        ax1b.margins(y=0)
    
        ax2.plot(cop_dict[reg][day:end].index,cop_dict[reg][day:end].values,'r', alpha=0.5, linestyle = '-', label = 'COP')
        ax2.margins(x=0)
        ax2.margins(y=0)
        
    # lgd = ax1.legend(loc=1,  bbox_to_anchor=(1.6,1))
    lgd2 = ax1b.legend(loc=1,  bbox_to_anchor=(1.37,1))
    lgd3 = ax2.legend(loc=1,  bbox_to_anchor=(1.31,1))
    fig.patch.set_facecolor('#F9E6CA')
    
    return(fig,lgd2,lgd3)
