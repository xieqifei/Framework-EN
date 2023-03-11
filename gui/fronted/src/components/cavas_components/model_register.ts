import type LogicFlow from "@logicflow/core";
import BatteryStorageSystem from '../models/BatteryStorageSystem';
import Grid from '../models/Grid';
import PVModule from '../models/PVModule';
import Node from '../models/Node';
import ChargingStation from "../models/ChargingStation";
import MyPolylineEdge from "../models/MyPolylineEdge";

export default (lf:LogicFlow)=>{
    lf.batchRegister([
        BatteryStorageSystem,
        Grid,
        PVModule,
        Node,
        ChargingStation,
        MyPolylineEdge
    ]);}

