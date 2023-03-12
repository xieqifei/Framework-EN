from pyomo.environ import *
from datetime import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.dates import HourLocator
from .Node import Node
import json
class ModelFrame():
    def __init__(self, model, model_params,):
        """this class is used to initialize the model, add some constant to model,
        like time step, total steps. Besides, power in and out of every node will be balanced here.

        Args:
            model (ConcreteModel): the object of model
            model_params (dict): some parameters of model. for example, time step, discount rate, serve year. detail see ./params/model.json
        """
        self.m = model
        self.m.time_step_size = Param(
            within=NonNegativeIntegers, initialize=model_params['time_step_size'])  # unit minute
        self.m.time_intervel_hour = self.m.time_step_size/60  # type: ignore # unit hour
        self.m.time_step_count = RangeSet(1, 7*24*60/self.m.time_step_size) # type: ignore        
        self.m.cost_investment = 0
        self.m.cashflow = 0
        self.m.discount_rate = Param(
            within=NonNegativeReals, initialize=model_params['discount_rate'],mutable=True)
        # self.m.discount_rate = model_params['discount_rate']
        self.m.serve_year = Param(
            within=NonNegativeIntegers, initialize=model_params['serve_year'],mutable=True)
        # self.m.serve_year = model_params['serve_year']
        # if the value of bigM exceed 1e5, a Problem will arise by using this too big value in component Inverter
        self.m.add_component('bigM', Param(
            within=NonNegativeIntegers, initialize=1e9))
        # nodes store here
        self.m.nodes = []
        # scaling factor
        self.m.scale_factor_week2year = Param(within=NonNegativeReals,initialize = 365/7)
        self.power_balanced = False
        self.obj_built = False

    def _build_obj(self):
        """build objective function
        """
        self.m.NPV = self.m.cashflow*sum([(1+self.m.discount_rate) **
                                          -j for j in range(1,value(self.m.serve_year)+1,1)])-self.m.cost_investment
        self.m.Obj = Objective(expr=self.m.NPV, sense=maximize)
        self.obj_built = True

    def _balance_power_of_all_nodes(self):
        for node in self.m.nodes:
            node.balance_power()
        self.power_balanced = True

    def solve(self, solver="Gurobi"):
        """solve the model

        Args:
            solver (str): the milp solver,that used to solve the module. for example, gurobi
        """
        
        
        # solve method may be repeatedlly executed. 
        # The following codes are used to advoid exception of redefining model component
        if not self.obj_built:
            self._build_obj()
        if not self.power_balanced:
            self._balance_power_of_all_nodes()
        opt = SolverFactory(solver)
        result = opt.solve(self.m)
        return result

    def print_var(self, var):
        """print the decision variables 

        Args:
            var (str): the name of a variable. You can use the Component.get_variables() to get the string list of the name of decision varibales.
        """
        var_data = [value(self.m.component(var)[i])
                    for i in self.m.component(var)]
        print(var_data)

    def show_line_chart(self,*vars):
        data = pd.read_csv('sources/result_data/com_data.csv')
        data['date'] = data.apply(lambda x: dt.strptime(
            x['date'], '%Y-%m-%d %H:%M:%S'), axis=1)
        data_buffer = {}
        data_buffer['date'] = data['date']
        for var in vars:
            data_buffer[var] =  [value(self.m.component(var)[i]) for i in self.m.component(var)]
        data_pd = pd.DataFrame(data_buffer)
        data_pd.set_index('date', drop=True, inplace=True)
        def show_figure(fig):
            # create a dummy figure and use its
            # manager to display "fig"  
            dummy = plt.figure()
            new_manager = dummy.canvas.manager
            new_manager.canvas.figure = fig
            fig.set_canvas(new_manager.canvas)
        fig = self._generate_line_chart(data_pd)
        show_figure(fig)
        fig.show()
        # while True:
        #     pass
        
    def save_line_chart(self, path,*vars,**kwargs):
        data = pd.read_csv(r'model\assets\com_data.csv')
        data['date'] = data.apply(lambda x: dt.strptime(
            x['date'], '%Y-%m-%d %H:%M:%S'), axis=1)
        data_buffer = {}
        data_buffer['date'] = data['date']
        for var in vars:
            data_buffer[var] =  [value(self.m.component(var)[i]) for i in self.m.component(var)]
        data_pd = pd.DataFrame(data_buffer)
        data_pd.set_index('date', drop=True, inplace=True)
        def show_figure(fig):
            # create a dummy figure and use its
            # manager to display "fig"  
            dummy = plt.figure()
            new_manager = dummy.canvas.manager
            new_manager.canvas.figure = fig
            fig.set_canvas(new_manager.canvas)
        fig = self._generate_line_chart(data_pd, ylabel=kwargs['ylabel'] if 'ylabel' in kwargs.keys() else 'power in kW')
        show_figure(fig)
        fig.savefig(path,bbox_inches='tight')
        
    def set_canvas(self,fig):
        # create a dummy figure and use its
        # manager to display "fig"  
        dummy = plt.figure()
        new_manager = dummy.canvas.manager
        new_manager.canvas.figure = fig
        fig.set_canvas(new_manager.canvas)
    
    def get_comp_powerflow_data(self,data_descp,*components):
        """get the merged data of components in format JSON

        Args:
            data_descp (string): Description of data, may used as ylabel of a chart
            *components (*compontent[]):  destructed list of components of model
        """     
        data = pd.read_csv(r'model\assets\com_data.csv')
        data['date'] = data.apply(lambda x: dt.strptime(
            x['date'], '%Y-%m-%d %H:%M:%S'), axis=1)
        data_buffer = {}
        data_buffer['date'] = data['date']
        for comp in components:
            data_buffer[comp.getname()] =  [value(comp[i]) for i in comp]
        data_pd = pd.DataFrame(data_buffer)
        json_str = data_pd.to_json(orient='records')
        dict_data = json.loads(json_str)
        return dict_data
    
    def get_node_powerflow_data(self,node:Node):
        data = pd.read_csv(r"model\assets\com_data.csv")
        data['date'] = data.apply(lambda x: dt.strptime(
            x['date'], '%Y-%m-%d %H:%M:%S'), axis=1)
        data_buffer = {}
        powerIn = node.powerIn
        powerOut = node.powerOut
        data_buffer['date'] = data['date']
        for comp in powerIn:
            data_buffer[comp.getname()] =  [value(comp[i]) for i in comp]
        for comp in powerOut:
            data_buffer[comp.getname()] =  [-value(comp[i]) for i in comp] 
        data_pd = pd.DataFrame(data_buffer)
        json_str = data_pd.to_json(orient='records')
        dict_data = json.loads(json_str)
        return dict_data
    
    def get_comp_powerflow_figure(self,ylabel,*components):
        data = pd.read_csv(r'model\assets\com_data.csv')
        data['date'] = data.apply(lambda x: dt.strptime(
            x['date'], '%Y-%m-%d %H:%M:%S'), axis=1)
        data_buffer = {}
        data_buffer['date'] = data['date']
        for comp in components:
            data_buffer[comp.getname()] =  [value(comp[i]) for i in comp]
        data_pd = pd.DataFrame(data_buffer)
        data_pd.set_index('date', drop=True, inplace=True)
        return self._generate_line_chart(data_pd,ylabel=ylabel)
    
    def get_node_powerflow_figure(self,node:Node):
        data = pd.read_csv(r"model\assets\com_data.csv")
        data['date'] = data.apply(lambda x: dt.strptime(
            x['date'], '%Y-%m-%d %H:%M:%S'), axis=1)
        data_buffer = {}
        powerIn = node.powerIn
        powerOut = node.powerOut
        data_buffer['date'] = data['date']
        for comp in powerIn:
            data_buffer[comp.getname()] =  [value(comp[i]) for i in comp]
        for comp in powerOut:
            data_buffer[comp.getname()] =  [-value(comp[i]) for i in comp] 
        data_pd = pd.DataFrame(data_buffer)
        data_pd.set_index('date', drop=True, inplace=True)
        return self._generate_line_chart(data_pd,ylabel='power in kW')
    
    def beautify_label_text(self,old_label:str) -> str:
        new_label = old_label.replace('_in', ' input').replace('_out', ' output').replace('_', ' ')
        new_label = new_label.split('&')[0]
        return new_label

    def _generate_line_chart(self,data, title='', ylabel=''):
        weeklist = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        monday = dt.strptime("10 10 2022 00:00", "%d %m %Y %H:%M")

        def my_formatter(date, pos):
            try:
                if pos % 4 == 0:
                    return weeklist[int(pos/4)]
                elif pos % 4 == 1:
                    return '6'
                elif pos % 4 == 2:
                    return '12'
                elif pos % 4 == 3:
                    return '18'
            except:
                return '24'
        fig = Figure(figsize=(12, 5), dpi=500)
        ax = fig.add_subplot(111)
        
        for col_name, data in data.items():
            if '_' in col_name:
                label = self.beautify_label_text(col_name)
            else:
                label = ''
            # linestyle = '--' if 'Average' not in col_name and 'Median' not in col_name else '-'
            ax.plot(data.index, data, label=label)
        ax.axhline(y=0, color='b', linestyle='-')
        ax.axis(xmin=monday,xmax=data.index[-1])
        ax.xaxis.set_major_locator(HourLocator(byhour=range(0, 24, 6)))
        ax.xaxis.set_major_formatter(my_formatter)
        ax.set_ylabel(ylabel)
        ax.set_title(title if title else '')
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.15,
                 box.width, box.height * 0.85])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),ncol=2)
        # plt.savefig('sources/result_figures/Power_flow_with_PV_and_BSS.png')
        return fig
    
 