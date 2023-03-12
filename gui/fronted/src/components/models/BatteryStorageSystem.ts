import {getRectLabel} from '../canvas_components/common'
import icons from '../canvas_components/icons'
import params from './parameters/bss'
import {BaseElementModel,BaseElementView} from "./base_model/BaseElement";

class BatteryStorageSystemView extends BaseElementView {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.bss.svgPath
    return getRectLabel(model,svgPath)
  }
}

class BatteryStorageSystemModel extends BaseElementModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.properties = params
        
    }
}

export default {
  type: "bss",
  view: BatteryStorageSystemView,
  model: BatteryStorageSystemModel
};
