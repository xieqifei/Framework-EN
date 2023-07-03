
import sys
import os

# add the project path to sys.path, so that model file can be found in .common/solve.py 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir =os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from pyomo.environ import *
from model.components import *
from model.base_module import *
from model.consumers import *
from model.base_module.base import read_params

    

def run_with_bss_topology():
    model = ConcreteModel()
    model_params = read_params('model/params/model.json')
    modelframe = ModelFrame(model,model_params)
    node_acbus = Node(model,'ACBus')
    node_bss2pcs = Node(model,'BSS2PCS')

    # create the grid 
    grid_params = read_params('model/params/grid.json')
    grid = Grid(model,'the grid',grid_params)
    grid.add2node(node_acbus)

    # add charging station to acbus
    cs_params = read_params('model/params/chargingstation.json')
    charge_station = ChargingStation(model,'charging station',cs_params)
    charge_station.add2node(node_acbus)

    #add company demand to acbus
    com_params =  read_params('model/params/company.json')
    company = Company(model,'company',com_params)
    company.add2node(node_acbus)

  

    #create BSS and add to ac bus

    bss_params = read_params('model/params/batterystoragesystem.json')
    bss = BatteryStorageSystem(model,'BSS',bss_params)
    bss.add2node(node_bss2pcs)

    pcs_params = read_params('model/params/pcs.json')
    pcs = PowerConversionSystem(model,'PCS',pcs_params)
    pcs.add2node(node_acbus,node_bss2pcs)


    modelframe.solve('gurobi')

    print('NPV:',value(model.Obj))
    print("bss power cap:",value(model.component(f'power_capacity_{bss.name}&{bss.id}')))
    print("bss energy cap:",value(model.component(f'energy_capacity_{bss.name}&{bss.id}')))
    print("grid max power flow:",value(model.component(f'power_peak_{grid.name}&{grid.id}')))
    print("total power variation",value(model.component(f'TotalPowerVariation{bss.name}&{bss.id}')))

    def convert_power(power_str):
        power_neg_val = [value(model.component(power_str)[i]) for i in model.component(power_str)]
        power_neg = {}
        for i,v in enumerate(power_neg_val):
            power_neg[i+1]=-power_neg_val[i]
        model.add_component(f'{power_str}_neg',Param(model.time_step_count,initialize = power_neg))
        return f'{power_str}_neg'
        
    
    
    def integrate_power(power_pos_str,power_neg_str,suffix):
        """integrate out and in power as a positive and negative power

        Returns:
            _type_: _description_
        """   
        power_pos_val = [value(model.component(power_pos_str)[i]) for i in model.component(power_pos_str)]
        power_neg_val = [value(model.component(power_neg_str)[i]) for i in model.component(power_neg_str)]
        power_intergrated = {}
        for i,v in enumerate(power_neg_val):
            power_intergrated[i+1]=power_pos_val[i]-power_neg_val[i]
        model.add_component(f'power_{suffix}',Param(model.time_step_count,initialize=power_intergrated))
        return f'power_{suffix}'
    # integrate grid
    power_grid = integrate_power(f'power_out_{grid.name}&{grid.id}',f'power_in_{grid.name}&{grid.id}','grid')
    power_bss = integrate_power(f'power_out_{bss.name}&{bss.id}',f'power_in_{bss.name}&{bss.id}','BSS')

    modelframe.save_line_chart(r'temp\result_with_bss.png',power_grid,power_bss,convert_power(f'power_comsuption_{charge_station.name}&{charge_station.id}'),convert_power(f'power_comsuption_{company.name}&{company.id}'))
    modelframe.save_line_chart( r'temp\result_with_bss_energy.png',f'RemainingEnergyExpression{bss.name}&{bss.id}',ylabel='remaining energy in BSS (kWh)')



run_with_bss_topology()