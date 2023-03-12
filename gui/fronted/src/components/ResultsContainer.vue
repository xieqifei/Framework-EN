<template>
    <el-container>

        <el-main>
            <el-tabs type="border-card" class="demo-tabs">

                <el-tab-pane label="Figures"> 
                    <el-scrollbar height="75vh">
                        <el-skeleton style=" width:60vw;height:250px;" :loading="!resultDataStorage.length" animated>
                            <template #template>
                                <el-skeleton-item variant="image" style="width:60vw;height:250px;" />
                            </template>
                        </el-skeleton>
                        <div v-for="resultData in resultDataStorage">
                            <ChartCard :data="resultData" />
                        </div>
                        <div class="floating-window" v-if="resultDataStorage.length">
                            <div v-for="resultData in resultDataStorage">
                                <a :href="'#' + resultData.name + ':' + resultData.result?.title">{{ resultData.name }}:{{
                                    resultData.result?.title }}</a>
                            </div>
                        </div>
                    </el-scrollbar>
                </el-tab-pane>
                <el-tab-pane label="Data">
                    <el-table :data="tableData" style="width: 100%" stripe>
                        <el-table-column prop="name" label="Name" width="180" />
                        <el-table-column prop="variable" label="Variable" />
                        <el-table-column prop="value" label="Value" width="180" />
                </el-table>
                </el-tab-pane>
            </el-tabs>

        </el-main>
    </el-container>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue';
import ChartCard from './ChartCard.vue'
import { SSE, type ResultData } from '../utils/sse'
import { ElNotification } from "element-plus";
import {beautyLabelName} from '../utils/echarts'
const resultDataStorage = ref<ResultData[]>([])
interface TableData{
    name:string,
    variable:string
    value:number
}
const tableData = ref<TableData[]>([])
const se = new SSE()
se.listenMessage((data: { msg: string }) => {
    //clear Result container
    if (data.msg.startsWith('Simulation got started')) {
        resultDataStorage.value.length = 0
        tableData.value.length = 0
    }
    //send notification
    ElNotification({
        title: 'Message',
        message: data.msg,
        type: 'info',
        showClose: false,
    })
})
se.listenError((data: { msg: string }) => {
    //send error notification
    ElNotification({
        title: 'Error',
        message: data.msg,
        type: 'error',
        showClose: false,
    })
})
se.listenSuccess((data: { msg: string }) => {
    //send success notification
    ElNotification({
        title: 'Success',
        message: data.msg,
        type: 'success',
        showClose: false,
    })
})
se.listenResult((data: ResultData) => {
    if (data.result.type == 'data') {
        console.log(data)
        resultDataStorage.value.push(data)
    } else if(data.result.type == 'variables'){
        for(let key in data.result.data) {
            let name = data.name
            let variable = beautyLabelName(key);
            let value = data.result.data[key].toFixed(3)
            tableData.value.push({
                name,
                variable,
                value
        })
        }
        
    }
})
function test() {
    fetch('src/components/temp.json')
        .then(response => response.json())
        .then(data => {
            const testData: ResultData = {
                name: 'Name',
                id: 'ID',
                type: 'data',
                result: {
                    type: 'data',
                    title: 'Title',
                    data: data
                }
            }
            for (let i = 1; i < 6; i++) {
                setTimeout(() => {
                    resultDataStorage.value.push({
                        name: 'Name' + i,
                        id: 'ID',
                        type: 'data',
                        result: {
                            type: 'data',
                            title: 'Title',
                            data: data
                        }
                    })
                }, i * 3000)
            }

        }).catch(error => console.error(error));
}
// test()
</script>

<style scoped>
#element-result-figure-container {
    position: relative;
    width: 1000px;
    height: 50vh;
    overflow: hidden;
}

.scrollbar-flex-content {
    display: flex;
}

.floating-window {
    position: fixed;
    top: 50%;
    right: 0;
    transform: translateY(-50%);
    width: auto;
    height: auto;
    background-color: #f5f5f5;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
}

.floating-window a {
    display: block;
    font-size: 16px;
    color: #333;
    text-align: center;
    margin-bottom: 10px;
}

.scrollbar-demo-item {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 50px;
    margin: 10px;
    text-align: center;
    border-radius: 4px;
    background: var(--el-color-danger-light-9);
    color: var(--el-color-danger);
}
</style>