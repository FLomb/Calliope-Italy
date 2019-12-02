# Calliope-Italy
Calliope-based 20-region representation of the Italian electric energy system, including both current and 2050 technological options.
The model also features the possibility to generate *spatially-explicit practically-optimal results* (SPORES).

## Requirements
The model is built on the Python-based open-source energy modelling framework Calliope, version 0.6.4. 

To run the model, it is recommended to follow the [instructions for installing Calliope](https://calliope.readthedocs.io/en/stable/user/installation.html).

## Overview
All input data are and model specification are in the Model folder. In particular, timeseries data are in the 'timeseries_data' sub-folder, whilst location and tech specifications are the 'model_config' sub-folder.

To run the model over a week of data for testing:
- select the 'subset_time' of interest in the model.yaml file
- run the spores_model_run.py file

## Italian 20-region energy system

<img src="https://github.com/FLomb/Calliope-Italy/blob/master/italy_model_map.png" width="600">

## Citing
If you use the Italian model or the related data, please cite the associated publication: "*Francesco Lombardi, Bryn Pickering, Emanuela Colombo, Stefan Pfenninger, Spatially explicit practically optimal results in a fully decarbonised energy system, Unpublished* "

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
