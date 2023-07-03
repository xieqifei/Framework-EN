from pyomo.environ import *
from model.base_module import ComponentAPI
from model.base_module.base import *


class BatteryStorageSystem(ComponentAPI):
    def __init__(self, model, name, params,**kwargs) -> None:
        super().__init__(model, name, params,**kwargs)

    def _set_variables(self,):
        """ decision variables of component are defined.
        """
        self.m.add_component(f'power_in_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(f'power_out_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=NonNegativeReals))
        self.m.add_component(
            f'power_capacity_{self.name}&{self.id}', Var(domain=NonNegativeReals))
        self.m.add_component(
            f'energy_capacity_{self.name}&{self.id}', Var(domain=NonNegativeReals))
        self.m.add_component(f'binary_variables_one_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=Binary))
        self.m.add_component(f'binary_variables_two_{self.name}&{self.id}', Var(
            self.m.time_step_count, domain=Binary))
        self.m.add_component(f'power_in_variation_pos_{self.name}&{self.id}',Var(self.m.time_step_count,domain=NonNegativeReals))
        self.m.add_component(f'power_in_variation_neg_{self.name}&{self.id}',Var(self.m.time_step_count,domain=NonNegativeReals))
        self.m.add_component(
            f'energy_throughput_{self.name}&{self.id}', Var(domain=NonNegativeReals))
    def _set_params(self,):
        """constant parameters of component are defined.
        """
        self.m.add_component(f'efficiency_discharge_{self.name}&{self.id}', Param(
            within=NonNegativeReals,mutable=True, initialize=self.params['efficiency_discharge']))
        self.m.add_component(f'efficiency_charge_{self.name}&{self.id}', Param(
            within=NonNegativeReals,mutable=True, initialize=self.params['efficiency_charge']))
        self.m.add_component(f'cost_investment_per_kwh_{self.name}&{self.id}', Param(
            mutable=True, within=NonNegativeReals, initialize=self.params['cost_investment_per_kwh']))
        self.m.add_component(f'cost_investment_per_kw_{self.name}&{self.id}', Param(
            mutable=True, within=NonNegativeReals, initialize=self.params['cost_investment_per_kw']))
        self.m.add_component(f'cost_o&m_per_kw_year_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['cost_o&m_per_kw_year']))
        self.m.add_component(f'soc_initial_{self.name}&{self.id}', Param(
            within=NonNegativeReals,mutable=True,  initialize=self.params['soc_initial']))
        self.m.add_component(f'cost_battery_purchasing_per_kwh_{self.name}&{self.id}', Param(
            within=NonNegativeReals, mutable=True,initialize=0.45*self.m.component(f'cost_investment_per_kwh_{self.name}&{self.id}')))
        self.m.add_component(f'price_recycle_per_kg_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['price_recycle_per_kg']))
        self.m.add_component(f'energy_density_{self.name}&{self.id}', Param(
            within=NonNegativeReals, initialize=self.params['energy_density']))
        self.m.add_component(f'soc_min_{self.name}&{self.id}', Param(
            within=NonNegativeIntegers,mutable=True , initialize=self.params['soc_min']))
        self.m.add_component(f'soc_max_{self.name}&{self.id}', Param(
            within=NonNegativeIntegers,mutable=True , initialize=self.params['soc_max']))
        self.m.add_component(f'power_fluctuation_penalty_weight_{self.name}&{self.id}',Param(within=NonNegativeReals,initialize=self.params['power_fluctuation_penalty_weight']))
        self.m.add_component(f'battery_replacement_period_{self.name}&{self.id}',Param(within=NonNegativeReals,initialize=self.params['battery_replacement_period']))
        self.m.add_component(f'capacity_ratio_min_{self.name}&{self.id}',Param(within=NonNegativeReals,initialize=self.params['capacity_ratio_min']))
        #maximal life cycle
        cycle_number, ratio = read_cycle_life_from_json(self.params['cycle_life_filepath'])
        cycle_equiv_max = integrate_ratio_cycle(cycle_number,ratio,self.m.component(f'capacity_ratio_min_{self.name}&{self.id}').value)
        self.m.add_component(f'cycle_equiv_max_{self.name}&{self.id}',Param(within=NonNegativeReals,initialize=cycle_equiv_max))

    def _set_constraints(self,):
        """ constraints of component are defined.
        """
        def _energy_remained_exp(m, t):
            # if(t==1):
            #     return m.component(f'soc_initial_{self.name}&{self.id}')/100*m.component(f'energy_capacity_{self.name}&{self.id}')
            # else:
            return m.component(f'soc_initial_{self.name}&{self.id}')/100*m.component(f'energy_capacity_{self.name}&{self.id}')+sum((m.component(f'power_in_{self.name}&{self.id}')[x]*m.component(f'efficiency_charge_{self.name}&{self.id}')-m.component(f'power_out_{self.name}&{self.id}')[x]/m.component(f'efficiency_discharge_{self.name}&{self.id}'))*m.time_intervel_hour for x in range(1, t+1))
            # return sum((m.component(f'power_in_{self.name}&{self.id}')[x]*m.component(f'efficiency_charge_{self.name}&{self.id}')-m.component(f'power_out_{self.name}&{self.id}')[x]/m.component(f'efficiency_discharge_{self.name}&{self.id}'))*m.time_intervel_hour for x in range(1, t+1))

        self.m.add_component(f'RemainingEnergyExpression{self.name}&{self.id}', Expression(
            self.m.time_step_count, rule=_energy_remained_exp))

        self.m.add_component(f'PowerInMaxConstraints{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_capacity_{self.name}&{self.id}') >= m.component(f'power_in_{self.name}&{self.id}')[t]))
        self.m.add_component(f'PowerOutMaxConstraints{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_capacity_{self.name}&{self.id}') >= m.component(f'power_out_{self.name}&{self.id}')[t]))

        self.m.add_component(f'SOCMaxConstraints{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'energy_capacity_{self.name}&{self.id}')*m.component(f'soc_max_{self.name}&{self.id}')/100 >= m.component(f'RemainingEnergyExpression{self.name}&{self.id}')[t]))
        self.m.add_component(f'SOCMinConstraints{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'energy_capacity_{self.name}&{self.id}') * m.component(f'soc_min_{self.name}&{self.id}')/100 <= m.component(f'RemainingEnergyExpression{self.name}&{self.id}')[t]))

        self.m.add_component(f'ChargingDirectionConstraintsOne{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_in_{self.name}&{self.id}')[t] <= m.component(f'binary_variables_one_{self.name}&{self.id}')[t]*m.bigM))
        self.m.add_component(f'ChargingDirectionConstraintsTwo{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'power_out_{self.name}&{self.id}')[t] <= m.component(f'binary_variables_two_{self.name}&{self.id}')[t]*m.bigM))
        self.m.add_component(f'ChargingDirectinoConstraintsThree{self.name}&{self.id}', Constraint(self.m.time_step_count, rule=lambda m, t: m.component(
            f'binary_variables_one_{self.name}&{self.id}')[t]+m.component(f'binary_variables_two_{self.name}&{self.id}')[t] <= 1))

        def power_variation_exp(m,t):
            if(t==1):
                return m.component(f'power_in_variation_pos_{self.name}&{self.id}')[t]+m.component(f'power_in_variation_neg_{self.name}&{self.id}')[t]==0
            else:
                return m.component(f'power_in_variation_pos_{self.name}&{self.id}')[t]-m.component(f'power_in_variation_neg_{self.name}&{self.id}')[t] == m.component(f'power_in_{self.name}&{self.id}')[t]-m.component(f'power_in_{self.name}&{self.id}')[t-1]
        
        self.m.add_component(f'PowerInFluctuationConstraint{self.name}&{self.id}',Constraint(self.m.time_step_count,rule=power_variation_exp))
        # initail SoC == end Soc
        self.m.add_component(f'InitialAndEndSocConstraint{self.name}&{self.id}',Constraint(rule=self.m.component(f'RemainingEnergyExpression{self.name}&{self.id}')[1]==self.m.component(f'RemainingEnergyExpression{self.name}&{self.id}')[len(self.m.time_step_count)]))
        # energy throughput
        self.m.add_component(f'EnergyThroughputConstraint{self.name}&{self.id}',Constraint(rule=self.m.component(f'energy_throughput_{self.name}&{self.id}')==self.m.component(f'efficiency_charge_{self.name}&{self.id}')*self.m.time_intervel_hour*summation(self.m.component(f'power_in_{self.name}&{self.id}'))))
        self.m.add_component(f'EnergyThroughputMaxExp',Expression(expr = self.m.component(f'energy_capacity_{self.name}&{self.id}')*self.m.component(f'cycle_equiv_max_{self.name}&{self.id}')))
        self.m.add_component(f'EnergyThroughputInPeriod',Expression(expr = self.m.component(f'energy_throughput_{self.name}&{self.id}')*self.m.component(f'battery_replacement_period_{self.name}&{self.id}')*self.m.scale_factor_week2year))
        self.m.add_component(f'EnergyThroughputMaxConstraint{self.name}&{self.id}',Constraint(rule=self.m.component(f'EnergyThroughputMaxExp')>=self.m.component(f'EnergyThroughputInPeriod')))
        


    def _add_investment_cost(self,):
        """the fixed costs of component are added to self.m.cost_investment.
        """
        self.m.cost_investment += self.m.component(f'energy_capacity_{self.name}&{self.id}')*self.m.component(f'cost_investment_per_kwh_{self.name}&{self.id}')+self.m.component(
            f'power_capacity_{self.name}&{self.id}')*self.m.component(f'cost_investment_per_kw_{self.name}&{self.id}')

    def _add_annual_cashflow(self,):
        """ the annual cashflow of component are added to self.m.cashflow.
        """
        self.m.cashflow -= self.m.component(f'power_capacity_{self.name}&{self.id}')*self.m.component(
            f'cost_o&m_per_kw_year_{self.name}&{self.id}')

        # replacement cost
        self.m.add_component(f'ReplacementCostPerKWh{self.name}&{self.id}', Expression(expr=(self.m.component(f'cost_battery_purchasing_per_kwh_{self.name}&{self.id}')-self.m.component(
            f'price_recycle_per_kg_{self.name}&{self.id}')/self.m.component(f'energy_density_{self.name}&{self.id}'))))
        self.m.cashflow -= self.m.component(f'ReplacementCostPerKWh{self.name}&{self.id}')*self.m.component(f'energy_capacity_{self.name}&{self.id}')/self.m.component(f'battery_replacement_period_{self.name}&{self.id}')

        # power fluctuation penalty
        self.m.add_component(f'TotalPowerVariation{self.name}&{self.id}',Expression(expr=summation(self.m.component(f'power_in_variation_pos_{self.name}&{self.id}'))+summation(self.m.component(f'power_in_variation_neg_{self.name}&{self.id}'))))
        self.m.cashflow -= self.m.scale_factor_week2year*self.m.component(f'power_fluctuation_penalty_weight_{self.name}&{self.id}')*self.m.component(f'TotalPowerVariation{self.name}&{self.id}')

    def add2node(self, node):
        """ connect the component to a node, where the power balance is built.
        """
        node.add_power_in(self.m.component(f'power_out_{self.name}&{self.id}'))
        node.add_power_out(self.m.component(f'power_in_{self.name}&{self.id}'))

    def get_series_variables(self):
        """return a list of the name string of series decision variables
        """
        return [{'ylabel':'Power in kW','components':[self.m.component(f'power_in_{self.name}&{self.id}'),self.m.component(f'power_out_{self.name}&{self.id}')]},{'ylabel':'Energy of BSS in kWh','components':[self.m.component(f'RemainingEnergyExpression{self.name}&{self.id}')]}]

    def get_single_variables(self):
        """return a list of the name string of single decision variables
        """
        return [self.m.component(f'power_capacity_{self.name}&{self.id}'), self.m.component(f'energy_capacity_{self.name}&{self.id}')]
