import json
import random
import string
import openpyxl
from scipy import interpolate
from scipy import integrate
import numpy as np


def read_params(filename):
    """_summary_

    Args:
        filename (str): relative path of json file

    Returns:
        params(dict): a dictionary of parameters if json file exists
        False: if json file does not exist

    """
    with open(filename, 'r') as f:
        params = json.load(f)
        return params

def convert_keys_str2int(dic:dict):
    for key in list(dic):
        dic[int(key)] = dic.pop(key)
    return dic


def list2dict(list, magnification):
    """change a list of data to dictionary of data. 

    Args:
        list (list): a data list 
        magnification (float): all the data will be multiplied by this value

    Returns:
        dic: dictinoary. index is from 1 to the number of data, values are data
    """
    dic = {}
    for index, value in enumerate(list):
        dic[index+1] = value*magnification
    return dic

def generate_random_id():
    # 定义随机字符串中可以包含的字符集，这里使用大小写字母和数字
    characters = string.ascii_letters + string.digits

    # 从字符集中随机选择 10 个字符，并将它们组合成一个字符串
    random_string = ''.join(random.choice(characters) for i in range(10))
    return random_string

def read_cycle_life_data_from_excel(path):
    # open excel file
    wb = openpyxl.load_workbook(path)

    # choose first sheet
    sheet = wb['Sheet1']

    # stroe the data of first colomn to col1_data
    col1_data = [cell.value for cell in sheet['A'][1:] if cell.value is not None]

    # 存储第二列数据到列表col2_data
    col2_data = [cell.value for cell in sheet['B'][1:] if cell.value is not None]
    return col1_data,col2_data

def save_cycle_life_data_to_json(cycle_number,ratio,path):
    data = {'cycle_number':cycle_number,'ratio':ratio}
    with open(path,'w') as fp:
        json.dump(data,fp)

def read_cycle_life_from_json(path):
    with open(path,'r') as fp:
        data = json.load(fp)
    return data['cycle_number'],data['ratio']

def get_cycle_number_by_ratio(cycle_number,ratio,unknow_ratio):
    c = interpolate.interp1d(ratio,cycle_number,kind='linear')
    return c(unknow_ratio)

def integrate_ratio_cycle(cycle_number,ratio,end_ratio=0.8):
    if(cycle_number[0] != 0):
        cycle_number.insert(0,0)
        ratio.insert(0,1)
    r = interpolate.interp1d(cycle_number,ratio,kind='linear')
    cycle_num_by_end_ratio = get_cycle_number_by_ratio(cycle_number,ratio,end_ratio)
    result, error = integrate.quad(r, 0, cycle_num_by_end_ratio)
    return result
