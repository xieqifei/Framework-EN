import json
import random
import string



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