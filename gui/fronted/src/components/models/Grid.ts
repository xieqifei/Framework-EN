import { RectNode, RectNodeModel, h } from "@logicflow/core";
import {getRectLabel,fontSize,viewColor,fontColor} from '../cavas_components/common'
import icons from '../cavas_components/icons'
import params from './parameters/grid'
class GridView extends RectNode {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.grid.svgPath
    return getRectLabel(model,svgPath)
  }
}

class GridModel extends RectNodeModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.text.draggable = true; 
        this.text.editable = true;  
        this.text.y =  this.text.y+this.height*4/5
        this.text.x = this.text.x;
        this.properties = params
    }

  setAttributes() {
    const size = this.properties.scale || 1;
    this.width = 90 * size;
    this.height = 80 * size;
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

export default {
  type: "grid",
  view: GridView,
  model: GridModel
};
