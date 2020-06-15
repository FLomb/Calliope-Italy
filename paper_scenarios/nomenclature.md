# Calliope-Italy paper scenarios
The scenarios contained in this folder allow to reproduce the results featuring the key publication associated with the model: "*Francesco Lombardi, Bryn Pickering, Emanuela Colombo, Stefan Pfenninger, Policy decision support for renewables deployment through spatially explicit practically optimal alternatives, [Unpublished]* ".

## Nomenclature
- reference:				reference scenario, timeseries related to PV, Wind and Wind offshore related to 2016 (most-typical year)
- weather_year_1989:		change of the timeseries related to PV, Wind and Wind offshore to 1989 (worst weather year) 
- weather_year_2010:		change of the timeseries related to PV, Wind and Wind offshore to 2010 (best weather year) 
- high/low_p2g_costs:		change of cost assumptions for Power-to-gas technologies (electrolysers, methanation with direct air capture)
- high/low_vres_bat_costs:	change of cost assumptions for renewables and battery storage

Demand sensitivity scenarios can be run from any of these by applying the corresponding override (see "overrides.yaml" in each folder).
Cost relaxation can be managed as a parameter in the spores_run script.

**Please notice that all timeseries are indexed to 2015, irrespective of the weather year adopted** (as it can be seen from the folder "full_list_of_weather_years", which allows to select any year in the range 1981-2016 but always indexed to 2015).
This is done because the original model was tested and validated against 2015 data from the Italian TSO; since then, all timeseries are reindexed to 2015 to make the overriding easier.
