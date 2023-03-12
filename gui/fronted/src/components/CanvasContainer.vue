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
    .lf-control-simulate {
        background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAABEhJREFUWEfFl11oHFUUx///yYcBq/igD1rFWmKT3XtvNLYirSh+gVg/nmylSB8ECfigEvxAsbUpDWih1GKhEAJSigh2/VYqgmCpIKLG4M6dRDHWoiFF+xDQl0iye+SEmTBuZ3ZnW8ULy7I759z7u+ece+5/iDaGc26LiNwMYC3JtfoNYF5ETgI4JSKzJD/x3h8vOi1bGRpjyiS3knxQREwr+/j5cRGpdHd3VyYnJ88082kKYK19DMChjAmOkzwtInMALgQwEH9WNdj+BOAZ7/27eRC5AMaYMZJDKcffALwTBMGharXqsyYsl8s3BUFwD4D7AdyQstntvR/J8skEsNZKyviYLlwqlQ5XKpVakRQYY7pJPgHgSQBXxj4V7/3WRv+zAKy138XhVNtc8iIgAwMDfbVabZzkLXkQ/wCw1h4BsD02Pq/F04DWWg3/riyIFQDn3JCIjKmRiHweRdGtRXZZ1KYBYmVzKwDW2m8ArCc5R/KOarX6Q97kxpjeKIpmii6e2FlrP9AC1TWWlpY2TE9Pn14GSO++Vd6ttUcBbAHwtYjsjaLo7aIg1tr7AHyYTvEyQHr3CVnWpMaY/SSHG56NBUEwWq1WZ4uApKNAch2dcxtF5IvY+aD3Xo9P5rDWfgbgNgDaavU7GSdJ7gnD8HArCOfcIyLymtoFQbBRAYZFZL/+QXJzGIYfFwEgeUBEdgDYkNiTfENERr3303lzDA4OXra4uPh7XOxDNMYcI6ndC977Vq15JQLe+9uNMatIvqjtNrWg9n6FeLXARg4y6XpamWEYrm4WwnQKFCCxNcbcHYNsSvmPeO93Z83nnNNIbdNUKsA8gEsATHjvV8KZ5ZgHENsGxpgRkjvj37Pe+6ty5tkH4KllAGPMzyTX/EsAu+JIaDM7FUXRNS0BrLWTAK4/nxQ45+4SEW23KlaSkdvKG1OQFNY5FSGAF0g+d45F+J6m4FmSe9s9hiLyCkk9hje2cwz7+vou6urq+iM+hsP/RyNSXantXOtkMGnF2kZXpy+JnOI5EIuM9ON2W/E4gEcBfO+9LyUAqvtU/+nILR4VqEEQHI3F6YSIvNTOZVQul+8MguDTON3Ph2H4cgJQAvAlgItbXcdxDte3I72TcDnn3heRBwB8u7CwsGlmZuavtB4Y1YqOc/NfC5Lt3vvXlyORTqYx5kRKv+W20mbtOqd2WkuyVF8/Q/LS+PeRer2+c2pq6pd2F03sUwJG/zpLGefJ8h8B9MbFMici47VabUwlVFEQa+1DscC9N/YpJstT5HqdPp5qMnP1ev0jreIwDCtZIP39/Ws6OztVrqn+T19suUKn6f3vnNsjIk8D6MlYUI/hBMk/SV4hIpc3qCR1UeG6w3v/Zl7kWr6clkqlazs6Oh4muU1E1hVMgS6sb1T7vPe/NvNpCZA49/b2XtDT07MZwHWpl9Gr49dz1RTzJL8i+VYYhicKguJvYCImc0smwi4AAAAASUVORK5CYII=');
    }
    .lf-control-clear{
        background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAA6xJREFUWEfFll2IVkUYx//PaxuCW0FfSFm9ENW288xhdS0wsKKgvKiuVAwskA1T2VQUMUFqNYq+SPrCCpLKitRuakUIDb+gK6OLeWbZCy8WrEvvQjZ29zwxL+97mD179n3P2RV27mbmP8//d56ZeeYQFrjRAvvjugAYY54lokRVrwA46b3/t+yHzRuAmYcAvBkZ/pGm6eDIyMhfZSDmBWCt3auq7xYYhUwMiMjpThBzBmDm7QA+zhlMArihOXZNVQe89z+1g5gTgLV2s6p+GQdW1ReJ6D8A3wK4qTVHRK855z6bDaIyADO/BOC7XMCXReRoGDPGrCGiAHFnpBkSkQNFEJUAkiRZm6bpiVygV0Tk63jMWvuEqgaI+6JMHHLO7cpDlAZg5ucADOcCbBWRL4q+jJlXAvgewEPR/BERGYj1pQCSJHk6TdMzOaMdIvJJuwPGzA8D+BFAX5SJn51z67J+p2vCzI8BuABgURRkt3Puo05rw3xvb++9tVot3IRVkf60iDwT+m0zkCTJiqmpqbNEdHNrsaq+7r1/r4x5S9PT03NbV1fXcVV9Klp3QESGZgUI6VPVM0R0V7Rov4i8XcW8pa3X64u7u7uPA3i+Ofa3iNxTCNDX11efmJj4jYgezBPPxby1hpnXAzjWFsAYsxTAKSJaXmDWSNtcIJh5I4BGrQhNVb/y3r86LQP9/f23jI+PDxPR6shkFEDPfDJhrd2kqkeiGOnk5OT9o6OjYxmAMeZGAL8Q0ZpI+AERHVXVcP+zogKgdCYKyvY1EVky4xoaY04Q0drI/LCIbAt9Y8yjRHQSwB1VMmGtHVTVT6M1V0Xk9ngLGxlIkmRZmqbhCW3tzzfe+02xkJmfbFbC7jIQxpidRHQo0v4jIsvy56cBwMxbABxuTh4TkQ1FB60J8TuAWjsIZt4D4P1Ic1lEHiiK2crA6jRNQ7VrNCLa6Jz7oQ3E2dxcdiaYeR+Ad6J5ERFbFKvh1Zpg5nDa44djxisXacN2zIAgoilVPRiZXRKRR2YznwZgrV2nqqFSZU1VB733n1fIRCYloovOucfbmU8DCJ0iCAB7ROTDihDZY1MJIIiLnl4iesM591Y+WPMfYXNU34NkWERe6GScnbcioTGml4h8bjvGiGgsGrsbQP5knythfD4u57O+hsaYW4noaomAlSVEtN451/i16/hHxMy/5lJc2TC/gIhWOuf+LAUQRMaYDbVara6qi+ftDpwTkWyrOmbgOhi2DbHgAP8D9+1sMIYTm2wAAAAASUVORK5CYII=');
    }
