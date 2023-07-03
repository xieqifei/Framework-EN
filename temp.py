from model.base_module.base import *
path = 'degradarion_data.xlsx'
cycle_number, ratio = read_cycle_life_from_json('model\data\cycle_life.json')
print(integrate_ratio_cycle(cycle_number,ratio,0.8))