import {getRectLabel} from '../canvas_components/common'
import icons from '../canvas_components/icons'
import params from './parameters/pcs'
import {BaseElementModel,BaseElementView} from "./base_model/BaseElement";

class PowerConversionSystemView extends BaseElementView {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.pcs.svgPath
    return getRectLabel(model,svgPath)
  }
}

class PowerConversionSystemModel extends BaseElementModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.properties = params
    }
}

export default {
  type: "pcs",
  view: PowerConversionSystemView,
  model: PowerConversionSystemModel
};
