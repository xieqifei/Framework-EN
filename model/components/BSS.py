from pyomo.environ import *
from model.base_module import ComponentAPI


class BSS(ComponentAPI):
    def __init__(self, model, name, params) -> None:
        super().__init__(model, name, params)

    def _set_variables(self,):
        """ decision variables of component are defined.
        """

        self.m.add_component(f'power_in_{self.name}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(f'power_out_{self.name}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(
            f'power_capacity_{self.name}', Var(domain=NonNegativeReals))
        self.m.add_component(
            f'energy_capacity_{self.name}', Var(domain=NonNegativeReals))
        self.m.add_component(f'binary_variables_one_{self.name}', Var(
            self.m.time_step_count, domain=Binary))
        self.m.add_component(f'binary_variables_two_{self.name}', Var(
            self.m.time_step_count, domain=Binary))

        self.m.add_component(f'energy_remaining_{self.name}', Var(
            self.m.time_step_count, domain=NonNegativeReals))

    def _set_params(self,):
        """constant parameters of component are defined.
        """
        self.m.add_component(f'efficiency_discharge_{self.name}', Param(
            within=NonNegativeReals, initialize=self.params['efficiency_discharge']))
        self.m.add_component(f'efficiency_charge_{self.name}', Param(
            within=NonNegativeReals, initialize=self.params['efficiency_charge']))
        self.m.add_component(f'lifecycle_{self.name}', Param(
            within=NonNegativeIntegers, initialize=self.params['lifecycle']))
        self.m.add_component(f'cost_investment_per_kwh_{self.name}', Param(
            mutable=True, within=NonNegativeReals, initialize=self.params['cost_investment_per_kwh']))
        self.m.add_component(f'cost_investment_per_kw_{self.name}', Param(
            mutable=True, within=NonNegativeReals, initialize=self.params['cost_investment_per_kw']))
        self.m.add_component(f'cost_o&m_per_kw_year_{self.name}', Param(
            within=NonNegativeReals, initialize=self.params['cost_o&m_per_kw_year']))
        self.m.add_component(f'soc_initial_{self.name}', Param(
            within=NonNegativeReals, initialize=self.params['soc_initial']))
        self.m.add_component(f'dod_max_{self.name}', Param(
            within=NonNegativeReals, initialize=self.params['dod_max']))
        self.m.add_component(f'cost_battery_purchasing_per_kwh_{self.name}', Param(
            within=NonNegativeReals, initialize=0.45*self.m.component(f'cost_investment_per_kwh_{self.name}')))
        self.m.add_component(f'price_recycle_per_kg_{self.name}', Param(
            within=NonNegativeReals, initialize=self.params['price_recycle_per_kg']))
        self.m.add_component(f'energy_density_{self.name}', Param(
            within=NonNegativeReals, initialize=self.params['energy_density']))

        # self.m.add_component(f'soc_min_{self.name}', Param(
        #     within=NonNegativeIntegers, initialize=self.params['soc_min']))
        # self.m.add_component(f'soc_max_{self.name}', Param(
        #     within=NonNegativeIntegers, initialize=self.params['soc_max']))

    def _set_constraints(self,):
        """ constraints of component are defined.
        """
        self.m.add_component(f'EnergyZeroStep{self.name}', Expression(expr=self.m.component(
            f'soc_initial_{self.name}')/100*self.m.component(f'energy_capacity_{self.name}')))

        def _energy_remaining_rule(m, t):
            if (t == 1):
                return m.component(f'energy_remaining_{self.name}')[t] == m.component(f'EnergyZeroStep{self.name}')+(m.component(f'power_in_{self.name}')[t]*m.component(f'efficiency_charge_{self.name}')-m.component(f'power_out_{self.name}')[t]/m.component(f'efficiency_discharge_{self.name}'))*m.time_intervel_hour
            else:
                return m.component(f'energy_remaining_{self.name}')[t] == m.component(f'energy_remaining_{self.name}')[t-1]+(m.component(f'power_in_{self.name}')[t]*m.component(f'efficiency_charge_{self.name}')-m.component(f'power_out_{self.name}')[t]/m.component(f'efficiency_discharge_{self.name}'))*m.time_intervel_hour
        self.m.add_component(f'RemainingEnergyConstraint{self.name}', Constraint(
            self.m.time_step_count, rule=_energy_remaining_rule))
        # def _energy_remained_exp(m, t):
        #     return m.component(f'soc_initial_{self.name}')/100*m.component(f'energy_capacity_{self.name}')+sum((m.component(f'power_in_{self.name}')[x]*m.component(f'efficiency_charge_{self.name}')-m.component(f'power_out_{self.name}')[x]/m.component(f'efficiency_discharge_{self.name}'))*m.time_intervel_hour for x in range(1, t+1))
        #     # return sum((m.component(f'power_in_{self.name}')[x]*m.component(f'efficiency_charge_{self.name}')-m.component(f'power_out_{self.name}')[x]/m.component(f'efficiency_discharge_{self.name}'))*m.time_intervel_hour for x in range(1, t+1))

        # self.m.add_component(f'energy_remaining_{self.name}', Expression(
        #     self.m.time_step_count, rule=_energy_remained_exp))

        self.m.add_component(f'PowerInMaxConstraints{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_capacity_{self.name}') >= m.component(f'power_in_{self.name}')[t]))
        self.m.add_component(f'PowerOutMaxConstraints{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_capacity_{self.name}') >= m.component(f'power_out_{self.name}')[t]))
        # self.m.add_component(f'SOCMaxConstraints{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
        #     f'energy_capacity_{self.name}')*m.component(f'soc_max_{self.name}')/100 >= m.component(f'energy_remaining_{self.name}')[t]))
        # self.m.add_component(f'SOCMinConstraints{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
        #     f'energy_capacity_{self.name}') * m.component(f'soc_min_{self.name}')/100 <= m.component(f'energy_remaining_{self.name}')[t]))

        self.m.add_component(f'ChargingDirectionConstraintsOne{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_in_{self.name}')[t] <= m.component(f'binary_variables_one_{self.name}')[t]*m.bigM))
        self.m.add_component(f'ChargingDirectionConstraintsTwo{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_out_{self.name}')[t] <= m.component(f'binary_variables_two_{self.name}')[t]*m.bigM))
        self.m.add_component(f'ChargingDirectinoConstraintsThree{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'binary_variables_one_{self.name}')[t]+m.component(f'binary_variables_two_{self.name}')[t] == 1))

        self.m.add_component(f'EnergyCapacityConstraints{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'energy_capacity_{self.name}') >= m.component(f'RemainingEnergyExpression{self.name}')[t]))
        self.m.add_component(f'DepthOfDischargeConstraints{self.name}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'energy_capacity_{self.name}')*(1-m.component(f'dod_max_{self.name}')/100) <= m.component(f'RemainingEnergyExpression{self.name}')[t]))


        self.m.add_component(f'PowerInMinConstraints{self.name}', Constraint(
            self.m.time_step_count, rule=lambda m, t: 0 <= m.component(f'power_in_{self.name}')[t]))
        self.m.add_component(f'PowerOutMinConstraints{self.name}', Constraint(
            self.m.time_step_count, rule=lambda m, t: 0 <= m.component(f'power_out_{self.name}')[t]))

    def _add_investment_cost(self,):
        """the fixed costs of component are added to self.m.cost_investment.
        """
        self.m.cost_investment += self.m.component(f'energy_capacity_{self.name}')*self.m.component(f'cost_investment_per_kwh_{self.name}')+self.m.component(
            f'power_capacity_{self.name}')*self.m.component(f'cost_investment_per_kw_{self.name}')

        # degradation cost
        self.m.add_component(f'DegradationCostPerKWh{self.name}', Expression(expr=(self.m.component(f'cost_battery_purchasing_per_kwh_{self.name}')-self.m.component(
            f'price_recycle_per_kg_{self.name}')/self.m.component(f'energy_density_{self.name}'))/self.m.component(f'lifecycle_{self.name}')))
        self.m.cost_investment += self.m.component(f'DegradationCostPerKWh{self.name}')*(self.m.component(f'efficiency_charge_{self.name}')*self.m.time_intervel_hour*summation(
            self.m.component(f'power_in_{self.name}'))+1/self.m.component(f'efficiency_discharge_{self.name}')*self.m.time_intervel_hour*summation(self.m.component(f'power_out_{self.name}')))

    def _add_annual_cashflow(self,):
        """ the annual cashflow of component are added to self.m.cashflow.
        """
        self.m.cashflow -= self.m.component(f'power_capacity_{self.name}')*self.m.component(
            f'cost_o&m_per_kw_year_{self.name}')

    def add2node(self, node):
        """ connect the component to a node, where the power balance is built.
        """
        node.add_power_in(self.m.component(f'power_out_{self.name}'))
        node.add_power_out(self.m.component(f'power_in_{self.name}'))

    def get_series_variables(self):
        """return a list of the name string of series decision variables
        """
        return [f'power_in_{self.name}', f'power_out_{self.name}']

    def get_single_variables(self):
        """return a list of the name string of single decision variables
        """
        return [f'power_capacity_{self.name}', f'energy_capacity_{self.name}']
