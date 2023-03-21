from pyomo.environ import *
from model.base_module import ComponentAPI


class Grid(ComponentAPI):

    def __init__(self, model, name, params,**kwargs) -> None:
        """init
        Args:
            model (ConcreteModel): objective of optimization model
            name (str): name of this component
            params (dict): dictionary of parameters
        """
        super().__init__(model, name, params,**kwargs)

    def _set_variables(self):
        self.m.add_component(f'power_out_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(f'power_in_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(
            f'power_peak_{self.name}&{self.id}', Var(domain=NonNegativeReals))

        self.m.add_component(f'binary_variables_one_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=Binary))
        self.m.add_component(f'binary_variables_two_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=Binary))
        
        self.m.add_component(f'abs_temp_variable_in_{self.name}&{self.id}',Var(self.m.time_step_count,domain = NonNegativeReals))
        self.m.add_component(f'abs_temp_variable_out_{self.name}&{self.id}',Var(self.m.time_step_count,domain = NonNegativeReals))

        
    def _set_params(self,):
        self.m.add_component(f'power_max_allowed_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['power_grid_max']))
        self.m.add_component(f'cost_connection_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['cost_grid_connection']))
        self.m.add_component(f'peak_demand_rate_{self.name}&{self.id}', Param(mutable=True,
                                                                           within=NonNegativeReals, initialize=self.params['peak_demand_rate']))
        # self.m.add_component(f'ele_price_sell_{self.name}&{self.id}', Param(mutable=True,
        #                                                                within=NonNegativeReals, initialize=self.params['ele_price_sell']))
        self.m.add_component(f'ele_price_{self.name}&{self.id}', Param(mutable=True,
                                                                      within=NonNegativeReals, initialize=self.params['ele_price']))
        self.m.add_component(f'maximal_allowed_power_change_{self.name}&{self.id}',Param(mutable=True, initialize=1,within=NonNegativeReals))

    def _set_constraints(self,):
        self.m.add_component(f'PowerOutMaxConstraint{self.name}&{self.id}', Constraint(
            self.m.time_step_count, rule=lambda m, t: m.component(f'power_out_{self.name}&{self.id}')[t] <= m.component(f'power_peak_{self.name}&{self.id}')))
        # self.m.add_component(f'PowerInMaxConstraint{self.name}&{self.id}', Constraint(
        #     self.m.time_step_count, rule=lambda m, t: m.component(f'power_in_{self.name}&{self.id}')[t] <= m.component(f'power_peak_{self.name}&{self.id}')))
        self.m.add_component(f'PowerMaxConstraint{self.name}&{self.id}', Constraint(expr=self.m.component(
            f'power_peak_{self.name}&{self.id}') <= self.m.component(f'power_max_allowed_{self.name}&{self.id}')))

        self.m.add_component(f'ChargingDirectionConstraintsOne{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_in_{self.name}&{self.id}')[t] <= m.component(f'binary_variables_one_{self.name}&{self.id}')[t]*m.bigM))
        self.m.add_component(f'ChargingDirectionConstraintsTwo{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_out_{self.name}&{self.id}')[t] <= m.component(f'binary_variables_two_{self.name}&{self.id}')[t]*m.bigM))
        self.m.add_component(f'ChargingDirectinoConstraintsThree{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'binary_variables_one_{self.name}&{self.id}')[t]+m.component(f'binary_variables_two_{self.name}&{self.id}')[t] <= 1))

    def _add_investment_cost(self):
        # grid connection charge
        self.m.cost_investment += self.m.component(
            f'cost_connection_{self.name}&{self.id}')

    def _add_annual_cashflow(self):
        # annual cash inflow, energy sell to grid, feed in tarif is 0.9 times electricity price
        self.m.cashflow += self.m.scale_factor_week2year * 0.9 * self.m.component(f'ele_price_{self.name}&{self.id}') *\
            summation(self.m.component(f'power_in_{self.name}&{self.id}')) * \
            self.m.time_intervel_hour
        # annual cash outflow, purchase energy from grid
        self.m.cashflow -= self.m.scale_factor_week2year * \
            self.m.time_intervel_hour * self.m.component(f'ele_price_{self.name}&{self.id}') *\
            summation(self.m.component(
                f'power_out_{self.name}&{self.id}'))
        # peak demand charge
        self.m.cashflow -= self.m.component(
            f'power_peak_{self.name}&{self.id}')*self.m.component(f'peak_demand_rate_{self.name}&{self.id}')

    def add2node(self, node):
        node.add_power_in(self.m.component(f'power_out_{self.name}&{self.id}'))
        node.add_power_out(self.m.component(f'power_in_{self.name}&{self.id}'))

    def get_series_variables(self):
        """return a list of the name string of series decision variables
        """
        return [{'ylabel':'Power in kW',"components":[self.m.component(f'power_in_{self.name}&{self.id}'), self.m.component(f'power_out_{self.name}&{self.id}')]}]

    def get_single_variables(self):
        """return a list of the name string of single decision variables
        """
        return [self.m.component(f'power_peak_{self.name}&{self.id}')]