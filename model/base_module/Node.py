from pyomo.environ import *

from .base import generate_random_id


class Node:
    def __init__(self, model, name,**kwargs) -> None:
        """a node, where all power in is equal to all power out

        Args:
            model (ConcreteModel): the object of model
            name (str): a nickname of this node
        """
        for key,value in kwargs.items():
            self.__dict__[key] = value
            
        if not hasattr(self,'id'):
            self.id = generate_random_id()    
                
        self.name = name
        self.m = model
        self.powerIn = []
        self.powerOut = []
        self.m.nodes.append(self)
        

    def add_power_in(self,*powerIn):
        for power in powerIn:
            self.powerIn.append(power)

    def add_power_out(self,*powerOut):
        for power in powerOut:
            self.powerOut.append(power)

    def balance_power(self):
        def _power_balance(m,t):
            powerIn = 0
            for power in self.powerIn:
                powerIn += power[t]
            powerOut = 0
            for power in self.powerOut:
                powerOut += power[t]
            return powerIn == powerOut
        try:
            self.m.add_component(f"PowerBalanceConstraint_{self.name}&{self.id}",Constraint(self.m.time_step_count,rule =_power_balance ))
        except TypeError:
            print('TypeError occurs, it may arise when you do not call method self._set_variables() in the __init__() of component class.')
            exit()

    def remove(self):
        self.m.del_component(self.m.component(f"PowerBalanceConstraint_{self.name}&{self.id}"))