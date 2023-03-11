const params =  {
    "node_ac":{'value':null,'name':'Connected AC node','unit':''},
    "number_ports":{'value':6,'name':'Charging port number','unit':'port'},
    "cost_hardware":{'value':1000,'name':'Hardware cost per port','unit':'EUR'},
    "cost_installation":{'value':1000,'name':'Installation cost per port','unit':'EUR'},
    "cost_operation_maintanence":{'value':1000,'name':'Annual operation and maintanence cost','unit':'EUR'},
    "price_ele_sell":{'value':0.4,'name':'Electricity price','unit':'EUR'},
    
    "power_demand_filepath":{'value':"model/data/cs_power_data.json",'name':'Filepath of power demand data','unit':''}
}

export default params