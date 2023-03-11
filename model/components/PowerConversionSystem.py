from pyomo.environ import *
from model.base_module import ComponentAPI


class PowerConversionSystem(ComponentAPI):

    def __init__(self, model, name, params,**kwargs) -> None:
       super().__init__(model,name,params,**kwargs)       

    def _set_variables(self):
        self.m.add_component(f'power_out_dc_{self.name}&{self.id}',Var(self.m.time_step_count,domain = NonNegativeReals))
        self.m.add_component(f'power_in_dc_{self.name}&{self.id}',Var(self.m.time_step_count,domain = NonNegativeReals))
        self.m.add_component(f'power_out_ac_{self.name}&{self.id}',Var(self.m.time_step_count,domain = NonNegativeReals))
        self.m.add_component(f'power_in_ac_{self.name}&{self.id}',Var(self.m.time_step_count,domain = NonNegativeReals))
        self.m.add_component(f'power_rated_{self.name}&{self.id}',Var(domain = NonNegativeReals))


    def _set_params(self,):
        self.m.add_component(f'pirce_per_kw_{self.name}&{self.id}',Param(within=NonNegativeReals,initialize=self.params['pirce_per_kw']))
        self.m.add_component(f'efficiency_{self.name}&{self.id}',Param(within=NonNegativeReals,initialize = self.params['efficiency']))

    def _set_constraints(self,):
        self.m.add_component(f'EfficiencyConstraintsOne{self.name}&{self.id}',Constraint(self.m.time_step_count,rule = lambda m,t:m.component(f'power_out_dc_{self.name}&{self.id}')[t]==m.component(f'efficiency_{self.name}&{self.id}')*m.component(f'power_in_ac_{self.name}&{self.id}')[t]))
        self.m.add_component(f'EfficiencyConstraintsTwo{self.name}&{self.id}',Constraint(self.m.time_step_count,rule = lambda m,t:m.component(f'power_out_ac_{self.name}&{self.id}')[t]==m.component(f'efficiency_{self.name}&{self.id}')*m.component(f'power_in_dc_{self.name}&{self.id}')[t]))
        self.m.add_component(f'RatedPowerConstraintsOne{self.name}&{self.id}',Constraint(self.m.time_step_count,rule = lambda m,t:m.component(f'power_in_dc_{self.name}&{self.id}')[t]<=m.component(f'power_rated_{self.name}&{self.id}')))
        self.m.add_component(f'RatedPowerConstraintsTwo{self.name}&{self.id}',Constraint(self.m.time_step_count,rule = lambda m,t:m.component(f'power_in_ac_{self.name}&{self.id}')[t]<=m.component(f'power_rated_{self.name}&{self.id}')))
    
    def _add_investment_cost(self):
        self.m.cost_investment += self.m.component(f'power_rated_{self.name}&{self.id}')*self.m.component(f'pirce_per_kw_{self.name}&{self.id}')
    
    def _add_annual_cashflow(self):
        pass

    def add2node(self, node_ac,node_dc):
       node_ac.add_power_in(self.m.component(f'power_out_ac_{self.name}&{self.id}'))
       node_ac.add_power_out(self.m.component(f'power_in_ac_{self.name}&{self.id}'))
       node_dc.add_power_in(self.m.component(f'power_out_dc_{self.name}&{self.id}'))
       node_dc.add_power_out(self.m.component(f'power_in_dc_{self.name}&{self.id}'))

    def get_series_variables(self):
        """return a list of the name string of series decision variables
        """
        return [{'ylabel':'Power in kW','components':[self.m.component(f'power_out_dc_{self.name}&{self.id}'), self.m.component(f'power_in_dc_{self.name}&{self.id}'),self.m.component(f'power_out_ac_{self.name}&{self.id}'),self.m.component(f'power_in_ac_{self.name}&{self.id}')]}]

    def get_single_variables(self):
        """return a list of the name string of single decision variables
        """
        return [self.m.component(f'power_rated_{self.name}&{self.id}')]