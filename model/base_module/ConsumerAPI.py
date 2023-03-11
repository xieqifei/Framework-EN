from pyomo.environ import *
import abc

from .base import convert_keys_str2int, generate_random_id, read_params

class ConsumerAPI(abc.ABC):

    def __init__(self,model,name,params,**kwargs) -> None:
        for key,value in kwargs.items():
            self.__dict__[key] = value
            
        if not hasattr(self,'id'):
            self.id = generate_random_id()
        self.m = model
        self.name = name
        self.params  = params
        self.power_comsuption = convert_keys_str2int(read_params(params['power_demand_filepath']))
        self.m.add_component(f'power_comsuption_{self.name}&{self.id}',Param(
            self.m.time_step_count, within=NonNegativeReals, initialize=self.power_comsuption))
        self._set_params()
        self._add_investment_cost()
        self._add_annual_cashflow()

    def add2node(self,node):
        node.add_power_out(self.m.component(f'power_comsuption_{self.name}&{self.id}'))

    @abc.abstractmethod
    def _set_params(self):
        """must be overload in child class, and be implemented in __init__() firstly.
        In this method, the parameters of comsumer will be defined.
        """        
        pass

    @abc.abstractmethod
    def _add_investment_cost(self):
        """must be overload in child class, and be implemented in __init__() secondly.
        In this method, the investment cost of comsumer will be added to self.m.cost_investment.
        """  
        pass

    @abc.abstractmethod
    def _add_annual_cashflow(self):
        """must be overload in child class, and be implemented in __init__() thirdly.
        In this method, the annaul cashflow of comsumer will be added to self.m.cashflow.
        """  
        pass
    
    def get_series_variables(self):
        return [{'ylabel':'power in kW','components':[self.m.component(f'power_comsuption_{self.name}&{self.id}')]}]
    
    def get_single_variables(self):
        """return a list of the name string of single decision variables
        """
        return []