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
def power_plot(model_inst, start, stop):
    
    locs_dict = {}
    
    locs_dict['NORD'] = ['NORD','R1','R2','R3','R4','R5','R6','R7','R8']
    locs_dict['CNOR'] = ['CNOR','R9','R10','R11']
    locs_dict['CSUD'] = ['CSUD','R12','R13','R14']
    locs_dict['SUD'] = ['SUD','R15','R16','R17','R18']
    locs_dict['SICI'] = ['SICI']
    locs_dict['SARD'] = ['SARD']
    
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
    
    links_dict['NORD'] = ['inter_zonal:CNOR']
    links_dict['CNOR'] = ['inter_zonal:NORD','inter_zonal:CSUD','inter_zonal:SARD']
    links_dict['CSUD'] = ['inter_zonal:CNOR','inter_zonal:SUD','inter_zonal:SARD']
    links_dict['SUD'] = ['inter_zonal:CSUD','inter_zonal:SICI']
    links_dict['SARD'] = ['inter_zonal:CNOR','inter_zonal:CSUD']
    links_dict['SICI'] = ['inter_zonal:SUD']          
    
    eu_links_dict['NORD'] = ['inter_zonal:FR','inter_zonal:AT','inter_zonal:CH','inter_zonal:SI']
    eu_links_dict['CNOR'] = []
    eu_links_dict['CSUD'] = []
    eu_links_dict['SUD'] = ['inter_zonal:GR']
    eu_links_dict['SARD'] = []
    eu_links_dict['SICI'] = []
    
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
        

    '''
    Bidding-zone Power Plots
    '''
    
    day = start #'2015-01-01 00:00:00'
    end = stop #'2015-01-07 23:00:00'
    
    fig, ((ax1, ax2), (ax3,ax4),(ax5,ax6)) = plt.subplots(3,2, sharex='col', gridspec_kw = {'height_ratios':[1,1,1], 'wspace':0.1, 'hspace':0.2}, figsize=(12,10))
    ax_dict = {'NORD': ax1, 'CNOR': ax2, 'CSUD': ax3, 'SUD': ax4, 'SICI': ax5, 'SARD': ax6}
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter('%m-%d')
    
    for zone in locs_dict.keys():

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
        if zone in ['CNOR','SUD','SARD']:
            ax_dict[zone].yaxis.tick_right()
            ax_dict[zone].set_ylabel('')
#        ax_dict[zone].xaxis.set_major_locator(plt.MaxNLocator(6))
#        ax_dict[zone].xaxis.set_major_formatter(plt.FixedFormatter(['','day1','day2','day3','day4','day5','day6']))
        ax_dict[zone].xaxis.set_major_formatter(xfmt)
    lgd = ax_dict['NORD'].legend(loc=1,  bbox_to_anchor=(2.70, 1.031))
    
    return(fig,lgd)   

