<template>

        <el-card class = 'chart-card'>
            <template #header>
            <div class="card-header">
                <a :name="data.name+data.id+data.result.title"></a>
                <span>{{ data.name }}:{{ data.result?.title }}</span>
                <!-- <el-button class="button" :icon="FullScreen" circle @click="showLargeChart"></el-button> -->
            </div>
            </template>
            <div ref="chartContainer" class="chart-container">

            </div>
            <!-- <el-dialog v-model="dialogLargeChart" class="large-chart-container">
                <div ref="largeChartContainer"></div>
            </el-dialog> -->
        </el-card>
            
</template>

<script setup lang="ts">
    import {insertLineChart,type PowerData} from '../utils/echarts'
    import {onMounted, ref} from 'vue'
    // import {FullScreen} from '@element-plus/icons-vue'
    import type { ResultData } from '@/utils/sse';
    const chartContainer = ref<HTMLDivElement>()
    const dialogLargeChart = ref(false)
    const largeChartContainer = ref<HTMLDivElement>()
    const props = defineProps<{
        data:ResultData
    }>()
    onMounted(()=>{
        insertLineChart(chartContainer.value as HTMLDivElement, props.data)
        
    })
    // const showLargeChart = ()=>{
    //         dialogLargeChart.value = true
    //         insertLineChart(largeChartContainer.value as HTMLDivElement, props.data.result.data as PowerData[])
    // }
   
    
</script>

<style>
.chart-card{
    width: fit-content;
    margin: 5px;
}

.chart-container{
    width:60vw;
    height:300px;
}
/* .large-chart-container{
    width:1500px;
    height: 75vh;
} */
</style>