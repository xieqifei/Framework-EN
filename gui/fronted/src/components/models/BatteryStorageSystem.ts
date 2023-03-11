import { RectNode, RectNodeModel, h } from "@logicflow/core";
import {getRectLabel,fontSize,viewColor,fontColor} from '../cavas_components/common'
import icons from '../cavas_components/icons'
import params from './parameters/bss'
class BatteryStorageSystemView extends RectNode {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.bss.svgPath
    return getRectLabel(model,svgPath)
  }
}

class BatteryStorageSystemModel extends RectNodeModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.text.draggable = true; 
        this.text.editable = true;  
        this.text.y =  this.text.y+this.height*4/5;
        this.properties = params
    }

  setAttributes() {
    const size = this.properties.scale || 1;
    this.width = 100 * size;
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

export default {
  type: "bss",
  view: BatteryStorageSystemView,
  model: BatteryStorageSystemModel
};
