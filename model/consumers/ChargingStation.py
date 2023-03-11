from model.base_module import ConsumerAPI
from pyomo.environ import *


class ChargingStation(ConsumerAPI):
    def __init__(self, model, name, params,**kwargs):
        super().__init__(model, name, params,**kwargs)
        

    def _set_params(self,):
        self.m.add_component(f'number_ports_{self.name}&{self.id}', Param(
            within=Integers,mutable=True, initialize=self.params['number_ports']))
        self.m.add_component(f'cost_hardware_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['cost_hardware']))
        self.m.add_component(f'cost_installation_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['cost_installation']))
        self.m.add_component(f'cost_operation_maintanence_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['cost_operation_maintanence']))
        self.m.add_component(f'price_ele_sell_{self.name}&{self.id}',Param(
            within=NonNegativeReals, initialize=self.params['price_ele_sell']))

    def _add_investment_cost(self):
        self.m.cost_investment += self.m.component(f'number_ports_{self.name}&{self.id}')*(self.m.component(f'cost_hardware_{self.name}&{self.id}')+self.m.component(
            f'cost_installation_{self.name}&{self.id}'))
        
    def _add_annual_cashflow(self):
        self.m.cashflow += 365/7*self.m.time_intervel_hour*sum([self.m.component(f'power_comsuption_{self.name}&{self.id}')[index] for index in self.m.component(f'power_comsuption_{self.name}&{self.id}')])*self.m.component(f'price_ele_sell_{self.name}&{self.id}')
        self.m.cashflow -= self.m.component(f'cost_operation_maintanence_{self.name}&{self.id}')