#%%
'''
Multi-node plots pre-processing - Heat sector
'''
def heat_only_DHW_plot(model_inst, start, stop, region):
    
    locs = [region]
            # ['R1','R2','R3','R4','R5','R6','R7','R8',
            # 'R9','R10','R11','R12','R13','R14','R15',
            # 'R16','R17','R18','SARD','SICI']
    
    hp_dict = {}
    hp_con_dict = {}
    tes_soc_dict = {}
    tes_dis_dict = {}
    tes_ch_dict = {}
    tes_out_dict = {}
    tes_in_dict = {}
    demand_dhw_dict = {}
    
    hp_plot = {}
    hp_con_plot = {}
    tes_soc_plot = {}
    tes_dis_plot = {}
    tes_ch_plot = {}
    demand_dhw_plot = {}
    
    
    for reg in locs:
        
        hp_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'ashp_DHW','carriers':'dhw','locs':reg}].to_pandas().T
        hp_con_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'ashp_DHW','carriers':'electricity','locs':reg}].to_pandas().T
        tes_soc_dict[reg] = model_inst.get_formatted_array('storage').loc[{'techs':'tes_DHW','locs':reg}].to_pandas().T
        demand_dhw_dict[reg] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_heat_DHW','carriers':'dhw','locs':reg}].to_pandas().T
        tes_dis_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'tes_DHW','carriers':'dhw','locs':reg}].to_pandas().T
        tes_ch_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'tes_DHW','carriers':'dhw','locs':reg}].to_pandas().T
        tes_out_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_out_dict[reg][tes_out_dict[reg]<0]=0
        tes_in_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_in_dict[reg][tes_in_dict[reg]>0]=0
        
        hp_plot[reg] = hp_dict[reg]/1e6
        hp_con_plot[reg] = -hp_con_dict[reg]/1e6
        tes_dis_plot[reg] = hp_plot[reg] + tes_out_dict[reg]/1e6
        tes_soc_plot[reg] = tes_soc_dict[reg]/1e8
        tes_ch_plot[reg] = tes_in_dict[reg]/1e6
        demand_dhw_plot[reg] = demand_dhw_dict[reg]/1e6


    '''
    Regional Heat Plots
    '''
    
    day = start #'2015-01-01 00:00:00'
    end = stop #'2015-01-07 23:00:00'
    
    fig, (ax1) = plt.subplots(1,1, sharex='col', gridspec_kw = {'height_ratios':[1], 'wspace':0.1, 'hspace':0.2}, figsize=(12,8))
    ax_dict = {reg: ax1}
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter('%m-%d')
    
    for reg in locs:
        
        ax_dict[reg].set_title(reg, weight='bold')
        ax_dict[reg].plot(demand_dhw_plot[reg][day:end].index,demand_dhw_plot[reg][day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
        ax_dict[reg].plot(hp_plot[reg][day:end].index,hp_plot[reg][day:end].values,'#EC3623', alpha=0.2)
        ax_dict[reg].plot(tes_dis_plot[reg][day:end].index,tes_dis_plot[reg][day:end].values,'#EC8123', alpha=0.2)
        ax_dict[reg].plot(tes_soc_plot[reg][day:end].index,tes_soc_plot[reg][day:end].values, '#ECE223', alpha=0.2) # storage
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
        #ax_dict[reg].fill_between(demand_dhw_plot[reg][day:end].index,0,tes_soc_plot[reg][day:end].values,facecolor = '#ECE223', alpha = 0.6, label = 'Thermal energy storage')        
        ax_dict[reg].xaxis.set_major_formatter(xfmt)
    #lgd = ax_dict[reg].legend(loc=1,  bbox_to_anchor=(1.7,1))
    lgd = ax_dict[reg].legend(loc='upper right')
    
    return(fig,lgd)

def heat_DHW_plot(model_inst, start, stop, region):
    
    locs = [region]
            # ['R1','R2','R3','R4','R5','R6','R7','R8',
            # 'R9','R10','R11','R12','R13','R14','R15',
            # 'R16','R17','R18','SARD','SICI']
    
    hp_dict = {}
    hp_con_dict = {}
    tes_soc_dict = {}
    tes_dis_dict = {}
    tes_ch_dict = {}
    tes_out_dict = {}
    tes_in_dict = {}
    demand_dhw_dict = {}
    
    hp_plot = {}
    hp_con_plot = {}
    tes_soc_plot = {}
    tes_dis_plot = {}
    tes_ch_plot = {}
    demand_dhw_plot = {}
    
    
    for reg in locs:
        
        hp_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['ashp_DHW','ashp_SH_DHW_floor'],'carriers':'dhw','locs':reg}].sum('techs').to_pandas().T
        hp_con_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':['ashp_DHW','ashp_SH_DHW_floor'],'carriers':'electricity','locs':reg}].sum('techs').to_pandas().T
        tes_soc_dict[reg] = model_inst.get_formatted_array('storage').loc[{'techs':'tes_DHW','locs':reg}].to_pandas().T
        demand_dhw_dict[reg] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_heat_DHW','carriers':'dhw','locs':reg}].to_pandas().T
        tes_dis_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'tes_DHW','carriers':'dhw','locs':reg}].to_pandas().T
        tes_ch_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'tes_DHW','carriers':'dhw','locs':reg}].to_pandas().T
        tes_out_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_out_dict[reg][tes_out_dict[reg]<0]=0
        tes_in_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_in_dict[reg][tes_in_dict[reg]>0]=0
        
        hp_plot[reg] = hp_dict[reg]/1e6
        hp_con_plot[reg] = -hp_con_dict[reg]/1e6
        tes_dis_plot[reg] = hp_plot[reg] + tes_out_dict[reg]/1e6
        tes_soc_plot[reg] = tes_soc_dict[reg]/1e8
        tes_ch_plot[reg] = tes_in_dict[reg]/1e6
        demand_dhw_plot[reg] = demand_dhw_dict[reg]/1e6


    '''
    Regional Heat Plots
    '''
    
    day = start #'2015-01-01 00:00:00'
    end = stop #'2015-01-07 23:00:00'
    
    fig, (ax1) = plt.subplots(1,1, sharex='col', gridspec_kw = {'height_ratios':[1], 'wspace':0.1, 'hspace':0.2}, figsize=(12,8))
    ax_dict = {reg: ax1}
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter('%m-%d')
    
    for reg in locs:
        
        ax_dict[reg].set_title(reg, weight='bold')
        ax_dict[reg].plot(demand_dhw_plot[reg][day:end].index,demand_dhw_plot[reg][day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
        ax_dict[reg].plot(hp_plot[reg][day:end].index,hp_plot[reg][day:end].values,'#EC3623', alpha=0.2)
        ax_dict[reg].plot(tes_dis_plot[reg][day:end].index,tes_dis_plot[reg][day:end].values,'#EC8123', alpha=0.2)
        ax_dict[reg].plot(tes_soc_plot[reg][day:end].index,tes_soc_plot[reg][day:end].values, '#ECE223', alpha=0.2) # storage
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
        #ax_dict[reg].fill_between(demand_dhw_plot[reg][day:end].index,0,tes_soc_plot[reg][day:end].values,facecolor = '#ECE223', alpha = 0.6, label = 'Thermal energy storage')        
        ax_dict[reg].xaxis.set_major_formatter(xfmt)
    lgd = ax_dict[reg].legend(loc=1,  bbox_to_anchor=(1.7,1))
    
    return(fig,lgd)     

def heat_SH_plot(model_inst,start,stop,region):
    
    locs = [region]
            # ['R1','R2','R3','R4','R5','R6','R7','R8',
            # 'R9','R10','R11','R12','R13','R14','R15',
            # 'R16','R17','R18','SARD','SICI']
    
    hp_dict = {}
    hp_con_dict = {}
    tes_soc_dict = {}
    tes_dis_dict = {}
    tes_ch_dict = {}
    tes_out_dict = {}
    tes_in_dict = {}
    demand_SH_dict = {}
    
    hp_plot = {}
    hp_con_plot = {}
    tes_soc_plot = {}
    tes_dis_plot = {}
    tes_ch_plot = {}
    demand_SH_plot = {}
    
    
    for reg in locs:
        
        hp_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['ashp_SH_floor','ashp_SH_DHW_floor'],'carriers':'heat','locs':reg}].sum('techs').to_pandas().T
        hp_con_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':['ashp_SH_floor','ashp_SH_DHW_floor'],'carriers':'electricity','locs':reg}].sum('techs').to_pandas().T
        tes_soc_dict[reg] = model_inst.get_formatted_array('storage').loc[{'techs':'tes_floor_heating','locs':reg}].to_pandas().T
        demand_SH_dict[reg] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_heating_floor','carriers':'heat','locs':reg}].to_pandas().T
        tes_dis_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'tes_floor_heating','carriers':'heat','locs':reg}].to_pandas().T
        tes_ch_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'tes_floor_heating','carriers':'heat','locs':reg}].to_pandas().T
        tes_out_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_out_dict[reg][tes_out_dict[reg]<0]=0
        tes_in_dict[reg] = tes_dis_dict[reg]+tes_ch_dict[reg]
        tes_in_dict[reg][tes_in_dict[reg]>0]=0
        
        hp_plot[reg] = hp_dict[reg]/1e6
        hp_con_plot[reg] = -hp_con_dict[reg]/1e6
        tes_dis_plot[reg] = hp_plot[reg] + tes_out_dict[reg]/1e6
        tes_soc_plot[reg] = tes_soc_dict[reg]/1e8
        tes_ch_plot[reg] = tes_in_dict[reg]/1e6
        demand_SH_plot[reg] = demand_SH_dict[reg]/1e6


    '''
    Regional Heat Plots
    '''
    
    day = start #'2015-01-01 00:00:00'
    end = stop #'2015-01-07 23:00:00'
    
    fig, (ax1) = plt.subplots(1,1, sharex='col', gridspec_kw = {'height_ratios':[1], 'wspace':0.1, 'hspace':0.2}, figsize=(12,8))
    ax_dict = {reg: ax1}
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter('%m-%d')
    
    for reg in locs:
        
        ax_dict[reg].set_title(reg, weight='bold')
        ax_dict[reg].plot(demand_SH_plot[reg][day:end].index,demand_SH_plot[reg][day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='SH loads')
        ax_dict[reg].plot(hp_plot[reg][day:end].index,hp_plot[reg][day:end].values,'#EC3623', alpha=0.2)
        ax_dict[reg].plot(tes_dis_plot[reg][day:end].index,tes_dis_plot[reg][day:end].values,'#EC8123', alpha=0.2)
        ax_dict[reg].plot(tes_soc_plot[reg][day:end].index,tes_soc_plot[reg][day:end].values, '#ECE223', alpha=0.2) # storage
        ax_dict[reg].plot(tes_ch_plot[reg][day:end].index,tes_ch_plot[reg][day:end].values,'#EC8123', alpha=0.2)
        ax_dict[reg].plot(hp_con_plot[reg][day:end].index,hp_con_plot[reg][day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
        ax_dict[reg].set_ylabel('Power (GW)',labelpad = 11)
        #ax_dict[reg].set_xlabel('UTC Time (hours)')
        #ax_dict[reg].set_ylim(ymax = 0.02)
        #ax_dict[reg].set_ylim(ymin = -0.02)
        ax_dict[reg].margins(x=0)
        ax_dict[reg].margins(y=0)
        #ax_dict[reg].set_xticks(np.arange(0,24,3))
        #ax_dict[reg].set_xticklabels(['0','3','6','9','12','15','18','21','24'])
        ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,hp_plot[reg][day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
        ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,hp_plot[reg][day:end].values,tes_dis_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage dis')
        ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,tes_ch_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6)
        ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,tes_soc_plot[reg][day:end].values,facecolor = '#ECE223', alpha = 0.6, label = 'Thermal energy storage soc')        
        ax_dict[reg].xaxis.set_major_formatter(xfmt)
    lgd = ax_dict[reg].legend(loc=1,  bbox_to_anchor=(1.7,1))
    
    return(fig,lgd)

#%%
    '''
    operatività pompe di calore
    '''
    
# def operatività_pompe_di_calore(model_inst,start,stop,region):
    
#     locs = [region]
#             # ['R1','R2','R3','R4','R5','R6','R7','R8',
#             # 'R9','R10','R11','R12','R13','R14','R15',
#             # 'R16','R17','R18','SARD','SICI']
    
#     hp_DHW_dict = {}
#     hp_SH_dict = {}
#     hp_con_DHW_dict = {}
#     hp_con_SH_dict = {}
#     tes_DHW_soc_dict = {}
#     tes_SH_soc_dict = {}
#     tes_DHW_dis_dict = {}
#     tes_SH_dis_dict = {}
#     tes_DHW_ch_dict = {}
#     tes_SH_ch_dict = {}
#     tes_DHW_out_dict = {}
#     tes_SH_out_dict = {}
#     tes_DHW_in_dict = {}
#     tes_SH_in_dict = {}
#     demand_SH_dict = {}
#     demand_DHW_dict = {}
    
#     hp_DHW_plot = {}
#     hp_SH_plot = {}
#     hp_con_DHW_plot = {}
#     hp_con_SH_plot = {}
#     tes_DHW_soc_plot = {}
#     tes_SH_soc_plot = {}
#     tes_DHW_dis_plot = {}
#     tes_SH_dis_plot = {}
#     tes_DHW_ch_plot = {}
#     tes_SH_ch_plot = {}
#     demand_SH_plot = {}
#     demand_DHW_plot = {}
    
    
#     for reg in locs:
        
#         hp_SH_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['ashp_SH_floor','ashp_SH_DHW_floor'],'carriers':'heat','locs':reg}].sum('techs').to_pandas().T
#         hp_DHW_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['ashp_DHW','ashp_SH_DHW_floor'],'carriers':'dhw','locs':reg}].sum('techs').to_pandas().T
#         hp_con_DHW_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':['ashp_DHW','ashp_SH_DHW_floor'],'carriers':'electricity','locs':reg}].sum('techs').to_pandas().T
#         hp_con_SH_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':['ashp_SH_floor','ashp_SH_DHW_floor'],'carriers':'electricity','locs':reg}].sum('techs').to_pandas().T
#         tes_SH_soc_dict[reg] = model_inst.get_formatted_array('storage').loc[{'techs':'tes_floor_heating','locs':reg}].to_pandas().T
#         tes_DHW_soc_dict[reg] = model_inst.get_formatted_array('storage').loc[{'techs':'tes_DHW','locs':reg}].to_pandas().T
#         demand_SH_dict[reg] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_heating_floor','carriers':'heat','locs':reg}].to_pandas().T
#         demand_DHW_dict[reg] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_heat_DHW','carriers':'dhw','locs':reg}].to_pandas().T
#         tes_SH_dis_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'tes_floor_heating','carriers':'heat','locs':reg}].to_pandas().T
#         tes_DHW_dis_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'tes_DHW','carriers':'dhw','locs':reg}].to_pandas().T
#         tes_SH_ch_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'tes_floor_heating','carriers':'heat','locs':reg}].to_pandas().T
#         tes_DHW_ch_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'tes_DHW','carriers':'dhw','locs':reg}].to_pandas().T
#         tes_SH_out_dict[reg] = tes_SH_dis_dict[reg]+tes_SH_ch_dict[reg]
#         tes_SH_out_dict[reg][tes_SH_out_dict[reg]<0]=0
#         tes_SH_in_dict[reg] = tes_SH_dis_dict[reg]+tes_SH_ch_dict[reg]
#         tes_SH_in_dict[reg][tes_SH_in_dict[reg]>0]=0
#         tes_DHW_out_dict[reg] = tes_DHW_dis_dict[reg]+tes_DHW_ch_dict[reg]
#         tes_DHW_out_dict[reg][tes_DHW_out_dict[reg]<0]=0
#         tes_DHW_in_dict[reg] = tes_DHW_dis_dict[reg]+tes_DHW_ch_dict[reg]
#         tes_DHW_in_dict[reg][tes_DHW_in_dict[reg]>0]=0
        
#         hp_SH_plot[reg] = hp_SH_dict[reg]/1e6
#         hp_con_SH_plot[reg] = -hp_con_SH_dict[reg]/1e6
#         tes_SH_dis_plot[reg] = hp_SH_plot[reg] + tes_SH_out_dict[reg]/1e6
#         tes_SH_soc_plot[reg] = tes_SH_soc_dict[reg]/1e8
#         tes_SH_ch_plot[reg] = tes_SH_in_dict[reg]/1e6
#         demand_SH_plot[reg] = demand_SH_dict[reg]/1e6
#         hp_DHW_plot[reg] = hp_DHW_dict[reg]/1e6
#         hp_con_DHW_plot[reg] = -hp_con_DHW_dict[reg]/1e6
#         tes_DHW_dis_plot[reg] = hp_DHW_plot[reg] + tes_DHW_out_dict[reg]/1e6
#         tes_DHW_soc_plot[reg] = tes_DHW_soc_dict[reg]/1e8
#         tes_DHW_ch_plot[reg] = tes_DHW_in_dict[reg]/1e6
#         demand_DHW_plot[reg] = demand_DHW_dict[reg]/1e6


#     '''
#     Regional Heat Plots
#     '''
    
#     day = start #'2015-01-01 00:00:00'
#     end = stop #'2015-01-07 23:00:00'
    
#     fig, (ax1) = plt.subplots(1,1, sharex='col', gridspec_kw = {'height_ratios':[1], 'wspace':0.1, 'hspace':0.2}, figsize=(12,8))
#     ax_dict = {reg: ax1}
#     fig.autofmt_xdate()
#     xfmt = mdates.DateFormatter('%m-%d')
    
#     for reg in locs:
        
#         ax_dict[reg].set_title(reg, weight='bold')
#         ax_dict[reg].plot(demand_SH_plot[reg][day:end].index,demand_SH_plot[reg][day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='SH loads')
#         ax_dict[reg].plot(hp_SH_plot[reg][day:end].index,hp_SH_plot[reg][day:end].values,'#EC3623', alpha=0.2)
#         ax_dict[reg].plot(tes_SH_dis_plot[reg][day:end].index,tes_SH_dis_plot[reg][day:end].values,'#EC8123', alpha=0.2)
#         ax_dict[reg].plot(tes_SH_soc_plot[reg][day:end].index,tes_SH_soc_plot[reg][day:end].values, '#ECE223', alpha=0.2) # storage
#         ax_dict[reg].plot(tes_SH_ch_plot[reg][day:end].index,tes_SH_ch_plot[reg][day:end].values,'#EC8123', alpha=0.2)
#         ax_dict[reg].plot(hp_con_SH_plot[reg][day:end].index,hp_con_SH_plot[reg][day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption SH')
#         ax_dict[reg].plot(demand_DHW_plot[reg][day:end].index,demand_DHW_plot[reg][day:end].values,'#000000', alpha=0.8, linestyle = '-', label ='DHW loads')
#         ax_dict[reg].plot(hp_DHW_plot[reg][day:end].index,hp_DHW_plot[reg][day:end].values,'#EC3623', alpha=0.6)
#         ax_dict[reg].plot(tes_DHW_dis_plot[reg][day:end].index,tes_DHW_dis_plot[reg][day:end].values,'#EC8123', alpha=0.6)
#         ax_dict[reg].plot(tes_DHW_soc_plot[reg][day:end].index,tes_DHW_soc_plot[reg][day:end].values, '#ECE223', alpha=0.2) # storage
#         ax_dict[reg].plot(tes_DHW_ch_plot[reg][day:end].index,tes_DHW_ch_plot[reg][day:end].values,'#EC8123', alpha=0.6)
#         ax_dict[reg].plot(hp_con_DHW_plot[reg][day:end].index,hp_con_DHW_plot[reg][day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption DHW')
#         ax_dict[reg].set_ylabel('Power (GW)',labelpad = 11)
#         #ax_dict[reg].set_xlabel('UTC Time (hours)')
#         #ax_dict[reg].set_ylim(ymax = 0.02)
#         #ax_dict[reg].set_ylim(ymin = -0.02)
#         ax_dict[reg].margins(x=0)
#         ax_dict[reg].margins(y=0)
#         #ax_dict[reg].set_xticks(np.arange(0,24,3))
#         #ax_dict[reg].set_xticklabels(['0','3','6','9','12','15','18','21','24'])
#         ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,hp_SH_plot[reg][day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
#         ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,hp_SH_plot[reg][day:end].values,tes_SH_dis_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
#         ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,tes_SH_ch_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6)
#         ax_dict[reg].fill_between(demand_DHW_plot[reg][day:end].index,0,hp_DHW_plot[reg][day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps DHW')
#         ax_dict[reg].fill_between(demand_DHW_plot[reg][day:end].index,hp_DHW_plot[reg][day:end].values,tes_DHW_dis_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage DHW')
#         ax_dict[reg].fill_between(demand_DHW_plot[reg][day:end].index,0,tes_DHW_ch_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6)
#         #ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,tes_soc_plot[reg][day:end].values,facecolor = '#ECE223', alpha = 0.6, label = 'Thermal energy storage')        
#         ax_dict[reg].xaxis.set_major_formatter(xfmt)
#     lgd = ax_dict[reg].legend(loc=1,  bbox_to_anchor=(1.7,1))
    
#     return(fig,lgd)

# # %%
#     '''
#     operatività stoccaggio
#     '''
    
# def tes_SH(model_inst,start,stop,region):
    
#     locs = [region]
#             # ['R1','R2','R3','R4','R5','R6','R7','R8',
#             # 'R9','R10','R11','R12','R13','R14','R15',
#             # 'R16','R17','R18','SARD','SICI']
    
#     hp_SH_dict = {}
#     hp_con_SH_dict = {}
#     tes_SH_soc_dict = {}
#     tes_SH_dis_dict = {}
#     tes_SH_ch_dict = {}
#     tes_SH_out_dict = {}
#     tes_SH_in_dict = {}
#     demand_SH_dict = {}
    
#     hp_SH_plot = {}
#     hp_con_SH_plot = {}
#     tes_SH_soc_plot = {}
#     tes_SH_dis_plot = {}
#     tes_SH_ch_plot = {}
#     demand_SH_plot = {}
    
    
#     for reg in locs:
        
#         hp_SH_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':['ashp_SH_floor','ashp_SH_DHW_floor'],'carriers':'heating','locs':reg}].sum('techs').to_pandas().T
#         hp_con_SH_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':['ashp_SH_floor','ashp_SH_DHW_floor'],'carriers':'electricity','locs':reg}].sum('techs').to_pandas().T
#         tes_SH_soc_dict[reg] = model_inst.get_formatted_array('storage').loc[{'techs':'tes_floor_heating','locs':reg}].to_pandas().T
#         demand_SH_dict[reg] = -model_inst.get_formatted_array('carrier_con').loc[{'techs':'demand_heating_floor','carriers':'heating','locs':reg}].to_pandas().T
#         tes_SH_dis_dict[reg] = model_inst.get_formatted_array('carrier_prod').loc[{'techs':'tes_floor_heating','carriers':'heating','locs':reg}].to_pandas().T
#         tes_SH_ch_dict[reg] = model_inst.get_formatted_array('carrier_con').loc[{'techs':'tes_floor_heating','carriers':'heating','locs':reg}].to_pandas().T
#         tes_SH_out_dict[reg] = tes_SH_dis_dict[reg]+tes_SH_ch_dict[reg]
#         tes_SH_out_dict[reg][tes_SH_out_dict[reg]<0]=0
#         tes_SH_in_dict[reg] = tes_SH_dis_dict[reg]+tes_SH_ch_dict[reg]
#         tes_SH_in_dict[reg][tes_SH_in_dict[reg]>0]=0
        
#         hp_SH_plot[reg] = hp_SH_dict[reg]/1e6
#         hp_con_SH_plot[reg] = -hp_con_SH_dict[reg]/1e6
#         tes_SH_dis_plot[reg] = hp_SH_plot[reg] + tes_SH_out_dict[reg]/1e6
#         tes_SH_soc_plot[reg] = tes_SH_soc_dict[reg]/1e8
#         tes_SH_ch_plot[reg] = tes_SH_in_dict[reg]/1e6
#         demand_SH_plot[reg] = demand_SH_dict[reg]/1e6


#     '''
#     Regional Heat Plots
#     '''
    
#     day = start #'2015-01-01 00:00:00'
#     end = stop #'2015-01-07 23:00:00'
    
#     fig, (ax1) = plt.subplots(1,1, sharex='col', gridspec_kw = {'height_ratios':[1], 'wspace':0.1, 'hspace':0.2}, figsize=(12,8))
#     ax_dict = {reg: ax1}
#     fig.autofmt_xdate()
#     xfmt = mdates.DateFormatter('%m-%d')
    
#     for reg in locs:
        
#         ax_dict[reg].set_title(reg, weight='bold')
#         ax_dict[reg].plot(demand_SH_plot[reg][day:end].index,demand_SH_plot[reg][day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='SH loads')
#         #ax_dict[reg].plot(hp_SH_plot[reg][day:end].index,hp_SH_plot[reg][day:end].values,'#EC3623', alpha=0.2)
#         ax_dict[reg].plot(tes_SH_dis_plot[reg][day:end].index,tes_SH_dis_plot[reg][day:end].values,'#EC8123', alpha=0.2)
#         ax_dict[reg].plot(tes_SH_soc_plot[reg][day:end].index,tes_SH_soc_plot[reg][day:end].values, '#ECE223', alpha=0.2) # storage
#         ax_dict[reg].plot(tes_SH_ch_plot[reg][day:end].index,tes_SH_ch_plot[reg][day:end].values,'#EC8123', alpha=0.2)
#         #ax_dict[reg].plot(hp_con_SH_plot[reg][day:end].index,hp_con_SH_plot[reg][day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption SH')
#         ax_dict[reg].set_ylabel('Power (GW)',labelpad = 11)
#         #ax_dict[reg].set_xlabel('UTC Time (hours)')
#         #ax_dict[reg].set_ylim(ymax = 0.02)
#         #ax_dict[reg].set_ylim(ymin = -0.02)
#         ax_dict[reg].margins(x=0)
#         ax_dict[reg].margins(y=0)
#         #ax_dict[reg].set_xticks(np.arange(0,24,3))
#         #ax_dict[reg].set_xticklabels(['0','3','6','9','12','15','18','21','24'])
#         ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,hp_SH_plot[reg][day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
#         ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,hp_SH_plot[reg][day:end].values,tes_SH_dis_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
#         ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,tes_SH_ch_plot[reg][day:end].values,facecolor = '#EC8123', alpha = 0.6)
#         #ax_dict[reg].fill_between(demand_SH_plot[reg][day:end].index,0,tes_soc_plot[reg][day:end].values,facecolor = '#ECE223', alpha = 0.6, label = 'Thermal energy storage')        
#         ax_dict[reg].xaxis.set_major_formatter(xfmt)
#     lgd = ax_dict[reg].legend(loc=1,  bbox_to_anchor=(1.7,1))
    
#     return(fig,lgd)
    
    