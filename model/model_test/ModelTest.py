import sys
import os

# add the project path to sys.path, so that model file can be found in .common/solve.py 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir =os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from pyomo.environ import *

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource


class ModelTest:
    def __init__(self,modelframe) -> None:
       self.modelframe = modelframe
    
    def _test_two_params(self,fst_param:dict,scd_param:dict,*observe_vals):
        model = self.modelframe.get_model()
        result = {}
        result[fst_param['name']] =[]
        result[scd_param['name']] =[]
        for observe_val in observe_vals:
            result[observe_val]=[]
        
        count = 1
        total_count = len(fst_param["range"])*len(scd_param["range"])
        for fst_param_val in fst_param["range"]:
            for scd_param_val in scd_param["range"]:
                model.component(fst_param['name']).value = fst_param_val
                model.component(scd_param['name']).value = scd_param_val
                self.modelframe.solve('gurobi')
                result[fst_param["name"]].append(value(model.component(fst_param['name'])))
                result[scd_param["name"]].append(value(model.component(scd_param['name'])))
                
                for observe_val in observe_vals:
                    result[observe_val].append(value(model.component(observe_val)))   
                print(count,'/',total_count)
                count = count+1
        df = pd.DataFrame(result)
        return df
    
    def test_model_two_params(self,dest_filepath:str,fst_param:dict,scd_param:dict,*observe_vals):
        df_temp = self._test_two_params(fst_param,scd_param,*observe_vals)
        df_temp.to_csv(dest_filepath)
        
    def _determine_inverted_state(self,xData,yData,zData):
        z_max = max(zData)
        data = {'x':xData,'y':yData,'z':zData}
        df = pd.DataFrame(data)
        df_xy = df.loc[df['z'] == z_max, ['x', 'y']]
        if(max(xData)-df_xy['x'].iloc[0]>df_xy['x'].iloc[0]-min(xData)):
            is_x_invert = False
        else:
            is_x_invert = True
        if(max(yData)-df_xy['y'].iloc[0]>df_xy['y'].iloc[0]-min(yData)):
            is_y_invert = True
        else:
            is_y_invert = False
        # def is_invert_needed(sorted_df):
        #     if(sorted_df['z'].iloc[0]>=sorted_df['z'].iloc[-1]):
        #         return True
        #     else:
        #         return False
        # # data = {'x':xData,'y':yData,'z':zData}
        # # df = pd.DataFrame(data)
        # df_yz = df.loc[df['x'] == df['x'].iloc[0], ['y', 'z']]
        # sorted_df_y = df_yz.sort_values(by='y')
        # is_y_invert = is_invert_needed(sorted_df_y)
        # df_xz = df.loc[df['y'] == df['y'].iloc[0], ['x', 'z']]
        # sorted_df_x = df_xz.sort_values(by='x')
        # is_x_invert = not is_invert_needed(sorted_df_x)
        return (is_x_invert,is_y_invert)
        
        
        
    
    def _histogram3D(self,xData,yData,zData,xlabel=None,ylabel=None,zlabel=None,azdeg=315,isNPV=False):
        
        
        fig = plt.figure(figsize=(6, 5),dpi=300)  # 画布宽长比例
        ax1 = fig.add_subplot(111, projection='3d')
        zData = np.array(zData)
        if(isNPV):
            zData = zData/1e5
        bottom = np.zeros_like(zData)
        bottom = min(zData)
        ax1.set_xlabel(xlabel,fontsize=10)# type: ignore   
        ax1.set_ylabel(ylabel,fontsize=10)# type: ignore   
        ax1.set_zlabel(zlabel,fontsize=11)# type: ignore 
        # ax1.invert_yaxis()
        
        invert_x,invert_y = self._determine_inverted_state(xData,yData,zData)
        # the axis start from minimum or maximum
        if(invert_y):
            ax1.set_ylim(max(yData),min(yData))
        if(invert_x):
            ax1.set_xlim(max(xData),min(xData))
        
        lightsource = LightSource(azdeg=azdeg)
        
        _xData = list(set(xData))
        _yData = list(set(yData))
        dy = (max(_yData)-min(_yData))/(len(_yData)-1)*0.8
        dx = (max(_xData)-min(_xData))/(len(_xData)-1)*0.8

        dz = np.array(zData)
        
        # set colors of the bars, different dz has different color
        if((dz.max() - dz.min()) != 0):
            colors = plt.cm.jet((dz.flatten() - dz.min()) / (dz.max() - dz.min()))
        else:
            colors = plt.cm.jet((dz.flatten() - dz.min()))        
        
        ax1.bar3d(xData, yData, bottom, dx = dx, dy = dy, dz=np.array(zData)-bottom,shade=True ,color=colors,lightsource=lightsource)# type: ignore    
        cbar = fig.colorbar(plt.cm.ScalarMappable(cmap = 'jet'), ax = ax1,ticks=[0, 0.5, 1], pad=0.1)
        cbar.ax.set_yticklabels([round(dz.min(),2),round((dz.min()+dz.max())/2,2),round(dz.max(),2)])
        return plt
    
    def save_3d_chart(self,src_filepath,dest_folderpath,xlabel=None,ylabel=None):
        pd_data = pd.read_csv(src_filepath)
        x = pd_data.iloc[:,1].to_list()
        y = pd_data.iloc[:,2].to_list()
        for col_index in pd_data.index:
            if(col_index not in (0,1,2)):
                print(col_index)
                z = pd_data.iloc[:,col_index].to_list()
                if('Obj' in pd_data.columns[col_index]):
                    zlabel = 'NPV(€)'
                elif('power_capacity_' in pd_data.columns[col_index]):
                    zlabel = 'BSS power capacity(kW)'
                elif('energy_capacity_' in pd_data.columns[col_index]):
                    zlabel = 'BSS energy capacity(kWh)'
                elif('power_rated_' in pd_data.columns[col_index]):
                    zlabel = 'PV rated power(kW)'
                elif('power_peak' in pd_data.columns[col_index]):
                    zlabel = 'Grid peak power(kW)'
                plt = self._histogram3D(x,y,z,xlabel if(xlabel) else pd_data.columns[1],ylabel if(ylabel) else pd_data.columns[2],zlabel if(zlabel) else pd_data.columns[col_index])
                plt.savefig(os.path.join(dest_folderpath, f'{pd_data.columns[col_index]}.png'))
                
    def show_3d_chart(self,src_filepath,z_col_name:str,x_label=None,y_label=None):
        pd_data = pd.read_csv(src_filepath)
        x = pd_data.iloc[:,1].to_list()
        y = pd_data.iloc[:,2].to_list()
        z = pd_data[z_col_name].to_list()
        if('Obj' in z_col_name):
            zlabel = 'NPV(€)'
        elif('power_capacity_' in z_col_name):
            zlabel = 'BSS power capacity(kW)'
        elif('energy_capacity_' in z_col_name):
            zlabel = 'BSS energy capacity(kWh)'
        elif('power_rated_' in z_col_name):
            zlabel = 'PV rated power(kW)'
        elif('power_peak' in z_col_name):
            zlabel = 'Grid peak power(kW)'
        plt = self._histogram3D(x,y,z,x_label if(x_label) else pd_data.columns[1],y_label if(y_label) else pd_data.columns[2],zlabel if(zlabel) else z_col_name)
        plt.show()