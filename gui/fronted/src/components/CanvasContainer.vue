<style>
    #container { 
        height: 90vh;
        width: 100%;
        padding-top: 2px;
        /* background-color: rgba(0, 128, 0, 0.12); */
    }
    .btn-solve{
        position: absolute;
        top: 2px;
        right: 2px;
    }
</style>

<template>
    <div id="container" ref="container">
        <el-button type="primary" class="btn-solve" @click="solveModel">Solve</el-button>
    </div>
    <ParametersDrawer v-model="paramDrawerActive" :model="nodeCompute" :edges="edgeModels" @updateProperties="updateProperties" @onDrawerChange="onDrawerChange"/>
    <!-- <DrawerTest/> -->
</template>

<script setup lang="ts">
import LogicFlow, { type BaseNodeModel } from '@logicflow/core';
import {  DndPanel,Menu, SelectionSelect} from '@logicflow/extension';
import "@logicflow/core/dist/style/index.css";
import '@logicflow/extension/lib/style/index.css'
import { ref,onMounted, computed ,provide} from 'vue';
import type { Ref } from 'vue';
import setMenu from './cavas_components/menu'
import setPanel from './cavas_components/panel'
import renderGraph from './cavas_components/render'
import registerModels from './cavas_components/model_register'
import getSolution from "../api/solve"
import ParametersDrawer from './ParametersDrawer.vue';

const container:Ref<HTMLElement | null> = ref(null)
const outLF:Ref<LogicFlow | null> = ref(null)
const paramDrawerActive:Ref<boolean> = ref(false)
const nodeModel = ref<BaseNodeModel|undefined>()
const edgeModels = ref<(BaseNodeModel | null)[]>([])


const onDrawerChange = (value:boolean)=>{
    paramDrawerActive.value=value
}

const nodeCompute = computed(() => nodeModel.value);    

onMounted(()=>{
    const lf = new LogicFlow({
      container: container.value as HTMLElement,
      grid: true,
      plugins: [DndPanel, SelectionSelect,Menu],
      keyboard: {
        enabled: true
        },
      stopMoveGraph: true,
      edgeType:'mypolyline'
    });
    registerModels(lf)
    setMenu(lf)
    setPanel(lf)
    renderGraph(lf)
    lf.setTheme({ 
        arrow: {
            offset: 0, // 箭头垂线长度
            verticalLength: 0, // 箭头底线长度
        }
    })
    outLF.value = lf

    // click node ,show parameters editor side drawer
    lf.on('node:click', (model:BaseNodeModel) => {
        paramDrawerActive.value = true
        nodeModel.value = model.data

        //get the model connected nodes
        const edgeModelsTemp = lf.getNodeEdges(model.data.id)
        edgeModels.value = []
        edgeModelsTemp.forEach((edge)=>{
            if(edge.sourceNodeId.indexOf(model.data.id) !== -1){
                edgeModels.value?.push(lf.getNodeModelById(edge.targetNodeId))
            }else{
                edgeModels.value?.push(lf.getNodeModelById(edge.sourceNodeId))
            }
        })
    })
});

const solveModel = (e:Event)=>{
        const graphData = outLF.value?.getGraphData()
        console.log(graphData)
        getSolution(graphData)
    }

const updateProperties = (model:BaseNodeModel)=>{
    outLF.value?.setProperties(model.id,model.properties)
}

</script>