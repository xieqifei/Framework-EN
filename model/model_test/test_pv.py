
import sys
import os

# add the project path to sys.path, so that model file can be found in .common/solve.py 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir =os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from pyomo.environ import ConcreteModel,value
from model.model_test import ModelTest
from model.components import *
from model.base_module import *
from model.consumers import *
from model.base_module.base import read_params 
import numpy as np
import pandas as pd

def run_model_test():
    model = ConcreteModel()
    model_params = read_params('model/params/model.json')
    modelframe = ModelFrame(model,model_params)
    node_acbus = Node(model,'ACBus')
    node_pv2inverter = Node(model,'PV2Inverter')
    node_bss2pcs = Node(model,'BSS2PCS')

    # add PV modules to acbus
    pv_params = read_params('model/params/pvmodule.json')
    pv_module =  PVModule(model,'PV modules',pv_params)
    pv_module.add2node(node_pv2inverter)

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


    # # # create inverter and add to ac bus and a dc bus node_pv2inverter
    inv_params = read_params('model/params/inverter.json')
    solar_inverter = Inverter(model,'solar inverter',inv_params)
    solar_inverter.add2node(node_acbus,node_pv2inverter)

    #create BSS and add to ac bus

    bss_params = read_params('model/params/batterystoragesystem.json')
    bss = BatteryStorageSystem(model,'BSS',bss_params)
    bss.add2node(node_bss2pcs)

    pcs_params = read_params('model/params/pcs.json')
    pcs = PowerConversionSystem(model,'PCS',pcs_params)
    pcs.add2node(node_acbus,node_bss2pcs)

    fst_param = {
        'name':f'peak_demand_rate_{grid.name}&{grid.id}',
        'range':range(100,800,70)
    }

    scd_param = {
        'name':f'price_invest_per_kw_{pv_module.name}&{pv_module.id}',
        'range':list(np.arange(1100,2000,90))
    }

    obs_vals = [
        'Obj',
        f'power_capacity_{bss.name}&{bss.id}',
        f'energy_capacity_{bss.name}&{bss.id}',
        f'power_rated_{solar_inverter.name}&{solar_inverter.id}',
        f'power_peak_{grid.name}&{grid.id}'
    ]
    modeltest = ModelTest(modelframe)
    modeltest.test_model_two_params(r'temp\test_v2\pricing_test_pv2.csv',fst_param,scd_param,*obs_vals)
    
def run_3d_bar_build():
    test = ModelTest('a')
    # test.show_3d_chart(r'temp\test_v2\pricing_test_pv2.csv','power_capacity_BSS&wUoLpgMbHN','Peak demand rate(€/a)','PV investment cost(€/kW)')
    test.save_3d_chart(r'temp\test_v2\pricing_test_pv2.csv',r'temp\test_v2\bar3d','Peak demand rate(€/kW/a)','PV investment cost(€/kW)')
run_3d_bar_build()
# run_model_test()