</style>

<template>
    <div id="container" ref="container">
        <!-- <el-button type="primary" class="btn-solve" @click="solveModel">Solve</el-button> -->
    </div>
    <ParametersDrawer v-model="paramDrawerActive" :elem="nodeCompute" :nodes="nodeModels" @updateProperties="updateProperties" />
    <!-- <DrawerTest/> -->
</template>

<script setup lang="ts">
import LogicFlow, { type BaseNodeModel, type GraphConfigData } from '@logicflow/core';
import { DndPanel,Menu, SelectionSelect} from '@logicflow/extension';
import "@logicflow/core/dist/style/index.css";
import '@logicflow/extension/lib/style/index.css'
import { ref,onMounted, computed } from 'vue';
import type { Ref } from 'vue';
import setMenu from './canvas_components/menu'
import setPanel from './canvas_components/panel'
import renderGraph from './canvas_components/render'
import registerModels from './canvas_components/model_register'
import getSolution from "../utils/solve"
import ParametersDrawer from './ParametersDrawer.vue';
import Control from './canvas_components/control'
// import {getElementConnectedNodes} from './canvas_components/common'

const container:Ref<HTMLElement | null> = ref(null)
const outLF:Ref<LogicFlow | null> = ref(null)
const paramDrawerActive:Ref<boolean> = ref(false)
const elemModel = ref<BaseNodeModel|undefined>()
const nodeModels = ref<(BaseNodeModel | null)[]>([])

