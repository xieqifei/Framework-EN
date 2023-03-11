
import abc

from .base import generate_random_id


class ComponentAPI(abc.ABC):
    """interface of Components, all the components need to implement this API, 
    so that all components have same methods.
    """
    def __init__(self,model,name,params,**kwargs) -> None:
        """the attribute of parent class will be added hier, the overloaded methodes in parent class like, _set_variables()
        ,_set_params(),_set_constrints(),etc. will be executed automaticlly.

        Args:
            model (ConcreteModel): model object
            name (str): name of component
            params (dict): parameters of component
        """        
        for key,value in kwargs.items():
            self.__dict__[key] = value
        if not hasattr(self,'id'):
            self.id = generate_random_id()
        self.m = model
        self.name = name
        self.params = params
        self.fix_cost = 0
        self.yearly_cashflow = 0
        self._set_variables()
        self._set_params()
        self._set_constraints()
        self._add_investment_cost()
        self._add_annual_cashflow() 



    @abc.abstractmethod
    def _set_variables(self,):
        """must be overloaded in child class, and call in __init__ firstly.
        In this method,  decision variables of component are defined.
        """        
        pass

    @abc.abstractmethod
    def _set_params(self,):
        """must be overloaded in child class, and call in __init__ secondly
        In this method, constant parameters of component are defined.
        """ 
        pass

    @abc.abstractmethod
    def _set_constraints(self,):
        """must be overloaded in child class, and call in __init__ thirdly
        In this method,  constraints of component are defined.
        """ 
        pass

    @abc.abstractmethod
    def _add_investment_cost(self):
        """must be overloaded in child class, and call in __init__ fourthly
        In this method, the fixed costs of component are added to self.m.cost_investment.
        """ 
        pass

    @abc.abstractmethod
    def _add_annual_cashflow(self):
        """must be overloaded in child class, and call in __init__ fifthly
        In this method, the annual cashflow of component are added to self.m.cashflow.
        """ 
        pass

    @abc.abstractmethod
    def add2node(self,):
        """must be overloaded in child class, and when call it to connect the component to a node, where the power balance is built.
        """        
        pass

 
    def get_investment_cost(self):
        return self.fix_cost

    def get_yearly_cashflow(self):
        return self.yearly_cashflow

    @abc.abstractmethod
    def get_series_variables(self):
        """return a list of the name string of series decision variables
        """
        pass

    @abc.abstractmethod
    def get_single_variables(self):
        """return a list of the name string of single decision variables
        """
        pass
