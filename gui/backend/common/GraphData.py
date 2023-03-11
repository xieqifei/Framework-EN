class GraphData:
    def __init__(self,graphData:dict) -> None:
        self.data = graphData
        
    def get_nodes(self):
        nodes = []
        for elem in self.data['nodes']:
            if elem['type'] == 'node':
                nodes.append(elem)
        return nodes
    
    def get_components_by_nodeid(self,nodeID):
        components = []
        for edge in self.data['edges']:
            if(edge['sourceNodeId'] == nodeID):
                for elem in self.data['nodes']:
                    if elem['type'] != 'node' and elem['id'] == edge['targetNodeId']:
                        components.append(elem)
            elif(edge['targetNodeId'] == nodeID):
                for elem in self.data['nodes']:
                    if elem['type'] != 'node' and elem['id'] == edge['sourceNodeId']:
                        components.append(elem)
        return components
    
    def get_parameters_by_elementid(self,elementID):
        for elem in self.data['nodes']:
            if(elem['id'] == elementID):
                return elem['properties']
        return {}
    
    def get_elements(self):
        return list(filter(lambda ele:ele['type'] != 'node',self.data['nodes']))
    
    def get_properties_value(self,properties):
        properties_temp = {}
        for key in properties:
            properties_temp[key] = properties[key]['value']
            
        return properties_temp
    
    