import { CircleNodeModel,CircleNode, BaseNodeModel, type AnchorConfig } from "@logicflow/core";
import params from './parameters/node'


class NodeModel extends CircleNodeModel {
  initNodeData(data: any) {
    super.initNodeData(data);
    this.text.draggable = true;
    this.r = 10
    this.properties = params
    const nodeNotAsTarget = {
      message: "Next node must be a node",
      validate: (sourceNode:BaseNodeModel|undefined, targetNode:BaseNodeModel|undefined, sourceAnchor:AnchorConfig|undefined, targetAnchor:AnchorConfig|undefined) => {
        return targetNode?.type != "node";
      },
    };
    this.sourceRules.push(nodeNotAsTarget);
    const nodeNotAsSource={
      message: 'Component only allows connecting nodes.',
      validate: (sourceNode:BaseNodeModel|undefined, targetNode:BaseNodeModel|undefined, sourceAnchor:AnchorConfig|undefined, targetAnchor:AnchorConfig|undefined) => {
        return sourceNode?.type != "node";
      },
    }
    this.targetRules.push(nodeNotAsSource)
  }
}
class NodeView extends CircleNode {
  
}

export default {
  type: "node",
  view: NodeView,
  model: NodeModel
};
