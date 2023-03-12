import {getRectLabel} from '../canvas_components/common'
import icons from '../canvas_components/icons'
import params from './parameters/pvmodule'
import {BaseElementModel,BaseElementView} from "./base_model/BaseElement";

class PVModuleView extends BaseElementView {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.pvmodule.svgPath
    return getRectLabel(model,svgPath)
  }
}

class PVModuleModel extends BaseElementModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.properties = params
    }
}

export default {
  type: "pvmodule",
  view: PVModuleView,
  model: PVModuleModel
};
