# -*- coding: utf-8 -*-
"""
Created on Mon May 27 11:46:57 2019

Script to generate static plots, tuned on the specific case of the Italian 20-node model

@author: F.Lombardi
"""

import matplotlib.pyplot as plt

#%% 
'''
Multi-node plots pre-processing - Power sector
'''
def power_plot(model_test, start, stop):
    ccgt_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ccgt','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    coal_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    coal_usc_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal_usc','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    oil_other_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'oil_&_other','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    biomass_wood_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biomass_wood','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    biofuel_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biofuel','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    biogas_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biogas','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    wte_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wte','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    geothermal_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'geothermal','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    hydro_ror_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_ror','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    hydro_dam_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_dam','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    phs_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'phs','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    pv_farm_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_farm','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    pv_rooftop_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_rooftop','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    wind_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wind','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    el_import_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'el_import','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    zonal_import_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':['inter_zonal:CNOR'],'carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').sum('techs').to_pandas().T
    zonal_export_NORD = model_test.get_formatted_array('carrier_con').loc[{'techs':['inter_zonal:NORD'],'carriers':'electricity','locs':['CNOR']}].sum('locs').sum('techs').to_pandas().T
    demand_NORD = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_power','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    phs_charge_NORD = model_test.get_formatted_array('carrier_con').loc[{'techs':'phs','carriers':'electricity','locs':['NORD','R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    
    geo_NORD = geothermal_NORD/1000000
    ror_NORD = geo_NORD + hydro_ror_NORD/1000000
    win_NORD = ror_NORD + wind_NORD/1000000
    pv_NORD = win_NORD + pv_farm_NORD/1000000 + pv_rooftop_NORD/1000000
    hyd_NORD = pv_NORD + hydro_dam_NORD/1000000
    bio_NORD = hyd_NORD + biomass_wood_NORD/1000000 + biofuel_NORD/1000000 + biogas_NORD/1000000 + wte_NORD/1000000
    imp_NORD = bio_NORD + el_import_NORD/1000000
    oil_NORD = imp_NORD + oil_other_NORD/1000000
    coa_NORD = oil_NORD + coal_NORD/1000000 + coal_usc_NORD/1000000
    gas_NORD = coa_NORD + ccgt_NORD/1000000
    pum_NORD = gas_NORD + phs_NORD/1000000
    zon_NORD = pum_NORD + zonal_import_NORD/1000000
    pch_NORD = phs_charge_NORD/1000000
    zwx_NORD = pch_NORD + zonal_export_NORD/1000000
    loa_NORD = demand_NORD/1000000
    
    ccgt_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ccgt','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    coal_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    coal_usc_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal_usc','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    oil_other_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'oil_&_other','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    biomass_wood_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biomass_wood','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    biofuel_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biofuel','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    biogas_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biogas','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    wte_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wte','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    geothermal_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'geothermal','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    hydro_ror_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_ror','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    hydro_dam_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_dam','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    phs_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'phs','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    pv_farm_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_farm','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    pv_rooftop_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_rooftop','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    wind_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wind','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    el_import_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'el_import','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    zonal_import_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':['inter_zonal:NORD','inter_zonal:CSUD','inter_zonal:SARD'],'carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').sum('techs').to_pandas().T
    zonal_export_CNOR = model_test.get_formatted_array('carrier_con').loc[{'techs':['inter_zonal:CNOR'],'carriers':'electricity','locs':['NORD','CSUD','SARD']}].sum('locs').sum('techs').to_pandas().T
    demand_CNOR = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_power','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    phs_charge_CNOR = model_test.get_formatted_array('carrier_con').loc[{'techs':'phs','carriers':'electricity','locs':['CNOR','R9','R10','R11']}].sum('locs').to_pandas().T
    
    geo_CNOR = geothermal_CNOR/1000000
    ror_CNOR = geo_CNOR + hydro_ror_CNOR/1000000
    win_CNOR = ror_CNOR + wind_CNOR/1000000
    pv_CNOR = win_CNOR + pv_farm_CNOR/1000000 + pv_rooftop_CNOR/1000000
    hyd_CNOR = pv_CNOR + hydro_dam_CNOR/1000000
    bio_CNOR = hyd_CNOR + biomass_wood_CNOR/1000000 + biofuel_CNOR/1000000 + biogas_CNOR/1000000 + wte_CNOR/1000000
    imp_CNOR = bio_CNOR + el_import_CNOR/1000000
    oil_CNOR = imp_CNOR + oil_other_CNOR/1000000
    coa_CNOR = oil_CNOR + coal_CNOR/1000000 + coal_usc_CNOR/1000000
    gas_CNOR = coa_CNOR + ccgt_CNOR/1000000
    pum_CNOR = gas_CNOR + phs_CNOR/1000000
    zon_CNOR = pum_CNOR + zonal_import_CNOR/1000000
    pch_CNOR = phs_charge_CNOR/1000000
    zwx_CNOR = pch_CNOR + zonal_export_CNOR/1000000
    loa_CNOR = demand_CNOR/1000000
    
    ccgt_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ccgt','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    coal_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    coal_usc_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal_usc','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    oil_other_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'oil_&_other','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    biomass_wood_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biomass_wood','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    biofuel_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biofuel','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    biogas_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biogas','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    wte_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wte','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    geothermal_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'geothermal','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    hydro_ror_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_ror','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    hydro_dam_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_dam','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    phs_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'phs','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    pv_farm_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_farm','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    pv_rooftop_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_rooftop','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    wind_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wind','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    el_import_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'el_import','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    zonal_import_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':['inter_zonal:SUD','inter_zonal:SARD'],'carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').sum('techs').to_pandas().T
    zonal_export_CSUD = model_test.get_formatted_array('carrier_con').loc[{'techs':['inter_zonal:SUD','inter_zonal:SARD'],'carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').sum('techs').to_pandas().T
    demand_CSUD = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_power','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    phs_charge_CSUD = model_test.get_formatted_array('carrier_con').loc[{'techs':'phs','carriers':'electricity','locs':['CSUD','R12','R13','R14']}].sum('locs').to_pandas().T
    
    geo_CSUD = geothermal_CSUD/1000000
    ror_CSUD = geo_CSUD + hydro_ror_CSUD/1000000
    win_CSUD = ror_CSUD + wind_CSUD/1000000
    pv_CSUD = win_CSUD + pv_farm_CSUD/1000000 + pv_rooftop_CSUD/1000000
    hyd_CSUD = pv_CSUD + hydro_dam_CSUD/1000000
    bio_CSUD = hyd_CSUD + biomass_wood_CSUD/1000000 + biofuel_CSUD/1000000 + biogas_CSUD/1000000 + wte_CSUD/1000000
    imp_CSUD = bio_CSUD + el_import_CSUD/1000000
    oil_CSUD = imp_CSUD + oil_other_CSUD/1000000
    coa_CSUD = oil_CSUD + coal_CSUD/1000000 + coal_usc_CSUD/1000000
    gas_CSUD = coa_CSUD + ccgt_CSUD/1000000
    pum_CSUD = gas_CSUD + phs_CSUD/1000000
    zon_CSUD = pum_CSUD + zonal_import_CSUD/1000000
    pch_CSUD = phs_charge_CSUD/1000000
    zwx_CSUD = pch_CSUD + zonal_export_CSUD/1000000
    loa_CSUD = demand_CSUD/1000000
    
    ccgt_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ccgt','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    coal_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    coal_usc_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal_usc','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    oil_other_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'oil_&_other','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    biomass_wood_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biomass_wood','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    biofuel_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biofuel','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    biogas_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biogas','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    wte_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wte','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    geothermal_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'geothermal','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    hydro_ror_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_ror','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    hydro_dam_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_dam','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    phs_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'phs','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    pv_farm_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_farm','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    pv_rooftop_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_rooftop','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    wind_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wind','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    el_import_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'el_import','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    zonal_import_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':['inter_zonal:CSUD','inter_zonal:SICI'],'carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').sum('techs').to_pandas().T
    zonal_export_SUD = model_test.get_formatted_array('carrier_con').loc[{'techs':['inter_zonal:CSUD','inter_zonal:SICI'],'carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').sum('techs').to_pandas().T
    demand_SUD = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_power','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    phs_charge_SUD = model_test.get_formatted_array('carrier_con').loc[{'techs':'phs','carriers':'electricity','locs':['SUD','R15','R16','R17','R18']}].sum('locs').to_pandas().T
    
    geo_SUD = geothermal_SUD/1000000
    ror_SUD = geo_SUD + hydro_ror_SUD/1000000
    win_SUD = ror_SUD + wind_SUD/1000000
    pv_SUD = win_SUD + pv_farm_SUD/1000000 + pv_rooftop_SUD/1000000
    hyd_SUD = pv_SUD + hydro_dam_SUD/1000000
    bio_SUD = hyd_SUD + biomass_wood_SUD/1000000 + biofuel_SUD/1000000 + biogas_SUD/1000000 + wte_SUD/1000000
    imp_SUD = bio_SUD + el_import_SUD/1000000
    oil_SUD = imp_SUD + oil_other_SUD/1000000
    coa_SUD = oil_SUD + coal_SUD/1000000 + coal_usc_SUD/1000000
    gas_SUD = coa_SUD + ccgt_SUD/1000000
    pum_SUD = gas_SUD + phs_SUD/1000000
    zon_SUD = pum_SUD + zonal_import_SUD/1000000
    pch_SUD = phs_charge_SUD/1000000
    zwx_SUD = pch_SUD + zonal_export_SUD/1000000
    loa_SUD = demand_SUD/1000000
    
    ccgt_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ccgt','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    coal_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    coal_usc_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal_usc','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    oil_other_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'oil_&_other','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    biomass_wood_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biomass_wood','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    biofuel_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biofuel','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    biogas_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biogas','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    wte_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wte','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    geothermal_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'geothermal','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    hydro_ror_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_ror','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    hydro_dam_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_dam','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    phs_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'phs','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    pv_farm_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_farm','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    pv_rooftop_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_rooftop','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    wind_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wind','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    el_import_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'el_import','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    zonal_import_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':['inter_zonal:CNOR','inter_zonal:CSUD'],'carriers':'electricity','locs':['SARD']}].sum('locs').sum('techs').to_pandas().T
    zonal_export_SARD = model_test.get_formatted_array('carrier_con').loc[{'techs':['inter_zonal:SARD'],'carriers':'electricity','locs':['CNOR','CSUD']}].sum('locs').sum('techs').to_pandas().T
    demand_SARD = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_power','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    phs_charge_SARD = model_test.get_formatted_array('carrier_con').loc[{'techs':'phs','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    
    geo_SARD = geothermal_SARD/1000000
    ror_SARD = geo_SARD + hydro_ror_SARD/1000000
    win_SARD = ror_SARD + wind_SARD/1000000
    pv_SARD = win_SARD + pv_farm_SARD/1000000 + pv_rooftop_SARD/1000000
    hyd_SARD = pv_SARD + hydro_dam_SARD/1000000
    bio_SARD = hyd_SARD + biomass_wood_SARD/1000000 + biofuel_SARD/1000000 + biogas_SARD/1000000 + wte_SARD/1000000
    imp_SARD = bio_SARD + el_import_SARD/1000000
    oil_SARD = imp_SARD + oil_other_SARD/1000000
    coa_SARD = oil_SARD + coal_SARD/1000000 + coal_usc_SARD/1000000
    gas_SARD = coa_SARD + ccgt_SARD/1000000
    pum_SARD = gas_SARD + phs_SARD/1000000
    zon_SARD = pum_SARD + zonal_import_SARD/1000000
    pch_SARD = phs_charge_SARD/1000000
    zwx_SARD = pch_SARD + zonal_export_SARD/1000000
    loa_SARD = demand_SARD/1000000
    
    ccgt_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ccgt','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    coal_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    coal_usc_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'coal_usc','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    oil_other_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'oil_&_other','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    biomass_wood_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biomass_wood','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    biofuel_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biofuel','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    biogas_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'biogas','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    wte_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wte','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    geothermal_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'geothermal','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    hydro_ror_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_ror','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    hydro_dam_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'hydro_dam','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    phs_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'phs','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    pv_farm_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_farm','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    pv_rooftop_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'pv_rooftop','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    wind_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'wind','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    el_import_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'el_import','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    zonal_import_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':['inter_zonal:SUD'],'carriers':'electricity','locs':['SICI']}].sum('locs').sum('techs').to_pandas().T
    zonal_export_SICI = model_test.get_formatted_array('carrier_con').loc[{'techs':['inter_zonal:SUD'],'carriers':'electricity','locs':['SICI']}].sum('locs').sum('techs').to_pandas().T
    demand_SICI = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_power','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    phs_charge_SICI = model_test.get_formatted_array('carrier_con').loc[{'techs':'phs','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    
    geo_SICI = geothermal_SICI/1000000
    ror_SICI = geo_SICI + hydro_ror_SICI/1000000
    win_SICI = ror_SICI + wind_SICI/1000000
    pv_SICI = win_SICI + pv_farm_SICI/1000000 + pv_rooftop_SICI/1000000
    hyd_SICI = pv_SICI + hydro_dam_SICI/1000000
    bio_SICI = hyd_SICI + biomass_wood_SICI/1000000 + biofuel_SICI/1000000 + biogas_SICI/1000000 + wte_SICI/1000000
    imp_SICI = bio_SICI + el_import_SICI/1000000
    oil_SICI = imp_SICI + oil_other_SICI/1000000
    coa_SICI = oil_SICI + coal_SICI/1000000 + coal_usc_SICI/1000000
    gas_SICI = coa_SICI + ccgt_SICI/1000000
    pum_SICI = gas_SICI + phs_SICI/1000000
    zon_SICI = pum_SICI + zonal_import_SICI/1000000
    pch_SICI = phs_charge_SICI/1000000
    zwx_SICI = pch_SICI + zonal_export_SICI/1000000
    loa_SICI = demand_SICI/1000000


    #%% 
    '''
    Bidding-zone Power Plots
    '''
    
    day = start #'2015-01-01 00:00:00'
    end = stop #'2015-01-07 23:00:00'
    #fig = plt.figure(figsize=(10,6))
    fig, ((ax1, ax2), (ax3,ax4),(ax5,ax6)) = plt.subplots(3,2, sharex='col', gridspec_kw = {'height_ratios':[1,1,1], 'wspace':0.1, 'hspace':0.2}, figsize=(12,10))
    
    #ax1 = fig.add_subplot(321)
    ax1.set_title("NORD", weight='bold')
    ax1.plot(loa_NORD[day:end].index,loa_NORD[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='Baseline load')
    #ax1.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax1.plot(geo_NORD[day:end].index,geo_NORD[day:end].values,'#873737', alpha=0.2)
    ax1.plot(ror_NORD[day:end].index,ror_NORD[day:end].values,'#00AFE7', alpha=0.2)
    ax1.plot(win_NORD[day:end].index,win_NORD[day:end].values,'#00E71F', alpha=0.2)
    ax1.plot(pv_NORD[day:end].index,pv_NORD[day:end].values,'#FCF100', alpha=0.2)
    ax1.plot(hyd_NORD[day:end].index,hyd_NORD[day:end].values,'#196AA2', alpha=0.2)
    ax1.plot(bio_NORD[day:end].index,bio_NORD[day:end].values,'#0E5801', alpha=0.2)
    ax1.plot(oil_NORD[day:end].index,oil_NORD[day:end].values,'#4F1731', alpha=0.2)        
    ax1.plot(coa_NORD[day:end].index,coa_NORD[day:end].values,'#544848', alpha=0.2)
    ax1.plot(gas_NORD[day:end].index,gas_NORD[day:end].values,'#9E8C8C', alpha=0.2)
    ax1.plot(imp_NORD[day:end].index,imp_NORD[day:end].values,'#E68A31', alpha=0.2)
    ax1.plot(pum_NORD[day:end].index,pum_NORD[day:end].values,'#4875A0', alpha=0.2)
    ax1.plot(pch_NORD[day:end].index,pch_NORD[day:end].values,'#4875A0', alpha=0.2)
    ax1.plot(zon_NORD[day:end].index,zon_NORD[day:end].values,'#D00045', alpha=0.2)
    ax1.plot(zwx_NORD[day:end].index,zwx_NORD[day:end].values,'#D00045', alpha=0.2)
    ax1.set_ylabel('Power (GW)',labelpad = 11)
    #ax1.set_xlabel('UTC Time (hours)')
    #ax1.set_ylim(bottom = -2)
    ax1.margins(x=0)
    ax1.margins(y=0)
    #ax1.set_xticks(np.arange(0,24,3))
    #ax1.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax1.fill_between(geo_NORD[day:end].index,0,geo_NORD[day:end].values,facecolor = '#873737', alpha = 0.6, label = 'Geothermal')
    ax1.fill_between(geo_NORD[day:end].index,geo_NORD[day:end].values,ror_NORD[day:end].values,facecolor = '#00AFE7', alpha = 0.6, label = 'Run-of-river')
    ax1.fill_between(geo_NORD[day:end].index,ror_NORD[day:end].values,win_NORD[day:end].values,facecolor = '#00E71F', alpha = 0.6, label = 'Wind')
    ax1.fill_between(geo_NORD[day:end].index,win_NORD[day:end].values,pv_NORD[day:end].values,facecolor = '#FCF100', alpha = 0.6, label = 'Photovoltaic')
    ax1.fill_between(geo_NORD[day:end].index,pv_NORD[day:end].values,hyd_NORD[day:end].values,facecolor = '#196AA2', alpha = 0.6, label = 'Large hydro')
    ax1.fill_between(geo_NORD[day:end].index,hyd_NORD[day:end].values,bio_NORD[day:end].values,facecolor = '#0E5801', alpha = 0.6, label = 'Bioenergy')
    ax1.fill_between(geo_NORD[day:end].index,bio_NORD[day:end].values,imp_NORD[day:end].values,facecolor = '#E68A31', alpha = 0.6, label = 'Imports')
    ax1.fill_between(geo_NORD[day:end].index,imp_NORD[day:end].values,oil_NORD[day:end].values,facecolor = '#4F1731', alpha = 0.6, label = 'Oil & other')
    ax1.fill_between(geo_NORD[day:end].index,oil_NORD[day:end].values,coa_NORD[day:end].values,facecolor = '#544848', alpha = 0.6, label = 'Coal')
    ax1.fill_between(geo_NORD[day:end].index,coa_NORD[day:end].values,gas_NORD[day:end].values,facecolor = '#9E8C8C', alpha = 0.6, label = 'CCGT')
    ax1.fill_between(geo_NORD[day:end].index,gas_NORD[day:end].values,pum_NORD[day:end].values,facecolor = '#4875A0', alpha = 0.6, label = 'Pumped hydro')
    ax1.fill_between(geo_NORD[day:end].index,pum_NORD[day:end].values,zon_NORD[day:end].values,facecolor = '#D00045', alpha = 0.6, label = 'Inter-zonal exchange')
    ax1.fill_between(geo_NORD[day:end].index,0,pch_NORD[day:end].values,facecolor = '#4875A0', alpha = 0.6)
    ax1.fill_between(geo_NORD[day:end].index,pch_NORD[day:end].values,zwx_NORD[day:end].values,facecolor = '#D00045', alpha = 0.6)
    lgd2 = ax1.legend(loc=1,  bbox_to_anchor=(2.70, 1.031))
    
    
    #ax2 = fig.add_subplot(322)
    ax2.set_title("CNOR", weight='bold')
    ax2.yaxis.tick_right()
    ax2.plot(loa_CNOR[day:end].index,loa_CNOR[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='Baseline load')
    #ax2.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax2.plot(geo_CNOR[day:end].index,geo_CNOR[day:end].values,'#873737', alpha=0.2)
    ax2.plot(ror_CNOR[day:end].index,ror_CNOR[day:end].values,'#00AFE7', alpha=0.2)
    ax2.plot(win_CNOR[day:end].index,win_CNOR[day:end].values,'#00E71F', alpha=0.2)
    ax2.plot(pv_CNOR[day:end].index,pv_CNOR[day:end].values,'#FCF100', alpha=0.2)
    ax2.plot(hyd_CNOR[day:end].index,hyd_CNOR[day:end].values,'#196AA2', alpha=0.2)
    ax2.plot(bio_CNOR[day:end].index,bio_CNOR[day:end].values,'#0E5801', alpha=0.2)
    ax2.plot(oil_CNOR[day:end].index,oil_CNOR[day:end].values,'#4F1731', alpha=0.2)        
    ax2.plot(coa_CNOR[day:end].index,coa_CNOR[day:end].values,'#544848', alpha=0.2)
    ax2.plot(gas_CNOR[day:end].index,gas_CNOR[day:end].values,'#9E8C8C', alpha=0.2)
    ax2.plot(imp_CNOR[day:end].index,imp_CNOR[day:end].values,'#E68A31', alpha=0.2)
    ax2.plot(pum_CNOR[day:end].index,pum_CNOR[day:end].values,'#4875A0', alpha=0.2)
    ax2.plot(zon_CNOR[day:end].index,zon_CNOR[day:end].values,'#D00045', alpha=0.2)
    ax2.plot(pch_CNOR[day:end].index,pch_CNOR[day:end].values,'#4875A0', alpha=0.2)
    ax2.plot(zwx_CNOR[day:end].index,zwx_CNOR[day:end].values,'#D00045', alpha=0.2)
    #ax2.set_ylabel('Power (GW)',labelpad = 11)
    #ax2.set_xlabel('UTC Time (hours)')
    #ax2.set_ylim(bottom = -2)
    ax2.margins(x=0)
    ax2.margins(y=0)
    #ax2.set_xticks(np.arange(0,24,3))
    #ax2.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax2.fill_between(geo_CNOR[day:end].index,0,geo_CNOR[day:end].values,facecolor = '#873737', alpha = 0.6, label = 'Geothermal')
    ax2.fill_between(geo_CNOR[day:end].index,geo_CNOR[day:end].values,ror_CNOR[day:end].values,facecolor = '#00AFE7', alpha = 0.6, label = 'Run-of-river')
    ax2.fill_between(geo_CNOR[day:end].index,ror_CNOR[day:end].values,win_CNOR[day:end].values,facecolor = '#00E71F', alpha = 0.6, label = 'Wind')
    ax2.fill_between(geo_CNOR[day:end].index,win_CNOR[day:end].values,pv_CNOR[day:end].values,facecolor = '#FCF100', alpha = 0.6, label = 'Photovoltaic')
    ax2.fill_between(geo_CNOR[day:end].index,pv_CNOR[day:end].values,hyd_CNOR[day:end].values,facecolor = '#196AA2', alpha = 0.6, label = 'Large hydro')
    ax2.fill_between(geo_CNOR[day:end].index,hyd_CNOR[day:end].values,bio_CNOR[day:end].values,facecolor = '#0E5801', alpha = 0.6, label = 'Bioenergy')
    ax2.fill_between(geo_CNOR[day:end].index,bio_CNOR[day:end].values,imp_CNOR[day:end].values,facecolor = '#E68A31', alpha = 0.6, label = 'Imports')
    ax2.fill_between(geo_CNOR[day:end].index,imp_CNOR[day:end].values,oil_CNOR[day:end].values,facecolor = '#4F1731', alpha = 0.6, label = 'Oil & other')
    ax2.fill_between(geo_CNOR[day:end].index,oil_CNOR[day:end].values,coa_CNOR[day:end].values,facecolor = '#544848', alpha = 0.6, label = 'Coal')
    ax2.fill_between(geo_CNOR[day:end].index,coa_CNOR[day:end].values,gas_CNOR[day:end].values,facecolor = '#9E8C8C', alpha = 0.6, label = 'CCGT')
    ax2.fill_between(geo_CNOR[day:end].index,gas_CNOR[day:end].values,pum_CNOR[day:end].values,facecolor = '#4875A0', alpha = 0.6, label = 'Pumped hydro')
    ax2.fill_between(geo_CNOR[day:end].index,pum_CNOR[day:end].values,zon_CNOR[day:end].values,facecolor = '#D00045', alpha = 0.6, label = 'Intra-zone import')
    ax2.fill_between(geo_CNOR[day:end].index,0,pch_CNOR[day:end].values,facecolor = '#4875A0', alpha = 0.6)
    ax2.fill_between(geo_CNOR[day:end].index,pch_CNOR[day:end].values,zwx_CNOR[day:end].values,facecolor = '#D00045', alpha = 0.6)
    
    #ax3 = fig.add_subplot(323)
    ax3.set_title("CSUD", weight='bold')
    ax3.plot(loa_CSUD[day:end].index,loa_CSUD[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='Baseline load')
    #ax3.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax3.plot(geo_CSUD[day:end].index,geo_CSUD[day:end].values,'#873737', alpha=0.2)
    ax3.plot(ror_CSUD[day:end].index,ror_CSUD[day:end].values,'#00AFE7', alpha=0.2)
    ax3.plot(win_CSUD[day:end].index,win_CSUD[day:end].values,'#00E71F', alpha=0.2)
    ax3.plot(pv_CSUD[day:end].index,pv_CSUD[day:end].values,'#FCF100', alpha=0.2)
    ax3.plot(hyd_CSUD[day:end].index,hyd_CSUD[day:end].values,'#196AA2', alpha=0.2)
    ax3.plot(bio_CSUD[day:end].index,bio_CSUD[day:end].values,'#0E5801', alpha=0.2)
    ax3.plot(oil_CSUD[day:end].index,oil_CSUD[day:end].values,'#4F1731', alpha=0.2)        
    ax3.plot(coa_CSUD[day:end].index,coa_CSUD[day:end].values,'#544848', alpha=0.2)
    ax3.plot(gas_CSUD[day:end].index,gas_CSUD[day:end].values,'#9E8C8C', alpha=0.2)
    ax3.plot(imp_CSUD[day:end].index,imp_CSUD[day:end].values,'#E68A31', alpha=0.2)
    ax3.plot(pum_CSUD[day:end].index,pum_CSUD[day:end].values,'#4875A0', alpha=0.2)
    ax3.plot(zon_CSUD[day:end].index,zon_CSUD[day:end].values,'#D00045', alpha=0.2)
    ax3.plot(pch_CSUD[day:end].index,pch_CSUD[day:end].values,'#4875A0', alpha=0.2)
    ax3.plot(zwx_CSUD[day:end].index,zwx_CSUD[day:end].values,'#D00045', alpha=0.2)
    ax3.set_ylabel('Power (GW)',labelpad = 11)
    #ax3.set_xlabel('UTC Time (hours)')
    #ax3.set_ylim(top = 35)
    ax3.margins(x=0)
    ax3.margins(y=0)
    #ax3.set_ylim(bottom = -2)
    #ax3.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    #ax3.fill_between(geo_CSUD[day:end].index,0,geo_CSUD[day:end].values,facecolor = '#873737', alpha = 0.6, label = 'Geothermal')
    ax3.fill_between(geo_CSUD[day:end].index,geo_CSUD[day:end].values,ror_CSUD[day:end].values,facecolor = '#00AFE7', alpha = 0.6, label = 'Run-of-river')
    ax3.fill_between(geo_CSUD[day:end].index,ror_CSUD[day:end].values,win_CSUD[day:end].values,facecolor = '#00E71F', alpha = 0.6, label = 'Wind')
    ax3.fill_between(geo_CSUD[day:end].index,win_CSUD[day:end].values,pv_CSUD[day:end].values,facecolor = '#FCF100', alpha = 0.6, label = 'Photovoltaic')
    ax3.fill_between(geo_CSUD[day:end].index,pv_CSUD[day:end].values,hyd_CSUD[day:end].values,facecolor = '#196AA2', alpha = 0.6, label = 'Large hydro')
    ax3.fill_between(geo_CSUD[day:end].index,hyd_CSUD[day:end].values,bio_CSUD[day:end].values,facecolor = '#0E5801', alpha = 0.6, label = 'Bioenergy')
    ax3.fill_between(geo_CSUD[day:end].index,bio_CSUD[day:end].values,imp_CSUD[day:end].values,facecolor = '#E68A31', alpha = 0.6, label = 'Imports')
    ax3.fill_between(geo_CSUD[day:end].index,imp_CSUD[day:end].values,oil_CSUD[day:end].values,facecolor = '#4F1731', alpha = 0.6, label = 'Oil & other')
    ax3.fill_between(geo_CSUD[day:end].index,oil_CSUD[day:end].values,coa_CSUD[day:end].values,facecolor = '#544848', alpha = 0.6, label = 'Coal')
    ax3.fill_between(geo_CSUD[day:end].index,coa_CSUD[day:end].values,gas_CSUD[day:end].values,facecolor = '#9E8C8C', alpha = 0.6, label = 'CCGT')
    ax3.fill_between(geo_CSUD[day:end].index,gas_CSUD[day:end].values,pum_CSUD[day:end].values,facecolor = '#4875A0', alpha = 0.6, label = 'Pumped hydro')
    ax3.fill_between(geo_CSUD[day:end].index,pum_CSUD[day:end].values,zon_CSUD[day:end].values,facecolor = '#D00045', alpha = 0.6, label = 'Intra-zone import')
    ax3.fill_between(geo_CSUD[day:end].index,0,pch_CSUD[day:end].values,facecolor = '#4875A0', alpha = 0.6)
    ax3.fill_between(geo_CSUD[day:end].index,pch_CSUD[day:end].values,zwx_CSUD[day:end].values,facecolor = '#D00045', alpha = 0.6)
                     
    #ax4 = fig.add_subplot(323)
    ax4.set_title("SUD", weight='bold')
    ax4.yaxis.tick_right()
    ax4.plot(loa_SUD[day:end].index,loa_SUD[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='Baseline load')
    #ax4.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax4.plot(geo_SUD[day:end].index,geo_SUD[day:end].values,'#873737', alpha=0.2)
    ax4.plot(ror_SUD[day:end].index,ror_SUD[day:end].values,'#00AFE7', alpha=0.2)
    ax4.plot(win_SUD[day:end].index,win_SUD[day:end].values,'#00E71F', alpha=0.2)
    ax4.plot(pv_SUD[day:end].index,pv_SUD[day:end].values,'#FCF100', alpha=0.2)
    ax4.plot(hyd_SUD[day:end].index,hyd_SUD[day:end].values,'#196AA2', alpha=0.2)
    ax4.plot(bio_SUD[day:end].index,bio_SUD[day:end].values,'#0E5801', alpha=0.2)
    ax4.plot(oil_SUD[day:end].index,oil_SUD[day:end].values,'#4F1731', alpha=0.2)        
    ax4.plot(coa_SUD[day:end].index,coa_SUD[day:end].values,'#544848', alpha=0.2)
    ax4.plot(gas_SUD[day:end].index,gas_SUD[day:end].values,'#9E8C8C', alpha=0.2)
    ax4.plot(imp_SUD[day:end].index,imp_SUD[day:end].values,'#E68A31', alpha=0.2)
    ax4.plot(pum_SUD[day:end].index,pum_SUD[day:end].values,'#4875A0', alpha=0.2)
    ax4.plot(zon_SUD[day:end].index,zon_SUD[day:end].values,'#D00045', alpha=0.2)
    ax4.plot(pch_SUD[day:end].index,pch_SUD[day:end].values,'#4875A0', alpha=0.2)
    ax4.plot(zwx_SUD[day:end].index,zwx_SUD[day:end].values,'#D00045', alpha=0.2)
    #ax4.set_ylabel('Power (GW)',labelpad = 11)
    #ax4.set_xlabel('UTC Time (hours)')
    #ax4.set_ylim(top = 35)
    #ax4.set_ylim(bottom = -2)
    ax4.margins(x=0)
    ax4.margins(y=0)
    #ax4.set_xticks(np.arange(0,24,3))
    #ax4.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax4.fill_between(geo_SUD[day:end].index,0,geo_SUD[day:end].values,facecolor = '#873737', alpha = 0.6, label = 'Geothermal')
    ax4.fill_between(geo_SUD[day:end].index,geo_SUD[day:end].values,ror_SUD[day:end].values,facecolor = '#00AFE7', alpha = 0.6, label = 'Run-of-river')
    ax4.fill_between(geo_SUD[day:end].index,ror_SUD[day:end].values,win_SUD[day:end].values,facecolor = '#00E71F', alpha = 0.6, label = 'Wind')
    ax4.fill_between(geo_SUD[day:end].index,win_SUD[day:end].values,pv_SUD[day:end].values,facecolor = '#FCF100', alpha = 0.6, label = 'Photovoltaic')
    ax4.fill_between(geo_SUD[day:end].index,pv_SUD[day:end].values,hyd_SUD[day:end].values,facecolor = '#196AA2', alpha = 0.6, label = 'Large hydro')
    ax4.fill_between(geo_SUD[day:end].index,hyd_SUD[day:end].values,bio_SUD[day:end].values,facecolor = '#0E5801', alpha = 0.6, label = 'Bioenergy')
    ax4.fill_between(geo_SUD[day:end].index,bio_SUD[day:end].values,imp_SUD[day:end].values,facecolor = '#E68A31', alpha = 0.6, label = 'Imports')
    ax4.fill_between(geo_SUD[day:end].index,imp_SUD[day:end].values,oil_SUD[day:end].values,facecolor = '#4F1731', alpha = 0.6, label = 'Oil & other')
    ax4.fill_between(geo_SUD[day:end].index,oil_SUD[day:end].values,coa_SUD[day:end].values,facecolor = '#544848', alpha = 0.6, label = 'Coal')
    ax4.fill_between(geo_SUD[day:end].index,coa_SUD[day:end].values,gas_SUD[day:end].values,facecolor = '#9E8C8C', alpha = 0.6, label = 'CCGT')
    ax4.fill_between(geo_SUD[day:end].index,gas_SUD[day:end].values,pum_SUD[day:end].values,facecolor = '#4875A0', alpha = 0.6, label = 'Pumped hydro')
    ax4.fill_between(geo_SUD[day:end].index,pum_SUD[day:end].values,zon_SUD[day:end].values,facecolor = '#D00045', alpha = 0.6, label = 'Intra-zone import')
    ax4.fill_between(geo_SUD[day:end].index,0,pch_SUD[day:end].values,facecolor = '#4875A0', alpha = 0.6)
    ax4.fill_between(geo_SUD[day:end].index,pch_SUD[day:end].values,zwx_SUD[day:end].values,facecolor = '#D00045', alpha = 0.6)
                     
    #ax5 = fig.add_subplot(323)
    ax5.set_title("SARD", weight='bold')
    ax5.plot(loa_SARD[day:end].index,loa_SARD[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='Baseline load')
    #ax5.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax5.plot(geo_SARD[day:end].index,geo_SARD[day:end].values,'#873737', alpha=0.2)
    ax5.plot(ror_SARD[day:end].index,ror_SARD[day:end].values,'#00AFE7', alpha=0.2)
    ax5.plot(win_SARD[day:end].index,win_SARD[day:end].values,'#00E71F', alpha=0.2)
    ax5.plot(pv_SARD[day:end].index,pv_SARD[day:end].values,'#FCF100', alpha=0.2)
    ax5.plot(hyd_SARD[day:end].index,hyd_SARD[day:end].values,'#196AA2', alpha=0.2)
    ax5.plot(bio_SARD[day:end].index,bio_SARD[day:end].values,'#0E5801', alpha=0.2)
    ax5.plot(oil_SARD[day:end].index,oil_SARD[day:end].values,'#4F1731', alpha=0.2)        
    ax5.plot(coa_SARD[day:end].index,coa_SARD[day:end].values,'#544848', alpha=0.2)
    ax5.plot(gas_SARD[day:end].index,gas_SARD[day:end].values,'#9E8C8C', alpha=0.2)
    ax5.plot(imp_SARD[day:end].index,imp_SARD[day:end].values,'#E68A31', alpha=0.2)
    ax5.plot(pum_SARD[day:end].index,pum_SARD[day:end].values,'#4875A0', alpha=0.2)
    ax5.plot(zon_SARD[day:end].index,zon_SARD[day:end].values,'#D00045', alpha=0.2)
    ax5.plot(pch_SARD[day:end].index,pch_SARD[day:end].values,'#4875A0', alpha=0.2)
    ax5.plot(zwx_SARD[day:end].index,zwx_SARD[day:end].values,'#D00045', alpha=0.2)
    ax5.set_ylabel('Power (GW)',labelpad = 11)
    ax5.set_xlabel('UTC Time (hours)')
    #ax5.set_ylim(bottom = -2)
    ax5.margins(x=0)
    ax5.margins(y=0)
    #ax5.set_xticks(np.arange(0,24,3))
    #ax5.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax5.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax5.xaxis.set_major_formatter(plt.FixedFormatter(['','day1','day2','day3','day4','day5','day6']))
    ax5.fill_between(geo_SARD[day:end].index,0,geo_SARD[day:end].values,facecolor = '#873737', alpha = 0.6, label = 'Geothermal')
    ax5.fill_between(geo_SARD[day:end].index,geo_SARD[day:end].values,ror_SARD[day:end].values,facecolor = '#00AFE7', alpha = 0.6, label = 'Run-of-river')
    ax5.fill_between(geo_SARD[day:end].index,ror_SARD[day:end].values,win_SARD[day:end].values,facecolor = '#00E71F', alpha = 0.6, label = 'Wind')
    ax5.fill_between(geo_SARD[day:end].index,win_SARD[day:end].values,pv_SARD[day:end].values,facecolor = '#FCF100', alpha = 0.6, label = 'Photovoltaic')
    ax5.fill_between(geo_SARD[day:end].index,pv_SARD[day:end].values,hyd_SARD[day:end].values,facecolor = '#196AA2', alpha = 0.6, label = 'Large hydro')
    ax5.fill_between(geo_SARD[day:end].index,hyd_SARD[day:end].values,bio_SARD[day:end].values,facecolor = '#0E5801', alpha = 0.6, label = 'Bioenergy')
    ax5.fill_between(geo_SARD[day:end].index,bio_SARD[day:end].values,imp_SARD[day:end].values,facecolor = '#E68A31', alpha = 0.6, label = 'Imports')
    ax5.fill_between(geo_SARD[day:end].index,imp_SARD[day:end].values,oil_SARD[day:end].values,facecolor = '#4F1731', alpha = 0.6, label = 'Oil & other')
    ax5.fill_between(geo_SARD[day:end].index,oil_SARD[day:end].values,coa_SARD[day:end].values,facecolor = '#544848', alpha = 0.6, label = 'Coal')
    ax5.fill_between(geo_SARD[day:end].index,coa_SARD[day:end].values,gas_SARD[day:end].values,facecolor = '#9E8C8C', alpha = 0.6, label = 'CCGT')
    ax5.fill_between(geo_SARD[day:end].index,gas_SARD[day:end].values,pum_SARD[day:end].values,facecolor = '#4875A0', alpha = 0.6, label = 'Pumped hydro')
    ax5.fill_between(geo_SARD[day:end].index,pum_SARD[day:end].values,zon_SARD[day:end].values,facecolor = '#D00045', alpha = 0.6, label = 'Intra-zone import')
    ax5.fill_between(geo_SARD[day:end].index,0,pch_SARD[day:end].values,facecolor = '#4875A0', alpha = 0.6)
    ax5.fill_between(geo_SARD[day:end].index,pch_SARD[day:end].values,zwx_SARD[day:end].values,facecolor = '#D00045', alpha = 0.6)
                     
    #ax5 = fig.add_subplot(323)
    ax6.yaxis.tick_right()
    ax6.set_title("SICI", weight='bold')
    ax6.plot(loa_SICI[day:end].index,loa_SICI[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='Baseline load')
    #ax6.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax6.plot(geo_SICI[day:end].index,geo_SICI[day:end].values,'#873737', alpha=0.2)
    ax6.plot(ror_SICI[day:end].index,ror_SICI[day:end].values,'#00AFE7', alpha=0.2)
    ax6.plot(win_SICI[day:end].index,win_SICI[day:end].values,'#00E71F', alpha=0.2)
    ax6.plot(pv_SICI[day:end].index,pv_SICI[day:end].values,'#FCF100', alpha=0.2)
    ax6.plot(hyd_SICI[day:end].index,hyd_SICI[day:end].values,'#196AA2', alpha=0.2)
    ax6.plot(bio_SICI[day:end].index,bio_SICI[day:end].values,'#0E5801', alpha=0.2)
    ax6.plot(oil_SICI[day:end].index,oil_SICI[day:end].values,'#4F1731', alpha=0.2)        
    ax6.plot(coa_SICI[day:end].index,coa_SICI[day:end].values,'#544848', alpha=0.2)
    ax6.plot(gas_SICI[day:end].index,gas_SICI[day:end].values,'#9E8C8C', alpha=0.2)
    ax6.plot(imp_SICI[day:end].index,imp_SICI[day:end].values,'#E68A31', alpha=0.2)
    ax6.plot(pum_SICI[day:end].index,pum_SICI[day:end].values,'#4875A0', alpha=0.2)
    ax6.plot(zon_SICI[day:end].index,zon_SICI[day:end].values,'#D00045', alpha=0.2)
    ax6.plot(pch_SICI[day:end].index,pch_SICI[day:end].values,'#4875A0', alpha=0.2)
    ax6.plot(zwx_SICI[day:end].index,zwx_SICI[day:end].values,'#D00045', alpha=0.2)
    #ax6.set_ylabel('Power (GW)',labelpad = 11)
    ax6.set_xlabel('UTC Time (hours)')
    #ax6.set_ylim(bottom = -2)
    ax6.margins(x=0)
    ax6.margins(y=0)
    #ax6.set_xticks(np.arange(day,end,dtype='datetime64[h]'))
    #ax6.set_xticklabels(np.arange(0,len(np.arange(day,end,dtype='datetime64[h]'))))
    ax6.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax6.xaxis.set_major_formatter(plt.FixedFormatter(['','day1','day2','day3','day4','day5','day6']))
    ax6.fill_between(geo_SICI[day:end].index,0,geo_SICI[day:end].values,facecolor = '#873737', alpha = 0.6, label = 'Geothermal')
    ax6.fill_between(geo_SICI[day:end].index,geo_SICI[day:end].values,ror_SICI[day:end].values,facecolor = '#00AFE7', alpha = 0.6, label = 'Run-of-river')
    ax6.fill_between(geo_SICI[day:end].index,ror_SICI[day:end].values,win_SICI[day:end].values,facecolor = '#00E71F', alpha = 0.6, label = 'Wind')
    ax6.fill_between(geo_SICI[day:end].index,win_SICI[day:end].values,pv_SICI[day:end].values,facecolor = '#FCF100', alpha = 0.6, label = 'Photovoltaic')
    ax6.fill_between(geo_SICI[day:end].index,pv_SICI[day:end].values,hyd_SICI[day:end].values,facecolor = '#196AA2', alpha = 0.6, label = 'Large hydro')
    ax6.fill_between(geo_SICI[day:end].index,hyd_SICI[day:end].values,bio_SICI[day:end].values,facecolor = '#0E5801', alpha = 0.6, label = 'Bioenergy')
    ax6.fill_between(geo_SICI[day:end].index,bio_SICI[day:end].values,imp_SICI[day:end].values,facecolor = '#E68A31', alpha = 0.6, label = 'Imports')
    ax6.fill_between(geo_SICI[day:end].index,imp_SICI[day:end].values,oil_SICI[day:end].values,facecolor = '#4F1731', alpha = 0.6, label = 'Oil & other')
    ax6.fill_between(geo_SICI[day:end].index,oil_SICI[day:end].values,coa_SICI[day:end].values,facecolor = '#544848', alpha = 0.6, label = 'Coal')
    ax6.fill_between(geo_SICI[day:end].index,coa_SICI[day:end].values,gas_SICI[day:end].values,facecolor = '#9E8C8C', alpha = 0.6, label = 'CCGT')
    ax6.fill_between(geo_SICI[day:end].index,gas_SICI[day:end].values,pum_SICI[day:end].values,facecolor = '#4875A0', alpha = 0.6, label = 'Pumped hydro')
    ax6.fill_between(geo_SICI[day:end].index,pum_SICI[day:end].values,zon_SICI[day:end].values,facecolor = '#D00045', alpha = 0.6, label = 'Intra-zone import')
    ax6.fill_between(geo_SICI[day:end].index,0,pch_SICI[day:end].values,facecolor = '#4875A0', alpha = 0.6)
    ax6.fill_between(geo_SICI[day:end].index,pch_SICI[day:end].values,zwx_SICI[day:end].values,facecolor = '#D00045', alpha = 0.6)                         
    

#%% 
'''
Multi-zone DHW Graph pre-processing
'''
def dhw_plot(model_test, start, stop):
    ashp_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ashp','carriers':'dhw','locs':['R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    ashp_con_NORD = model_test.get_formatted_array('carrier_con').loc[{'techs':'ashp','carriers':'electricity','locs':['R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    dhw_loa_NORD = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_heat','carriers':'dhw','locs':['R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    tes_out_NORD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'tes','carriers':'dhw','locs':['R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    tes_in_NORD = model_test.get_formatted_array('carrier_con').loc[{'techs':'tes','carriers':'dhw','locs':['R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    tes_ou_NORD = tes_out_NORD+tes_in_NORD
    tes_ou_NORD[tes_ou_NORD<0]=0
    tes_ii_NORD = tes_out_NORD+tes_in_NORD
    tes_ii_NORD[tes_ii_NORD>0]=0
    tes_NORD_cap = model_test.get_formatted_array('storage').loc[{'techs':'tes','locs':['R1','R2','R3','R4','R5','R6','R7','R8']}].sum('locs').to_pandas().T
    
    hp_NORD = ashp_NORD/1000000
    hp_con_NORD = -ashp_con_NORD/1000000
    tes_o_NORD = hp_NORD + tes_ou_NORD/1000000
    tes_i_NORD = tes_ii_NORD/1000000
    dhw_NORD = dhw_loa_NORD/1000000
    
    ashp_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ashp','carriers':'dhw','locs':['R9','R10','R11']}].sum('locs').to_pandas().T
    ashp_con_CNOR = model_test.get_formatted_array('carrier_con').loc[{'techs':'ashp','carriers':'electricity','locs':['R9','R10','R11']}].sum('locs').to_pandas().T
    dhw_loa_CNOR = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_heat','carriers':'dhw','locs':['R9','R10','R11']}].sum('locs').to_pandas().T
    tes_out_CNOR = model_test.get_formatted_array('carrier_prod').loc[{'techs':'tes','carriers':'dhw','locs':['R9','R10','R11']}].sum('locs').to_pandas().T
    tes_in_CNOR = model_test.get_formatted_array('carrier_con').loc[{'techs':'tes','carriers':'dhw','locs':['R9','R10','R11']}].sum('locs').to_pandas().T
    tes_ou_CNOR = tes_out_CNOR+tes_in_CNOR
    tes_ou_CNOR[tes_ou_CNOR<0]=0
    tes_ii_CNOR = tes_out_CNOR+tes_in_CNOR
    tes_ii_CNOR[tes_ii_CNOR>0]=0
    tes_CNOR_cap = model_test.get_formatted_array('storage').loc[{'techs':'tes','locs':['R9','R10','R11']}].sum('locs').to_pandas().T
    
    hp_CNOR = ashp_CNOR/1000000
    hp_con_CNOR = -ashp_con_CNOR/1000000
    tes_o_CNOR = hp_CNOR + tes_ou_CNOR/1000000
    tes_i_CNOR = tes_ii_CNOR/1000000
    dhw_CNOR = dhw_loa_CNOR/1000000
    
    ashp_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ashp','carriers':'dhw','locs':['R12','R13','R14']}].sum('locs').to_pandas().T
    ashp_con_CSUD = model_test.get_formatted_array('carrier_con').loc[{'techs':'ashp','carriers':'electricity','locs':['R12','R13','R14']}].sum('locs').to_pandas().T
    dhw_loa_CSUD = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_heat','carriers':'dhw','locs':['R12','R13','R14']}].sum('locs').to_pandas().T
    tes_out_CSUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'tes','carriers':'dhw','locs':['R12','R13','R14']}].sum('locs').to_pandas().T
    tes_in_CSUD = model_test.get_formatted_array('carrier_con').loc[{'techs':'tes','carriers':'dhw','locs':['R12','R13','R14']}].sum('locs').to_pandas().T
    tes_ou_CSUD = tes_out_CSUD+tes_in_CSUD
    tes_ou_CSUD[tes_ou_CSUD<0]=0
    tes_ii_CSUD = tes_out_CSUD+tes_in_CSUD
    tes_ii_CSUD[tes_ii_CSUD>0]=0
    tes_CSUD_cap = model_test.get_formatted_array('storage').loc[{'techs':'tes','locs':['R12','R13','R14']}].sum('locs').to_pandas().T
    
    hp_CSUD = ashp_CSUD/1000000
    hp_con_CSUD = -ashp_con_CSUD/1000000
    tes_o_CSUD = hp_CSUD + tes_ou_CSUD/1000000
    tes_i_CSUD = tes_ii_CSUD/1000000
    dhw_CSUD = dhw_loa_CSUD/1000000
    
    ashp_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ashp','carriers':'dhw','locs':['R15','R16','R17','R18']}].sum('locs').to_pandas().T
    ashp_con_SUD = model_test.get_formatted_array('carrier_con').loc[{'techs':'ashp','carriers':'electricity','locs':['R15','R16','R17','R18']}].sum('locs').to_pandas().T
    dhw_loa_SUD = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_heat','carriers':'dhw','locs':['R15','R16','R17','R18']}].sum('locs').to_pandas().T
    tes_out_SUD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'tes','carriers':'dhw','locs':['R15','R16','R17','R18']}].sum('locs').to_pandas().T
    tes_in_SUD = model_test.get_formatted_array('carrier_con').loc[{'techs':'tes','carriers':'dhw','locs':['R15','R16','R17','R18']}].sum('locs').to_pandas().T
    tes_ou_SUD = tes_out_SUD+tes_in_SUD
    tes_ou_SUD[tes_ou_SUD<0]=0
    tes_ii_SUD = tes_out_SUD+tes_in_SUD
    tes_ii_SUD[tes_ii_SUD>0]=0
    tes_SUD_cap = model_test.get_formatted_array('storage').loc[{'techs':'tes','locs':['R15','R16','R17','R18']}].sum('locs').to_pandas().T
    
    hp_SUD = ashp_SUD/1000000
    hp_con_SUD = -ashp_con_SUD/1000000
    tes_o_SUD = hp_SUD + tes_ou_SUD/1000000
    tes_i_SUD = tes_ii_SUD/1000000
    dhw_SUD = dhw_loa_SUD/1000000
    
    ashp_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ashp','carriers':'dhw','locs':['SARD']}].sum('locs').to_pandas().T
    ashp_con_SARD = model_test.get_formatted_array('carrier_con').loc[{'techs':'ashp','carriers':'electricity','locs':['SARD']}].sum('locs').to_pandas().T
    dhw_loa_SARD = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_heat','carriers':'dhw','locs':['SARD']}].sum('locs').to_pandas().T
    tes_out_SARD = model_test.get_formatted_array('carrier_prod').loc[{'techs':'tes','carriers':'dhw','locs':['SARD']}].sum('locs').to_pandas().T
    tes_in_SARD = model_test.get_formatted_array('carrier_con').loc[{'techs':'tes','carriers':'dhw','locs':['SARD']}].sum('locs').to_pandas().T
    tes_ou_SARD = tes_out_SARD+tes_in_SARD
    tes_ou_SARD[tes_ou_SARD<0]=0
    tes_ii_SARD = tes_out_SARD+tes_in_SARD
    tes_ii_SARD[tes_ii_SARD>0]=0
    tes_SARD_cap = model_test.get_formatted_array('storage').loc[{'techs':'tes','locs':['SARD']}].sum('locs').to_pandas().T
    
    hp_SARD = ashp_SARD/1000000
    hp_con_SARD = -ashp_con_SARD/1000000
    tes_o_SARD = hp_SARD + tes_ou_SARD/1000000
    tes_i_SARD = tes_ii_SARD/1000000
    dhw_SARD = dhw_loa_SARD/1000000
    
    ashp_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'ashp','carriers':'dhw','locs':['SICI']}].sum('locs').to_pandas().T
    ashp_con_SICI = model_test.get_formatted_array('carrier_con').loc[{'techs':'ashp','carriers':'electricity','locs':['SICI']}].sum('locs').to_pandas().T
    dhw_loa_SICI = -model_test.get_formatted_array('carrier_con').loc[{'techs':'demand_heat','carriers':'dhw','locs':['SICI']}].sum('locs').to_pandas().T
    tes_out_SICI = model_test.get_formatted_array('carrier_prod').loc[{'techs':'tes','carriers':'dhw','locs':['SICI']}].sum('locs').to_pandas().T
    tes_in_SICI = model_test.get_formatted_array('carrier_con').loc[{'techs':'tes','carriers':'dhw','locs':['SICI']}].sum('locs').to_pandas().T
    tes_ou_SICI = tes_out_SICI+tes_in_SICI
    tes_ou_SICI[tes_ou_SICI<0]=0
    tes_ii_SICI = tes_out_SICI+tes_in_SICI
    tes_ii_SICI[tes_ii_SICI>0]=0
    tes_SICI_cap = model_test.get_formatted_array('storage').loc[{'techs':'tes','locs':['SICI']}].sum('locs').to_pandas().T
    
    hp_SICI = ashp_SICI/1000000
    hp_con_SICI = -ashp_con_SICI/1000000
    tes_o_SICI = hp_SICI + tes_ou_SICI/1000000
    tes_i_SICI = tes_ii_SICI/1000000
    dhw_SICI = dhw_loa_SICI/1000000

    #%% 
    '''
    Bidding-zone DHW plots
    '''
    
    day = start #'2015-01-01 00:00:00'
    end = stop #'2015-01-07 23:00:00'
    #fig = plt.figure(figsize=(10,6))
    fig, ((ax1, ax2), (ax3,ax4),(ax5,ax6)) = plt.subplots(3,2, sharex='col', gridspec_kw = {'height_ratios':[1,1,1], 'wspace':0.1, 'hspace':0.2}, figsize=(12,10))
    
    #ax1 = fig.add_subplot(321)
    ax1.set_title("NORD", weight='bold')
    ax1.plot(dhw_NORD[day:end].index,dhw_NORD[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
    #ax1.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax1.plot(hp_NORD[day:end].index,hp_NORD[day:end].values,'#EC3623', alpha=0.2)
    ax1.plot(tes_o_NORD[day:end].index,tes_o_NORD[day:end].values,'#EC8123', alpha=0.2)
    ax1.plot(tes_i_NORD[day:end].index,tes_i_NORD[day:end].values,'#EC8123', alpha=0.2)
    ax1.plot(hp_con_NORD[day:end].index,hp_con_NORD[day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
    ax1.set_ylabel('Power (GW)',labelpad = 11)
    #ax1.set_xlabel('UTC Time (hours)')
    #ax1.set_ylim(ymax = 28)
    ax1.margins(x=0)
    ax1.margins(y=0)
    #ax1.set_xticks(np.arange(0,24,3))
    #ax1.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax1.fill_between(dhw_NORD[day:end].index,0,hp_NORD[day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
    ax1.fill_between(dhw_NORD[day:end].index,hp_NORD[day:end].values,tes_o_NORD[day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
    ax1.fill_between(dhw_NORD[day:end].index,0,tes_i_NORD[day:end].values,facecolor = '#EC8123', alpha = 0.6)
    lgd2 = ax1.legend(loc=1,  bbox_to_anchor=(2.90, 1.031))
    
    #ax2 = fig.add_subplot(321)
    ax2.yaxis.tick_right()
    ax2.set_title("CNOR", weight='bold')
    ax2.plot(dhw_CNOR[day:end].index,dhw_CNOR[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
    #ax2.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax2.plot(hp_CNOR[day:end].index,hp_CNOR[day:end].values,'#EC3623', alpha=0.2)
    ax2.plot(tes_o_CNOR[day:end].index,tes_o_CNOR[day:end].values,'#EC8123', alpha=0.2)
    ax2.plot(tes_i_CNOR[day:end].index,tes_i_CNOR[day:end].values,'#EC8123', alpha=0.2)
    ax2.plot(hp_con_CNOR[day:end].index,hp_con_CNOR[day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
    #ax2.set_ylabel('Power (GW)',labelpad = 11)
    #ax2.set_xlabel('UTC Time (hours)')
    #ax2.set_ylim(ymax = 28)
    ax2.margins(x=0)
    ax2.margins(y=0)
    #ax2.set_xticks(np.arange(0,24,3))
    #ax2.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax2.fill_between(dhw_CNOR[day:end].index,0,hp_CNOR[day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
    ax2.fill_between(dhw_CNOR[day:end].index,hp_CNOR[day:end].values,tes_o_CNOR[day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
    ax2.fill_between(dhw_CNOR[day:end].index,0,tes_i_CNOR[day:end].values,facecolor = '#EC8123', alpha = 0.6)
    
    #ax3 = fig.add_subplot(321)
    ax3.set_title("CSUD", weight='bold')
    ax3.plot(dhw_CSUD[day:end].index,dhw_CSUD[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
    #ax3.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax3.plot(hp_CSUD[day:end].index,hp_CSUD[day:end].values,'#EC3623', alpha=0.2)
    ax3.plot(tes_o_CSUD[day:end].index,tes_o_CSUD[day:end].values,'#EC8123', alpha=0.2)
    ax3.plot(tes_i_CSUD[day:end].index,tes_i_CSUD[day:end].values,'#EC8123', alpha=0.2)
    ax3.plot(hp_con_CSUD[day:end].index,hp_con_CSUD[day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
    ax3.set_ylabel('Power (GW)',labelpad = 11)
    #ax3.set_xlabel('UTC Time (hours)')
    #ax3.set_ylim(ymax = 28)
    ax3.margins(x=0)
    ax3.margins(y=0)
    #ax3.set_xticks(np.arange(0,24,3))
    #ax3.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax3.fill_between(dhw_CSUD[day:end].index,0,hp_CSUD[day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
    ax3.fill_between(dhw_CSUD[day:end].index,hp_CSUD[day:end].values,tes_o_CSUD[day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
    ax3.fill_between(dhw_CSUD[day:end].index,0,tes_i_CSUD[day:end].values,facecolor = '#EC8123', alpha = 0.6)
    
    #ax4 = fig.add_subplot(321)
    ax4.yaxis.tick_right()
    ax4.set_title("SUD", weight='bold')
    ax4.plot(dhw_SUD[day:end].index,dhw_SUD[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
    #ax4.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax4.plot(hp_SUD[day:end].index,hp_SUD[day:end].values,'#EC3623', alpha=0.2)
    ax4.plot(tes_o_SUD[day:end].index,tes_o_SUD[day:end].values,'#EC8123', alpha=0.2)
    ax4.plot(tes_i_SUD[day:end].index,tes_i_SUD[day:end].values,'#EC8123', alpha=0.2)
    ax4.plot(hp_con_SUD[day:end].index,hp_con_SUD[day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
    #ax4.set_ylabel('Power (GW)',labelpad = 11)
    #ax4.set_xlabel('UTC Time (hours)')
    #ax4.set_ylim(ymax = 28)
    ax4.margins(x=0)
    ax4.margins(y=0)
    #ax4.set_xticks(np.arange(0,24,3))
    #ax4.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax4.fill_between(dhw_SUD[day:end].index,0,hp_SUD[day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
    ax4.fill_between(dhw_SUD[day:end].index,hp_SUD[day:end].values,tes_o_SUD[day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
    ax4.fill_between(dhw_SUD[day:end].index,0,tes_i_SUD[day:end].values,facecolor = '#EC8123', alpha = 0.6)
    
    #ax5 = fig.add_subplot(321)
    ax5.set_title("SARD", weight='bold')
    ax5.plot(dhw_SARD[day:end].index,dhw_SARD[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
    #ax5.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax5.plot(hp_SARD[day:end].index,hp_SARD[day:end].values,'#EC3623', alpha=0.2)
    ax5.plot(tes_o_SARD[day:end].index,tes_o_SARD[day:end].values,'#EC8123', alpha=0.2)
    ax5.plot(tes_i_SARD[day:end].index,tes_i_SARD[day:end].values,'#EC8123', alpha=0.2)
    ax5.plot(hp_con_SARD[day:end].index,hp_con_SARD[day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
    ax5.set_ylabel('Power (GW)',labelpad = 11)
    #ax5.set_xlabel('UTC Time (hours)')
    #ax5.set_ylim(ymax = 28)
    ax5.margins(x=0)
    ax5.margins(y=0)
    ax5.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax5.xaxis.set_major_formatter(plt.FixedFormatter(['','day1','day2','day3','day4','day5','day6']))
    #ax5.set_xticks(np.arange(0,24,3))
    #ax5.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax5.fill_between(dhw_SARD[day:end].index,0,hp_SARD[day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
    ax5.fill_between(dhw_SARD[day:end].index,hp_SARD[day:end].values,tes_o_SARD[day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
    ax5.fill_between(dhw_SARD[day:end].index,0,tes_i_SARD[day:end].values,facecolor = '#EC8123', alpha = 0.6)
    
    #ax6 = fig.add_subplot(321)
    ax6.yaxis.tick_right()
    ax6.set_title("SICI", weight='bold')
    ax6.plot(dhw_SICI[day:end].index,dhw_SICI[day:end].values,'#000000', alpha=0.5, linestyle = '-', label ='DHW loads')
    #ax6.plot(loa2[day:end].index,loa2[day:end].values,'#000000', alpha=1, label = 'New load')
    ax6.plot(hp_SICI[day:end].index,hp_SICI[day:end].values,'#EC3623', alpha=0.2)
    ax6.plot(tes_o_SICI[day:end].index,tes_o_SICI[day:end].values,'#EC8123', alpha=0.2)
    ax6.plot(tes_i_SICI[day:end].index,tes_i_SICI[day:end].values,'#EC8123', alpha=0.2)
    ax6.plot(hp_con_SICI[day:end].index,hp_con_SICI[day:end].values,'b', alpha=0.8, linestyle = ':', label ='Electricity consumption')
    #ax6.set_ylabel('Power (GW)',labelpad = 11)
    #ax6.set_xlabel('UTC Time (hours)')
    #ax6.set_ylim(ymax = 28)
    ax6.margins(x=0)
    ax6.margins(y=0)
    ax6.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax6.xaxis.set_major_formatter(plt.FixedFormatter(['','day1','day2','day3','day4','day5','day6']))
    #ax6.set_xticks(np.arange(0,24,3))
    #ax6.set_xticklabels(['0','3','6','9','12','15','18','21','24'])
    ax6.fill_between(dhw_SICI[day:end].index,0,hp_SICI[day:end].values,facecolor = '#EC3623', alpha = 0.6, label = 'Heat Pumps')
    ax6.fill_between(dhw_SICI[day:end].index,hp_SICI[day:end].values,tes_o_SICI[day:end].values,facecolor = '#EC8123', alpha = 0.6, label = 'Thermal Energy Storage')
    ax6.fill_between(dhw_SICI[day:end].index,0,tes_i_SICI[day:end].values,facecolor = '#EC8123', alpha = 0.6)
