import * as echarts from 'echarts';
import type { ResultData } from './sse';
export interface PowerData {
    [key: string]: number;
}

const getYAxisDataSeries = (powerData:PowerData[])=>{
    interface YAxisData {
        name: string;
        type: 'line',
        data: number[];
      }
      
      // get data name
      const names = Object.keys(powerData[0]).slice(1);
      
      // extract value of this data name
      const resultData = [];
      for (let i = 0; i < names.length; i++) {
        const name = beautyLabelName(names[i]);
        const data = powerData.map(item => item[names[i]].toFixed(3));
        resultData.push({ name, type:'line',data });
      }
      return resultData
}

 // 将时间戳转换为日期字符串
 const formatTime = (timestamp: number) => {
    const date = new Date(timestamp);
    const weekday = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][date.getDay()];
    const hour = date.getHours().toString().padStart(2, '0');
    const minute = date.getMinutes().toString().padStart(2, '0');
    return `${weekday}\n${hour}:${minute}`;
  }


const getXAxisData = (data:PowerData[])=>{
    const xAxisData = [];
    for (let i = 0; i < data.length; i++) {
        const item = data[i];
        const time = formatTime(item["date"]);
        xAxisData.push(time);
      }
    return xAxisData
}

export const beautyLabelName = (name:string)=>{
    let newName = name.split('&')[0]
    newName = newName.replace('_out_',' output ')
    newName = newName.replace('_in_',' input ')
    newName = newName.replace(/_/g,' ')
    console.log(newName)
    return newName
}

export const insertLineChart = (chartContainer:HTMLDivElement,resultData:ResultData)=>{
  const data = resultData.result.data as PowerData[]

  // 提取横坐标和纵坐标数据
  
  const yAxisDataSeries = getYAxisDataSeries(data);
  const xAxisData = getXAxisData(data)
  // 创建 ECharts 实例
  const chart = echarts.init(chartContainer);
  
  // 配置选项
  const option = {
    grid: {
        top: '15%',
        bottom: '15%'
      },
    tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: yAxisDataSeries.map(item=>beautyLabelName(item.name))
      },
    xAxis: {
      type: 'category',
      data: xAxisData,
    },
    yAxis: {
      type: 'value',
      name: resultData.result.title,
      nameLocation: 'middle',
      nameRotate: 90,
    },
    series: yAxisDataSeries
  };
  
  chart.setOption(option);
}

