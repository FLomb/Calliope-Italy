# Calliope-Italy
Calliope-based 20-region representation of the Italian electric energy system, for the reference year 2015.
The model also features the possibility to simulate scenarios of high penetration of power-to-heat technologies for DHW production.

## Requirements
The model is built on the Python-based open-source energy modelling framework Calliope, version 0.6.4. 

To run the model, it is recommended to follow the [instructions for installing Calliope](https://calliope.readthedocs.io/en/stable/user/installation.html).

## Overview
All input data are and model specification are in the Model folder. In particular, timeseries data are in the 'timeseries_data' sub-folder, whilst location and tech specifications are the 'model_config' sub-folder.

To run the model over a week of data for testing:
- select the 'subset_time' of interest in the model.yaml file
- run the model_run.py file

## Italian 20-region energy system

<img src="https://github.com/FLomb/Calliope-Italy/blob/ECOS_2020/italy_model_map.png" width="600">

## Author
Francesco Lombardi </br>
E-mail: francesco.lombardi@polimi.it </br>
Politecnico di Milano, SESAM Group (http://sesam.polimi.it) </br>

## Citing
If you use the P2H version of the Italian model or the related data, please cite the associated publication: "*Francesco Lombardi, Sylvain Quoilin, Emanuela Colombo, Modelling distributed Power-to-Heat technologies as a flexibility option for smart heat-electricity integration, ECOS 2020* "

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
