import type { GraphConfigData } from "@logicflow/core/types/type";
import axios from "axios";

const getSimulationResult = (graphData:GraphConfigData|unknown)=>{
    axios.post('/solve', graphData)
    .then(function (response) {
        console.log(response.data);
    })
    .catch(function (error) {
        console.log(error);
    });
}

export default function getSolution(graphData:GraphConfigData | unknown){
    getSimulationResult(graphData)
}