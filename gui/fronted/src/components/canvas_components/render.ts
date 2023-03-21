import type LogicFlow from "@logicflow/core";
export default (lf:LogicFlow)=>{
    lf.render({
        "nodes": [
            {
                "id": "f7607b14-afbb-479c-9e5d-c75c7f315217",
                "type": "grid",
                "x": 240,
                "y": 400,
                "properties": {
                    "node_ac": {
                        "value": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                        "name": "Connected AC node",
                        "unit": ""
                    },
                    "power_grid_max": {
                        "value": 312,
                        "name": "Maximum power suply",
                        "unit": "kW"
                    },
                    "cost_grid_connection": {
                        "value": 5000,
                        "name": "Connection cost",
                        "unit": "EUR"
                    },
                    "peak_demand_rate": {
                        "value": 600,
                        "name": "Annual peak demand rate",
                        "unit": "EUR"
                    },
                    "ele_price": {
                        "value": 0.34,
                        "name": "Electricity price",
                        "unit": "EUR"
                    }
                },
                "text": {
                    "x": 224,
                    "y": 400,
                    "value": "Grid"
                }
            },
            {
                "id": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                "type": "node",
                "x": 340,
                "y": 400,
                "properties": {
                    "name": {
                        "value": "ac",
                        "name": "Node text",
                        "unit": ""
                    }
                }
            },
            {
                "id": "88831a7e-1eed-4b0d-9526-3d121cb0fe24",
                "type": "cs",
                "x": 420,
                "y": 520,
                "properties": {
                    "node_ac": {
                        "value": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                        "name": "Connected AC node",
                        "unit": ""
                    },
                    "number_ports": {
                        "value": 6,
                        "name": "Charging port number",
                        "unit": "port"
                    },
                    "cost_hardware": {
                        "value": 1000,
                        "name": "Hardware cost per port",
                        "unit": "EUR"
                    },
                    "cost_installation": {
                        "value": 1000,
                        "name": "Installation cost per port",
                        "unit": "EUR"
                    },
                    "cost_operation_maintanence": {
                        "value": 1000,
                        "name": "Annual operation and maintanence cost",
                        "unit": "EUR"
                    },
                    "price_ele_sell": {
                        "value": 0.4,
                        "name": "Electricity price",
                        "unit": "EUR"
                    },
                    "power_demand_filepath": {
                        "value": "model/data/cs_power_data.json",
                        "name": "Filepath of power demand data",
                        "unit": ""
                    }
                },
                "text": {
                    "x": 419,
                    "y": 510,
                    "value": "Charging station"
                }
            },
            {
                "id": "6f2fd298-1787-4b37-848a-4a096b4c4402",
                "type": "company",
                "x": 640,
                "y": 520,
                "properties": {
                    "node_ac": {
                        "value": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                        "name": "Connected AC node",
                        "unit": ""
                    },
                    "power_demand_filepath": {
                        "value": "model/data/com_power_data.json",
                        "name": "Filepath of power demand data",
                        "unit": ""
                    }
                },
                "text": {
                    "x": 640,
                    "y": 510,
                    "value": "Company"
                }
            },
            {
                "id": "00cdb3bc-af9d-4119-aa6b-f9f3d02bf326",
                "type": "bss",
                "x": 420,
                "y": 120,
                "properties": {
                    "node_dc": {
                        "value": "399df6a2-6f96-4b72-8a47-6826f235bdf1",
                        "name": "Connected DC node",
                        "unit": ""
                    },
                    "efficiency_discharge": {
                        "value": 0.9,
                        "name": "Discharging efficiency",
                        "unit": ""
                    },
                    "efficiency_charge": {
                        "value": 0.9,
                        "name": "Charging efficiency",
                        "unit": ""
                    },
                    "lifecycle": {
                        "value": 3000,
                        "name": "Discharging efficiency",
                        "unit": ""
                    },
                    "cost_investment_per_kwh": {
                        "value": 408,
                        "name": "Cost of investing in energy capacity",
                        "unit": "EUR"
                    },
                    "cost_investment_per_kw": {
                        "value": 156,
                        "name": "Cost of investing in power capacity",
                        "unit": "EUR"
                    },
                    "cost_o&m_per_kw_year": {
                        "value": 4,
                        "name": "Annual maintenance and operation cost per kW",
                        "unit": "EUR"
                    },
                    "soc_initial": {
                        "value": 30,
                        "name": "Initial SoC",
                        "unit": "%"
                    },
                    "price_recycle_per_kg": {
                        "value": 0.47,
                        "name": "Recycling price per kg of battery",
                        "unit": "EUR"
                    },
                    "energy_density": {
                        "value": 0.1,
                        "name": "Energy density of battery",
                        "unit": "kWh/kg"
                    },
                    "cost_battery_purchasing_per_kwh": {
                        "value": 185,
                        "name": "Purchase price per kWh of battery",
                        "unit": "EUR"
                    },
                    "soc_min": {
                        "value": 15,
                        "name": "Minimum SoC",
                        "unit": "%"
                    },
                    "soc_max": {
                        "value": 85,
                        "name": "Maximum SoC",
                        "unit": "%"
                    },
                    "power_fluctuation_penalty_weight": {
                        "value": 0.00001,
                        "name": "Penalty weight for limitation of power fluctuation",
                        "unit": ""
                    }
                },
                "text": {
                    "x": 348,
                    "y": 44,
                    "value": "BSS"
                }
            },
            {
                "id": "399df6a2-6f96-4b72-8a47-6826f235bdf1",
                "type": "node",
                "x": 420,
                "y": 200,
                "properties": {
                    "name": {
                        "value": "node_holder",
                        "name": "Node text",
                        "unit": ""
                    }
                }
            },
            {
                "id": "6ae2a8d8-519b-4d52-acf1-b4cf97aa0fc1",
                "type": "inverter",
                "x": 640,
                "y": 300,
                "properties": {
                    "node_dc": {
                        "value": "a0d8040b-a700-40d8-9a65-4d51d37c6921",
                        "name": "Connected DC node",
                        "unit": ""
                    },
                    "node_ac": {
                        "value": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                        "name": "Connected AC node",
                        "unit": ""
                    },
                    "efficiency": {
                        "value": 0.968,
                        "name": "Power conversion efficiency",
                        "unit": ""
                    },
                    "cost_per_kw": {
                        "value": 82,
                        "name": "Investment cost per kW",
                        "unit": "EUR"
                    }
                },
                "text": {
                    "x": 738,
                    "y": 224,
                    "value": "Inverter"
                }
            },
            {
                "id": "5f8081e5-daec-4f17-bd3b-f577aba0ff2d",
                "type": "pvmodule",
                "x": 640,
                "y": 140,
                "properties": {
                    "node_dc": {
                        "value": "a0d8040b-a700-40d8-9a65-4d51d37c6921",
                        "name": "Connected node",
                        "unit": ""
                    },
                    "module_area": {
                        "value": 1,
                        "name": "Surface area of module",
                        "unit": "m^2"
                    },
                    "irradiance_stc": {
                        "value": 1,
                        "name": "Irradiance under standard test condition",
                        "unit": "kW/m^2"
                    },
                    "efficiency_module": {
                        "value": 0.19,
                        "name": "Power conversion efficiency",
                        "unit": ""
                    },
                    "power_stc": {
                        "value": 0.24,
                        "name": "Nominal power under standard test condition",
                        "unit": "kW"
                    },
                    "temperature_coefficient": {
                        "value": 0.003,
                        "name": "Temperature coefficient of power of PV module",
                        "unit": ""
                    },
                    "temperature_cell_stc": {
                        "value": 25,
                        "name": "Cell temperatureunder standard test condition",
                        "unit": "℃"
                    },
                    "temperature_noc": {
                        "value": 44,
                        "name": "Nominal operation cell temperature",
                        "unit": "℃"
                    },
                    "area_max": {
                        "value": 9999,
                        "name": "Maximum available installation area",
                        "unit": "m^2"
                    },
                    "price_invest_per_kw": {
                        "value": 1500,
                        "name": "Investment cost of PV module per kW",
                        "unit": "EUR"
                    },
                    "ambient_temperature_filepath": {
                        "value": "model/data/ambient_temp.json",
                        "name": "Path of ambient temperature data",
                        "unit": ""
                    },
                    "global_irradiance_filepath": {
                        "value": "model/data/irradiance.json",
                        "name": "Path of global irradiance data",
                        "unit": ""
                    }
                },
                "text": {
                    "x": 735,
                    "y": 74,
                    "value": "PV Module"
                }
            },
            {
                "id": "a0d8040b-a700-40d8-9a65-4d51d37c6921",
                "type": "node",
                "x": 640,
                "y": 220,
                "properties": {
                    "name": {
                        "value": "node_holder",
                        "name": "Node text",
                        "unit": ""
                    }
                }
            },
            {
                "id": "03012de2-3bd5-4a65-becc-4f55f6a06814",
                "type": "pcs",
                "x": 420,
                "y": 280,
                "properties": {
                    "node_dc": {
                        "value": "399df6a2-6f96-4b72-8a47-6826f235bdf1",
                        "name": "Connected DC node",
                        "unit": ""
                    },
                    "node_ac": {
                        "value": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                        "name": "Connected AC node",
                        "unit": ""
                    },
                    "efficiency": {
                        "value": 0.98,
                        "name": "Power conversion efficiency",
                        "unit": ""
                    },
                    "pirce_per_kw": {
                        "value": 140,
                        "name": "Investment cost per kW",
                        "unit": "EUR"
                    }
                },
                "text": {
                    "x": 270,
                    "y": 202,
                    "value": "Power conversion system"
                }
            }
        ],
        "edges": [
            {
                "id": "ad7b3b5b-0418-48fc-b6e5-da5ec2d089ed",
                "type": "mypolyline",
                "sourceNodeId": "f7607b14-afbb-479c-9e5d-c75c7f315217",
                "targetNodeId": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                "startPoint": {
                    "x": 275,
                    "y": 400
                },
                "endPoint": {
                    "x": 330,
                    "y": 400
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 275,
                        "y": 400
                    },
                    {
                        "x": 305,
                        "y": 400
                    },
                    {
                        "x": 305,
                        "y": 400
                    },
                    {
                        "x": 300,
                        "y": 400
                    },
                    {
                        "x": 300,
                        "y": 400
                    },
                    {
                        "x": 330,
                        "y": 400
                    }
                ]
            },
            {
                "id": "c4695ffa-ad14-4061-b5e1-e37ce2933c0d",
                "type": "mypolyline",
                "sourceNodeId": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                "targetNodeId": "88831a7e-1eed-4b0d-9526-3d121cb0fe24",
                "startPoint": {
                    "x": 350,
                    "y": 400
                },
                "endPoint": {
                    "x": 420,
                    "y": 485
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 350,
                        "y": 400
                    },
                    {
                        "x": 420,
                        "y": 400
                    },
                    {
                        "x": 420,
                        "y": 485
                    }
                ]
            },
            {
                "id": "60c7c882-f4c4-492d-981f-86c197965d52",
                "type": "mypolyline",
                "sourceNodeId": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                "targetNodeId": "6f2fd298-1787-4b37-848a-4a096b4c4402",
                "startPoint": {
                    "x": 350,
                    "y": 400
                },
                "endPoint": {
                    "x": 640,
                    "y": 485
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 350,
                        "y": 400
                    },
                    {
                        "x": 640,
                        "y": 400
                    },
                    {
                        "x": 640,
                        "y": 485
                    }
                ]
            },
            {
                "id": "915e6351-1e8c-43eb-8a17-774e8e9e37cb",
                "type": "mypolyline",
                "sourceNodeId": "a0d8040b-a700-40d8-9a65-4d51d37c6921",
                "targetNodeId": "5f8081e5-daec-4f17-bd3b-f577aba0ff2d",
                "startPoint": {
                    "x": 640,
                    "y": 210
                },
                "endPoint": {
                    "x": 640,
                    "y": 175
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 640,
                        "y": 210
                    },
                    {
                        "x": 640,
                        "y": 180
                    },
                    {
                        "x": 640,
                        "y": 180
                    },
                    {
                        "x": 640,
                        "y": 205
                    },
                    {
                        "x": 640,
                        "y": 205
                    },
                    {
                        "x": 640,
                        "y": 175
                    }
                ]
            },
            {
                "id": "e7752234-6dec-47f1-91ad-ad586377609c",
                "type": "mypolyline",
                "sourceNodeId": "a0d8040b-a700-40d8-9a65-4d51d37c6921",
                "targetNodeId": "6ae2a8d8-519b-4d52-acf1-b4cf97aa0fc1",
                "startPoint": {
                    "x": 640,
                    "y": 230
                },
                "endPoint": {
                    "x": 640,
                    "y": 265
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 640,
                        "y": 230
                    },
                    {
                        "x": 640,
                        "y": 260
                    },
                    {
                        "x": 640,
                        "y": 260
                    },
                    {
                        "x": 640,
                        "y": 235
                    },
                    {
                        "x": 640,
                        "y": 235
                    },
                    {
                        "x": 640,
                        "y": 265
                    }
                ]
            },
            {
                "id": "7ac2ba2d-7a89-448c-af58-9070a5d15dff",
                "type": "mypolyline",
                "sourceNodeId": "6ae2a8d8-519b-4d52-acf1-b4cf97aa0fc1",
                "targetNodeId": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                "startPoint": {
                    "x": 640,
                    "y": 335
                },
                "endPoint": {
                    "x": 350,
                    "y": 400
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 640,
                        "y": 335
                    },
                    {
                        "x": 640,
                        "y": 400
                    },
                    {
                        "x": 350,
                        "y": 400
                    }
                ]
            },
            {
                "id": "16997217-49ad-4d37-81d0-48043e03e207",
                "type": "mypolyline",
                "sourceNodeId": "399df6a2-6f96-4b72-8a47-6826f235bdf1",
                "targetNodeId": "00cdb3bc-af9d-4119-aa6b-f9f3d02bf326",
                "startPoint": {
                    "x": 420,
                    "y": 190
                },
                "endPoint": {
                    "x": 420,
                    "y": 155
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 420,
                        "y": 190
                    },
                    {
                        "x": 420,
                        "y": 160
                    },
                    {
                        "x": 420,
                        "y": 160
                    },
                    {
                        "x": 420,
                        "y": 185
                    },
                    {
                        "x": 420,
                        "y": 185
                    },
                    {
                        "x": 420,
                        "y": 155
                    }
                ]
            },
            {
                "id": "6c123503-805a-4e30-984a-257cdd31bfdf",
                "type": "mypolyline",
                "sourceNodeId": "03012de2-3bd5-4a65-becc-4f55f6a06814",
                "targetNodeId": "399df6a2-6f96-4b72-8a47-6826f235bdf1",
                "startPoint": {
                    "x": 420,
                    "y": 245
                },
                "endPoint": {
                    "x": 420,
                    "y": 210
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 420,
                        "y": 245
                    },
                    {
                        "x": 420,
                        "y": 215
                    },
                    {
                        "x": 420,
                        "y": 215
                    },
                    {
                        "x": 420,
                        "y": 240
                    },
                    {
                        "x": 420,
                        "y": 240
                    },
                    {
                        "x": 420,
                        "y": 210
                    }
                ]
            },
            {
                "id": "83277c41-fb23-4012-ba09-e3ed905bf5f3",
                "type": "mypolyline",
                "sourceNodeId": "03012de2-3bd5-4a65-becc-4f55f6a06814",
                "targetNodeId": "f44c446e-91f6-4d3c-892f-53f2f988c131",
                "startPoint": {
                    "x": 420,
                    "y": 315
                },
                "endPoint": {
                    "x": 350,
                    "y": 400
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 420,
                        "y": 315
                    },
                    {
                        "x": 420,
                        "y": 400
                    },
                    {
                        "x": 350,
                        "y": 400
                    }
                ]
            }
        ]
    });
}