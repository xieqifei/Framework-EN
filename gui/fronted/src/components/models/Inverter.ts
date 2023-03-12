import {getRectLabel} from '../canvas_components/common'
import icons from '../canvas_components/icons'
import params from './parameters/inverter'
import {BaseElementModel,BaseElementView} from "./base_model/BaseElement";


class InverterView extends BaseElementView {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.inverter.svgPath
    return getRectLabel(model,svgPath)
  }
}

class InverterModel extends BaseElementModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.properties = params
    }
}

export default {
  type: "inverter",
  view: InverterView,
  model: InverterModel
};
