import type LogicFlow from "@logicflow/core";
export default (lf:LogicFlow)=>{
    lf.render({
        "nodes": [
            {
                "id": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
                "type": "node",
                "x": 440,
                "y": 280,
                "properties": {
                    "name": {
                        "value": "node_holder",
                        "name": "Node text",
                        "unit": ""
                    }
                }
            },
            {
                "id": "c89c5c5d-64dc-4daa-a79a-0bcf75a9eb1b",
                "type": "pvmodule",
                "x": 260,
                "y": 280,
                "properties": {
                    "node_dc": {
                        "value": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
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
                        "value": 200,
                        "name": "Maximum available installation area",
                        "unit": "m^2"
                    },
                    "price_invest_per_kw": {
                        "value": 2000,
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
                    "x": 260,
                    "y": 440,
                    "value": "PV Module"
                }
            },
            {
                "id": "c247aece-dab9-47cb-8da5-f9c88f50c4f1",
                "type": "bss",
                "x": 600,
                "y": 120,
                "properties": {
                    "node_dc": {
                        "value": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
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
                    "x": 600,
                    "y": 248,
                    "value": "BSS"
                }
            },
            {
                "id": "fc0afc39-fe1c-457e-aa66-108210ad0aa8",
                "type": "grid",
                "x": 600,
                "y": 280,
                "properties": {
                    "node_ac": {
                        "value": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
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
                    "ele_price_buy": {
                        "value": 0.34,
                        "name": "Electricity price",
                        "unit": "EUR"
                    },
                    "ele_price_sell": {
                        "value": 0.28,
                        "name": "Feed-in tarif",
                        "unit": "EUR"
                    }
                },
                "text": {
                    "x": 600,
                    "y": 408,
                    "value": "Grid"
                }
            },
            {
                "id": "f3795f9a-b742-41a5-9455-2d9c5166caaf",
                "type": "cs",
                "x": 600,
                "y": 440,
                "properties": {
                    "node_ac": {
                        "value": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
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
                    "x": 600,
                    "y": 568,
                    "value": "Charging station"
                }
            }
        ],
        "edges": [
            {
                "id": "5b68ae20-7c20-4a6d-b232-9fa6b2fd49a6",
                "type": "mypolyline",
                "sourceNodeId": "c89c5c5d-64dc-4daa-a79a-0bcf75a9eb1b",
                "targetNodeId": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
                "startPoint": {
                    "x": 309,
                    "y": 280
                },
                "endPoint": {
                    "x": 425,
                    "y": 280
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 309,
                        "y": 280
                    },
                    {
                        "x": 425,
                        "y": 280
                    }
                ]
            },
            {
                "id": "62a92745-cbb9-4521-a72e-76f387d88b73",
                "type": "mypolyline",
                "sourceNodeId": "fc0afc39-fe1c-457e-aa66-108210ad0aa8",
                "targetNodeId": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
                "startPoint": {
                    "x": 555,
                    "y": 280
                },
                "endPoint": {
                    "x": 455,
                    "y": 280
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 555,
                        "y": 280
                    },
                    {
                        "x": 455,
                        "y": 280
                    }
                ]
            },
            {
                "id": "502b25eb-1b7e-4645-afaa-e364b93373a3",
                "type": "mypolyline",
                "sourceNodeId": "c247aece-dab9-47cb-8da5-f9c88f50c4f1",
                "targetNodeId": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
                "startPoint": {
                    "x": 550,
                    "y": 120
                },
                "endPoint": {
                    "x": 455,
                    "y": 280
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 550,
                        "y": 120
                    },
                    {
                        "x": 485,
                        "y": 120
                    },
                    {
                        "x": 485,
                        "y": 280
                    },
                    {
                        "x": 455,
                        "y": 280
                    }
                ]
            },
            {
                "id": "3e6869dc-1ba7-4111-bef3-c4371e5bba93",
                "type": "mypolyline",
                "sourceNodeId": "f3795f9a-b742-41a5-9455-2d9c5166caaf",
                "targetNodeId": "f8f18b64-3a05-411e-9fb8-a1e008e64d2c",
                "startPoint": {
                    "x": 550,
                    "y": 440
                },
                "endPoint": {
                    "x": 455,
                    "y": 280
                },
                "properties": {},
                "pointsList": [
                    {
                        "x": 550,
                        "y": 440
                    },
                    {
                        "x": 485,
                        "y": 440
                    },
                    {
                        "x": 485,
                        "y": 280
                    },
                    {
                        "x": 455,
                        "y": 280
                    }
                ]
            }
        ]
    });
}