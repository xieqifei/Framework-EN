from model.base_module import ComponentAPI
from model.base_module.base import convert_keys_str2int, read_params
from pyomo.environ import *


class PVModule(ComponentAPI):
    def __init__(self, model, name, params,**kwargs) -> None:
           super().__init__(model,name,params,**kwargs)

    def _set_variables(self,):
        self.m.add_component(f'power_out_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(f'module_number_{self.name}&{self.id}', Var(
            domain=NonNegativeIntegers))

    def _set_params(self,):
        self.m.add_component(f'module_area_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['module_area']))
        self.m.add_component(f'irradiance_stc_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['irradiance_stc']))
        self.m.add_component(f'irradiance_real_{self.name}&{self.id}', Param(
            self.m.time_step_count, within=NonNegativeReals, initialize=convert_keys_str2int(read_params(self.params['global_irradiance_filepath']))))
        self.m.add_component(f'efficiency_module_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['efficiency_module']))
        self.m.add_component(f'power_stc_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['power_stc']))
        self.m.add_component(f'temperature_coefficient_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['temperature_coefficient']))
        self.m.add_component(f'temperature_cell_stc_{self.name}&{self.id}', Param(
            within=Reals, initialize=self.params['temperature_cell_stc']))
        self.m.add_component(f'temperature_ambient_{self.name}&{self.id}', Param(
            self.m.time_step_count, within=Reals, initialize=convert_keys_str2int(read_params(self.params['ambient_temperature_filepath']))))
        self.m.add_component(f'temperature_noc_{self.name}&{self.id}', Param(
            within=Reals, initialize=self.params['temperature_noc']))
        self.m.add_component(f'area_max_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['area_max']))
        self.m.add_component(f'price_invest_per_kw_{self.name}&{self.id}', Param(mutable = True,
            within=NonNegativeReals, initialize=self.params['price_invest_per_kw']))

    def _set_constraints(self,):
        def _cell_tempe_expr(m, t):
            return m.component(f'temperature_ambient_{self.name}&{self.id}')[t]+(m.component(f'temperature_noc_{self.name}&{self.id}')-20)*m.component(f'irradiance_real_{self.name}&{self.id}')[t]/0.8
        self.m.add_component(f'temperature_cell_{self.name}&{self.id}', Expression(
            self.m.time_step_count, rule=_cell_tempe_expr))
        self.m.add_component(f'PowerMaxGenerationConstraints{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(f'power_out_{self.name}&{self.id}')[t] <= m.component(f'module_number_{self.name}&{self.id}')*m.component(f'module_area_{self.name}&{self.id}')*m.component(f'irradiance_real_{self.name}&{self.id}')[
                             t]/m.component(f'irradiance_stc_{self.name}&{self.id}')*m.component(f'efficiency_module_{self.name}&{self.id}')*m.component(f'power_stc_{self.name}&{self.id}')*(1-m.component(f'temperature_coefficient_{self.name}&{self.id}')*(m.component(f'temperature_cell_{self.name}&{self.id}')[t]-m.component(f'temperature_cell_stc_{self.name}&{self.id}')))))
        self.m.add_component(f'AreaMaxConstraint{self.name}&{self.id}', Constraint(
            expr=self.m.component(f'module_number_{self.name}&{self.id}') <= self.m.component(f'area_max_{self.name}&{self.id}')/self.m.component(f'module_area_{self.name}&{self.id}')))

    def _add_investment_cost(self,):
        # self.m.add_component(f'investment_cost_{self.name}&{self.id}', Expression(expr=self.m.component(f'price_invest_per_kw_{self.name}&{self.id}')*self.m.component(
        #     f'module_number_{self.name}&{self.id}')*self.m.component(f'power_stc_{self.name}&{self.id}')))
        # self.m.cost_investment += self.m.component(f'investment_cost_{self.name}&{self.id}')
        self.m.cost_investment += self.m.component(f'price_invest_per_kw_{self.name}&{self.id}')*self.m.component(
            f'module_number_{self.name}&{self.id}')*self.m.component(f'power_stc_{self.name}&{self.id}')
       

    def _add_annual_cashflow(self,):
        self.m.cashflow -= 0.02*self.m.component(f'price_invest_per_kw_{self.name}&{self.id}')*self.m.component(
            f'module_number_{self.name}&{self.id}')*self.m.component(f'power_stc_{self.name}&{self.id}')
        # super()._add_annual_cashflow(-0.02*self.m.component(f'price_invest_per_kw_{self.name}&{self.id}')*self.m.component(
        #     f'module_number_{self.name}&{self.id}')*self.m.component(f'power_stc_{self.name}&{self.id}'))

    def add2node(self,node):
        node.add_power_in(self.m.component(f'power_out_{self.name}&{self.id}'))

    def get_series_variables(self):
        """return a list of the name string of series decision variables
        """
        return [{'ylabel':'Power in kW','components':[self.m.component(f'power_out_{self.name}&{self.id}')]}]

    def get_single_variables(self):
        """return a list of the name string of single decision variables
        """
        return [self.m.component(f'module_number_{self.name}&{self.id}')]
