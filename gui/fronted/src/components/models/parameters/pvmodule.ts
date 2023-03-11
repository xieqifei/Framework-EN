const params =  {
    "node_dc":{'value':null,'name':'Connected node','unit':''},
    "module_area":{'value':1,'name':'Surface area of module','unit':'m^2'},
    "irradiance_stc":{'value':1,'name':'Irradiance under standard test condition','unit':'kW/m^2'},
    "efficiency_module":{'value':0.19,'name':'Power conversion efficiency','unit':''},
    "power_stc":{'value':0.24,'name':'Nominal power under standard test condition','unit':'kW'},
    "temperature_coefficient":{'value':0.003,'name':'Temperature coefficient of power of PV module','unit':''},
    "temperature_cell_stc":{'value':25,'name':'Cell temperatureunder standard test condition','unit':'℃'},
    "temperature_noc":{'value':44,'name':'Nominal operation cell temperature','unit':'℃'},
    "area_max":{'value':200,'name':'Maximum available installation area','unit':'m^2'},
    "price_invest_per_kw":{'value':2000,'name':'Investment cost of PV module per kW','unit':'EUR'},
    "ambient_temperature_filepath":{'value':"model/data/ambient_temp.json",'name':'Path of ambient temperature data','unit':''},
    "global_irradiance_filepath":{'value':"model/data/irradiance.json",'name':'Path of global irradiance data','unit':''}
}

export default params