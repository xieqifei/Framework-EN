from model.base_module import ConsumerAPI
from pyomo.environ import *

class Company(ConsumerAPI):
    def __init__(self, model, name, params,**kwargs) -> None:
        super().__init__(model, name, params,**kwargs)

    def _set_params(self):
        pass

    def _add_investment_cost(self):
        pass

    def _add_annual_cashflow(self):
        pass