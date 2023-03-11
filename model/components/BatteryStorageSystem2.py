from pyomo.environ import *
from model.base_module import ComponentAPI


class BatteryStorageSystem2(ComponentAPI):
    def __init__(self, model, comp_name, params) -> None:
        super().__init__(model, comp_name, params)

    def _set_variables(self,):
        """ decision variables of component are defined.
        """
        self.m.add_component(f'power_{self.comp_name}', Var(
            self.m.time_step_count, domain=Reals))
       
        self.m.add_component(
            f'power_capacity_{self.comp_name}', Var(domain=NonNegativeReals))
        self.m.add_component(
            f'energy_capacity_{self.comp_name}', Var(domain=NonNegativeReals))


    def _set_params(self,):
        """constant parameters of component are defined.
        """
        self.m.add_component(f'efficiency_discharge_{self.comp_name}', Param(
            within=NonNegativeReals, initialize=self.params['efficiency_discharge']))
        self.m.add_component(f'efficiency_charge_{self.comp_name}', Param(
            within=NonNegativeReals, initialize=self.params['efficiency_charge']))
        self.m.add_component(f'lifecycle_{self.comp_name}', Param(
            within=NonNegativeIntegers, initialize=self.params['lifecycle']))
        self.m.add_component(f'cost_investment_per_kwh_{self.comp_name}', Param(
            mutable=True, within=NonNegativeReals, initialize=self.params['cost_investment_per_kwh']))
        self.m.add_component(f'cost_investment_per_kw_{self.comp_name}', Param(
            mutable=True, within=NonNegativeReals, initialize=self.params['cost_investment_per_kw']))
        self.m.add_component(f'cost_o&m_per_kw_year_{self.comp_name}', Param(
            within=NonNegativeReals, initialize=self.params['cost_o&m_per_kw_year']))
        self.m.add_component(f'soc_initial_{self.comp_name}', Param(
            within=NonNegativeReals, initialize=self.params['soc_initial']))
        self.m.add_component(f'cost_battery_purchasing_per_kwh_{self.comp_name}', Param(
            within=NonNegativeReals, initialize=0.45*self.m.component(f'cost_investment_per_kwh_{self.comp_name}')))
        self.m.add_component(f'price_recycle_per_kg_{self.comp_name}', Param(
            within=NonNegativeReals, initialize=self.params['price_recycle_per_kg']))
        self.m.add_component(f'energy_density_{self.comp_name}', Param(
            within=NonNegativeReals, initialize=self.params['energy_density']))
        self.m.add_component(f'soc_min_{self.comp_name}', Param(
            within=NonNegativeIntegers, initialize=self.params['soc_min']))
        self.m.add_component(f'soc_max_{self.comp_name}', Param(
            within=NonNegativeIntegers, initialize=self.params['soc_max']))

    def _set_constraints(self,):
        """ constraints of component are defined.
        """
        def _energy_remained_exp(m, t):
            return m.component(f'soc_initial_{self.comp_name}')/100*m.component(f'energy_capacity_{self.comp_name}')+sum((m.component(f'power_{self.comp_name}')[x])*m.time_intervel_hour*m.component(f'efficiency_charge_{self.comp_name}') for x in range(1, t+1))
            # return sum((m.component(f'power_in_{self.comp_name}')[x]*m.component(f'efficiency_charge_{self.comp_name}')-m.component(f'power_out_{self.comp_name}')[x]/m.component(f'efficiency_discharge_{self.comp_name}'))*m.time_intervel_hour for x in range(1, t+1))

        self.m.add_component(f'RemainingEnergyExpression{self.comp_name}', Expression(
            self.m.time_step_count, rule=_energy_remained_exp))

        self.m.add_component(f'PowerInMaxConstraints{self.comp_name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_capacity_{self.comp_name}') >= m.component(f'power_{self.comp_name}')[t]))
        self.m.add_component(f'PowerOutMaxConstraints{self.comp_name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_capacity_{self.comp_name}') >= -m.component(f'power_{self.comp_name}')[t]))

        self.m.add_component(f'SOCMaxConstraints{self.comp_name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'energy_capacity_{self.comp_name}')*m.component(f'soc_max_{self.comp_name}')/100 >= m.component(f'RemainingEnergyExpression{self.comp_name}')[t]))
        self.m.add_component(f'SOCMinConstraints{self.comp_name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'energy_capacity_{self.comp_name}') * m.component(f'soc_min_{self.comp_name}')/100 <= m.component(f'RemainingEnergyExpression{self.comp_name}')[t]))

        
        #  self.m.add_component(f'PowerInMinConstraints{self.comp_name}', Constraint(
        #     self.m.time_step_count, rule=lambda m, t: 0 <= m.component(f'power_in_{self.comp_name}')[t]))
        
        # self.m.add_component(f'PowerOutMinConstraints{self.comp_name}', Constraint(
        #     self.m.time_step_count, rule=lambda m, t: 0 <= m.component(f'power_out_{self.comp_name}')[t]))

    def _add_investment_cost(self,):
        """the fixed costs of component are added to self.m.cost_investment.
        """
        self.m.cost_investment += self.m.component(f'energy_capacity_{self.comp_name}')*self.m.component(f'cost_investment_per_kwh_{self.comp_name}')+self.m.component(
            f'power_capacity_{self.comp_name}')*self.m.component(f'cost_investment_per_kw_{self.comp_name}')

    def _add_annual_cashflow(self,):
        """ the annual cashflow of component are added to self.m.cashflow.
        """
        self.m.cashflow -= self.m.component(f'power_capacity_{self.comp_name}')*self.m.component(
            f'cost_o&m_per_kw_year_{self.comp_name}')

        # degradation cost
        # self.m.add_component(f'DegradationCostPerKWh{self.comp_name}', Expression(expr=(self.m.component(f'cost_battery_purchasing_per_kwh_{self.comp_name}')-self.m.component(
        #     f'price_recycle_per_kg_{self.comp_name}')/self.m.component(f'energy_density_{self.comp_name}'))/self.m.component(f'lifecycle_{self.comp_name}')))
        # self.m.cashflow -= self.m.scale_factor_week2year*self.m.component(f'DegradationCostPerKWh{self.comp_name}')*(self.m.component(f'efficiency_charge_{self.comp_name}')*self.m.time_intervel_hour*summation(
        #     self.m.component(f'power_in_{self.comp_name}'))+1/self.m.component(f'efficiency_discharge_{self.comp_name}')*self.m.time_intervel_hour*summation(self.m.component(f'power_out_{self.comp_name}')))

    def add2node(self, node):
        """ connect the component to a node, where the power balance is built.
        """
        # node.add_power_in(self.m.component(f'power_out_{self.comp_name}'))
        node.add_power_out(self.m.component(f'power_{self.comp_name}'))

    def get_series_variables(self):
        """return a list of the name string of series decision variables
        """
        return [f'power_{self.comp_name}']

    def get_single_variables(self):
        """return a list of the name string of single decision variables
        """
        return [f'power_capacity_{self.comp_name}', f'energy_capacity_{self.comp_name}']
