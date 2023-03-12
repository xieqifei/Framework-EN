import {getRectLabel} from '../canvas_components/common'
import icons from '../canvas_components/icons'
import params from './parameters/chargingstation'
import {BaseElementModel,BaseElementView} from "./base_model/BaseElement";
class ChargingStationView extends BaseElementView {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.cs.svgPath
    return getRectLabel(model,svgPath)
  }
}

class ChargingStationModel extends BaseElementModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.properties = params

    }

  
}

export default {
  type: "cs",
  view: ChargingStationView,
  model: ChargingStationModel
};
