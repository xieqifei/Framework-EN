import { CircleNodeModel,CircleNode } from "@logicflow/core";
import params from './parameters/node'


class NodeModel extends CircleNodeModel {
  initNodeData(data: any) {
    super.initNodeData(data);
    // this.style.fill = 'black'
    this.text.draggable = true;
    this.r = 15
    this.properties = params
  }
  // getDefaultAnchor() {
  //   const { width, height, x, y, id } = this;
  //   let anchorPoint = []
  //   for(let segment=100;segment<=height-100;segment+=100){
  //     anchorPoint.push({
  //       x:x-width/2,
  //       y:y-height/2+segment,
  //       this:'left',
  //       id:`${id}_+${segment}`
  //     })
  //     anchorPoint.push({
  //       x:x+width/2,
  //       y:y-height/2+segment,
  //       this:'right',
  //       id:`${id}_-${segment}`
  //     })
  //   }
  //   return anchorPoint
  // }
}
class NodeView extends CircleNode {
  
}

export default {
  type: "node",
  view: NodeView,
  model: NodeModel
};
