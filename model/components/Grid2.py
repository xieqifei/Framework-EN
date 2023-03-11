from pyomo.environ import *
from model.base_module import ComponentAPI


class Grid2(ComponentAPI):

    def __init__(self, model, comp_name, params, ele_price) -> None:
        """init

        Args:
            model (ConcreteModel): objective of optimization model
            comp_name (str): name of this component
            params_filepath (str): filepath of constant parameters, point to a .json file
            ele_price (dict): electricity price, usually day ahead price, keys from 1 to number of data, values are prices of each time step.
        """
        super().__init__(model, comp_name, params)

    def _set_variables(self):
        self.m.add_component(f'power_out_{self.comp_name}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(f'power_in_{self.comp_name}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(f'power_max_real_{self.comp_name}',Var(domain = NonNegativeReals))

    def _set_params(self,):
        self.m.add_component(f'power_max_allowed_{self.comp_name}', Param(
            within=NonNegativeReals, initialize=self.params['power_grid_max']))
        self.m.add_component(f'cost_connection_{self.comp_name}',Param(
            within=NonNegativeReals, initialize=self.params['cost_grid_connection'] ))
        self.m.add_component(f'peak_demand_rate_{self.comp_name}',Param(
            within=NonNegativeReals, initialize=self.params['peak_demand_rate']))
        self.m.add_component(f'price_day_ahead_{self.comp_name}',Param(
            self.m.time_step_count, within=NonNegativeReals, initialize=self.ele_price))
        self.m.add_component(f'ele_price_100x',Expression(self.m.time_step_count,rule = lambda m,t:100*m.component(f'price_day_ahead_{self.comp_name}')[t]))


    def _set_constraints(self,):
        self.m.add_component(f'PowerOutMaxConstraint{self.comp_name}',Constraint(
            self.m.time_step_count, rule=lambda m, t: m.component(f'power_out_{self.comp_name}')[t] <= m.component(f'power_max_real_{self.comp_name}'))) 
        self.m.add_component(f'PowerInMaxConstraint{self.comp_name}',Constraint(
            self.m.time_step_count, rule=lambda m, t: m.component(f'power_in_{self.comp_name}')[t] <= m.component(f'power_max_real_{self.comp_name}'))) 
        self.m.add_component(f'PowerMaxConstraint{self.comp_name}',Constraint(expr=self.m.component(f'power_max_real_{self.comp_name}')<=self.m.component(f'power_max_allowed_{self.comp_name}')))
    def _add_investment_cost(self):
        # grid connection charge
        self.m.cost_investment += self.m.component(f'cost_connection_{self.comp_name}')
        #peak demand charge
        self.m.cost_investment += self.m.component(
            f'power_max_real_{self.comp_name}')*self.m.component(f'peak_demand_rate_{self.comp_name}')

    def _add_annual_cashflow(self):
        # annual cash inflow, energy sell to grid
        self.m.cashflow += 0.9*365/7 * \
            summation(self.m.component(f'price_day_ahead_{self.comp_name}'), self.m.component(f'power_in_{self.comp_name}')) * \
            self.m.time_intervel_hour
        # annual cash outflow, purchase energy from grid
        self.m.cashflow -= 365/7 * \
            self.m.time_intervel_hour * \
            summation(self.m.component(f'price_day_ahead_{self.comp_name}'), self.m.component(
                f'power_out_{self.comp_name}'))

    def add2node(self, node):
        node.add_power_in(self.m.component(f'power_out_{self.comp_name}'))
        node.add_power_out(self.m.component(f'power_in_{self.comp_name}'))

    def get_variables(self):
        """return a list with name of variables

        Returns:
            list[str]: a string list, where name of the decision varibales will be returned as string
        """        
        vars = [f'power_out_{self.comp_name}', f'power_in_{self.comp_name}']
        return vars
