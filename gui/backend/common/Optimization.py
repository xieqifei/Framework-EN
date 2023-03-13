
import io
import os
import re

# add the project path to sys.path, so that model file can be found in .common/solve.py
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))


import base64
import traceback
from .Stream import Stream
from .model_register import model_list
from .GraphData import GraphData
from pyomo.environ import *
from model.consumers import *
from model.base_module import *
from model.components import *

class Optimization:
    def __init__(self, announcer) -> None:
        self.announcer = announcer
        self.stream = Stream(announcer)

    def get_node_by_id(self, nodes, nodeID):
        for node in nodes:
            if node.id == nodeID:
                return node

    def get_node_id_by_element(self, elem, node_type):
        return elem['properties'][node_type]['value']

    def get_node(self, nodes, elem, node_type):
        nodeID = self.get_node_id_by_element(elem, node_type)
        node = self.get_node_by_id(nodes, nodeID)
        return node

    def convert_fig_to_base64(self,fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format='svg')
        buffer.seek(0)
        image_data = buffer.read()
        encoded_image = base64.b64encode(image_data).decode()
        # Use the base64-encoded string in an HTML <img> tag
        img_src = 'data:image/svg+xml;base64,{}'.format(encoded_image)
        return img_src

    def handel_node_stream_fig(self, node):
        fig = self.modelframe.get_node_powerflow_figure(node)
        img_src = self.convert_fig_to_base64(fig)
        self.stream.send_result('node', node.name, node.id, {
            'type': 'img',
            'data': img_src
        })
        
    def handel_node_stream_data(self,node):
        data = self.modelframe.get_node_powerflow_data(node)
        self.stream.send_result('node',node.name, node.id,{
            'type':'data',
            'data':data,
            'title': 'Power in kW'
        })

    
    def add_space_to_camel_case_string(self, s):
        """Convert camel case string to spaced string."""
        pattern = r'(?<!^)(?=[A-Z])'
        s = re.sub(pattern, ' ', s)
        s = s.lower()
        return s

    def handle_element_single_variables(self, elem):
        elem_type = 'component' if isinstance(
            elem, ComponentAPI) else 'consumer'
        if (elem_type != 'consumer'):
            single_variables = elem.get_single_variables()
            data = {}
            for single_var in single_variables:
                var_name = single_var.getname()
                var_name = var_name.replace(f'&{elem.id}', '')
                var_name = var_name.replace("_", ' ')
                # var_name = self.add_space_to_camel_case_string(var_name)
                data[var_name] = value(single_var)
            self.stream.send_result(elem_type, elem.name, elem.id, {
                'type': 'variables',
                'data': data
            })

    def handle_element_series_variables_figure(self, elem):
        elem_type = 'component' if isinstance(
            elem, ComponentAPI) else 'consumer'
        series_variables = elem.get_series_variables()
        for series_variable in series_variables:
            fig = self.modelframe.get_comp_powerflow_figure(
                series_variable['ylabel'], *series_variable['components'])
            img_src = self.convert_fig_to_base64(fig)
            self.stream.send_result(elem_type, elem.name, elem.id, {
                'type': 'img',
                'data': img_src
            })

    def handle_element_series_variables_data(self, elem):
        elem_type = 'component' if isinstance(
            elem, ComponentAPI) else 'consumer'
        series_variables = elem.get_series_variables()
        for series_variable in series_variables:
            data = self.modelframe.get_comp_powerflow_data(
                series_variable['ylabel'], *series_variable['components'])
            self.stream.send_result(elem_type, elem.name, elem.id, {
                'type': 'data',
                'data': data,
                'title':series_variable['ylabel']
            })
    def handle_element_stream(self, elem):
        self.handle_element_series_variables_data(elem)
        self.handle_element_single_variables(elem)

    def handle_solution(self, graphData):
        try:
            self.stream.send_message('Simulation got started.')
            graph = GraphData(graphData)
            model = ConcreteModel()
            self.model_params = read_params(os.path.join(
                root_path, 'model', 'params', 'model.json'))
            self.modelframe = ModelFrame(model, self.model_params)
            # create nodes

            nodes = [Node(model, node['properties']['name']['value'],
                        id=node['id']) for node in graph.get_nodes()]
            elements = []
            # creat components and consumers
            for elem in graph.get_elements():
                elem_temp = model_list[elem['type']](
                    model, elem['text']['value'], graph.get_properties_value(elem['properties']), id=elem['id'])
                # add node to the components and consumers
                if 'node_ac' in elem['properties'] and 'node_dc' in elem['properties']:
                    elem_temp.add2node(self.get_node(
                        nodes, elem, 'node_ac'), self.get_node(nodes, elem, 'node_dc'))
                elif 'node_ac' in elem['properties']:
                    elem_temp.add2node(self.get_node(nodes, elem, 'node_ac'))
                elif 'node_dc' in elem['properties']:
                    elem_temp.add2node(self.get_node(nodes, elem, 'node_dc'))
                elements.append(elem_temp)
            self.stream.send_message('Simulating...')
            self.modelframe.solve('gurobi')
            self.stream.send_success(f'Got result,NPV = {round(value(model.Obj),2)} EUR')
            for node in nodes:
                self.handel_node_stream_data(node)
            for elem in elements:
                self.handle_element_stream(elem)
            self.stream.send_end()

        except Exception as e:
            self.stream.send_error(e)
            self.stream.send_end()
            return 0
