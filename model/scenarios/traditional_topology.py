from pyomo.environ import *
from model.components import *
from model.base_module import *
from model.base_module.base import read_params
from model.consumers import *
import os
    

def run_traditional_topology():
    model_path = os.path.dirname(os.path.dirname(__file__))
    model_params_path = os.path.join(model_path,'params')
    model_data_path = os.path.join(os.path.dirname(model_path),'sources/model_data')

    model = ConcreteModel()
    model_params = read_params(os.path.join(model_params_path,'model.json'))
    modelframe = ModelFrame(model,model_params)
    node_acbus = Node(model,'ACBus')

    # create the grid 
    grid_params = read_params(os.path.join(model_params_path,'grid.json'))
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
   


    modelframe.solve('gurobi')
    print('NPV:',value(model.Obj))
    print("grid max power flow:",value(model.component(f'power_peak_{grid.comp_name}')))

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
    power_grid = integrate_power(f'power_out_{grid.comp_name}',f'power_in_{grid.comp_name}','grid')

    modelframe.save_line_chart(r"sources\result_figures\final_figure\result_simple.png",power_grid,convert_power(f'power_comsuption_{charge_station.coms_name}'),convert_power(f'power_comsuption_{company.coms_name}'))
    