// const onDrawerChange = (value:boolean)=>{
//     paramDrawerActive.value=value
// }

const nodeCompute = computed(() => elemModel.value);    

onMounted(()=>{
    const lf = new LogicFlow({
      container: container.value as HTMLElement,
      grid: true,
      plugins: [DndPanel, SelectionSelect,Menu,Control],
      keyboard: {
        enabled: true
        },
      stopMoveGraph: true,
      edgeType:'mypolyline'
    });

    lf.extension.control.addItem(
        {
        key: 'simulate',
        title: "",
        iconClass: 'lf-control-simulate',
        text: "Simulate",
        onClick: () => {
            solveModel()
        }
        }
    )
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

    const getElementConnectedNodes = (elem:BaseNodeModel)=>{
        const edgeModelsTemp = lf.getNodeEdges(elem.id)
        let nodeModelsTemp: BaseNodeModel[] = []
        edgeModelsTemp.forEach((edge)=>{
            if(edge.sourceNodeId.indexOf(elem.id) !== -1){
                nodeModelsTemp.push(lf.getNodeModelById(edge.targetNodeId))
            }else{
                nodeModelsTemp.push(lf.getNodeModelById(edge.sourceNodeId))
            }
        })
        return nodeModelsTemp

    }

    // click node ,show parameters editor side drawer
    lf.on('node:click', (e) => {
        paramDrawerActive.value = true
        elemModel.value = e.data
        //get the model connected nodes
        nodeModels.value = [...getElementConnectedNodes(e.data)]
    })
    
    // if a element connected to a node, then edit property of element
    lf.on('anchor:drop',({data,e,nodeModel,edgeModel})=>{
        if(edgeModel.sourceNode.type != 'node'){
            setSingleNodeValue(edgeModel.sourceNode)
        }else{
            setSingleNodeValue(edgeModel.targetNode)
        }
    })

    // does this element connect to any one node?
    const isSingleNodeConnection = (elem:BaseNodeModel)=>{
      let count = 0
      for(let key in elem.properties){
        if(key.startsWith('node')){
          count++
        }
      }
      
      if(count==1){
        return true
      }else{
        return false
      }
    }

    //set the node value, if any one node need to be connect and is already connected to one node.
    const setSingleNodeValue=(elem:BaseNodeModel)=>{
        let elemConnectedNodes = getElementConnectedNodes(elem)
      if(isSingleNodeConnection(elem)){
        for(let key in elem.properties){
          if(key.startsWith('node')&&elem&&elemConnectedNodes.length==1){
            elem.properties[key].value = elemConnectedNodes[0].id
          }
        }
      }
    }
    const graphData:GraphConfigData  = lf.getGraphData()
    for(let key in graphData.nodes){
        const elem = graphData.nodes[key]
        if(elem.type!='node'){
            let elemModel = lf.getNodeModelById(elem.id as string)
            setSingleNodeValue(elemModel)
        }
    }

});

const solveModel = (e?:Event)=>{
        const graphData = outLF.value?.getGraphData()
        console.log(graphData)
        getSolution(graphData)
        //clear result container
        // var nodeResultContainer = document.getElementById("node-result-container");
        // var elementResultImageContainer = document.getElementById("element-result-figure-container");
        // nodeResultContainer!.innerHTML = ''
        // elementResultImageContainer!.innerHTML=''
    }

const updateProperties = (model:BaseNodeModel)=>{
    outLF.value?.setProperties(model.id,model.properties)
}

</script>