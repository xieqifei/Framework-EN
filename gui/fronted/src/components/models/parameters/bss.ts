const params  =  {
    "node_dc":{'value':null,'name':'Connected DC node','unit':''},
    "efficiency_discharge":{'value':0.9,'name':'Discharging efficiency','unit':''},
    "efficiency_charge":{'value':0.9,'name':'Charging efficiency','unit':''},
    "lifecycle":{'value':3000,'name':'Discharging efficiency','unit':''},
    "cost_investment_per_kwh":{'value':408,'name':'Cost of investing in energy capacity','unit':'EUR'},
    "cost_investment_per_kw":{'value':156,'name':'Cost of investing in power capacity','unit':'EUR'},
    "cost_o&m_per_kw_year":{'value':4,'name':'Annual maintenance and operation cost per kW','unit':'EUR'},
    "soc_initial":{'value':30,'name':'Initial SoC','unit':'%'},
    "price_recycle_per_kg":{'value':0.47,'name':'Recycling price per kg of battery','unit':'EUR'},
    "energy_density":{'value':0.1,'name':'Energy density of battery','unit':'kWh/kg'},
    "cost_battery_purchasing_per_kwh":{'value':185,'name':'Purchase price per kWh of battery','unit':'EUR'},
    "soc_min":{'value':15,'name':'Minimum SoC','unit':'%'},
    "soc_max":{'value':85,'name':'Maximum SoC','unit':'%'},
    "power_fluctuation_penalty_weight":{'value':0.00001,'name':'Penalty weight for limitation of power fluctuation','unit':''}
}

export default params