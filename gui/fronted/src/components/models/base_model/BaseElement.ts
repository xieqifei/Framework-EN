import { RectNode, RectNodeModel, h, BaseNodeModel, type AnchorConfig, GraphModel } from "@logicflow/core";
import {fontSize,viewColor,fontColor} from '../../canvas_components/common'
import {getRequiredNodeNumber,getConnectedNodeNumber} from '../../canvas_components/common'
export class BaseElementView extends RectNode {
  
}

export class BaseElementModel extends RectNodeModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.text.draggable = true; 
        this.text.editable = true;  
        this.text.y =  this.text.y+this.height*4/5;
        const nodeAsOnlyTarget = {
          message: "Next node must be a node",
          validate: (sourceNode:BaseNodeModel|undefined, targetNode:BaseNodeModel|undefined, sourceAnchor:AnchorConfig|undefined, targetAnchor:AnchorConfig|undefined) => {
            return targetNode?.type === "node";
          },
        };
        const sNodeCapacityValidation = {
          message: "Node capacity is full.",
          validate: (sourceNode:BaseNodeModel|undefined, targetNode:BaseNodeModel|undefined, sourceAnchor:AnchorConfig|undefined, targetAnchor:AnchorConfig|undefined) => {
            const requiredNodeNumber = getRequiredNodeNumber(sourceNode as BaseNodeModel)
            const connectedNodeNumber = getConnectedNodeNumber(sourceNode as BaseNodeModel)
            return requiredNodeNumber>connectedNodeNumber;
          },
        };
        this.sourceRules.push(nodeAsOnlyTarget,sNodeCapacityValidation);
        const elementNotAsTargetOfElement={
          message: 'Component only allows connecting nodes.',
          validate: (sourceNode:BaseNodeModel|undefined, targetNode:BaseNodeModel|undefined, sourceAnchor:AnchorConfig|undefined, targetAnchor:AnchorConfig|undefined) => {
            return sourceNode?.type === "node" ;
          },
        }
        const tNodeCapacityValidation={
          message: 'Node capacity is full.',
          validate: (sourceNode:BaseNodeModel|undefined, targetNode:BaseNodeModel|undefined, sourceAnchor:AnchorConfig|undefined, targetAnchor:AnchorConfig|undefined) => {
            const requiredNodeNumber = getRequiredNodeNumber(targetNode as BaseNodeModel)
            const connectedNodeNumber = getConnectedNodeNumber(targetNode as BaseNodeModel)
            return requiredNodeNumber>connectedNodeNumber;
          },
        }
        this.targetRules.push(elementNotAsTargetOfElement,tNodeCapacityValidation)
    }

  setAttributes() {
    const size = this.properties.scale || 1;
    this.width = 70 * size;
    this.height = 70 * size;
  }

  getTextStyle() {
    const style = super.getTextStyle();
    style.fontSize = fontSize;
    const properties = this.properties;
    style.color = properties.disabled ? "red" : fontColor;
    return style;
  }

  getNodeStyle() {
    const style = super.getNodeStyle();
    const properties = this.properties;
    if (properties.disabled) {
      style.stroke = "red";
    } else {
      style.stroke = viewColor;
    }
    return style;
  }

}
