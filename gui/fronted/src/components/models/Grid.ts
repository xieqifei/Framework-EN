import {getRectLabel} from '../canvas_components/common'
import icons from '../canvas_components/icons'
import params from './parameters/grid'
import {BaseElementModel,BaseElementView} from "./base_model/BaseElement";


class GridView extends BaseElementView {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.grid.svgPath
    return getRectLabel(model,svgPath)
  }
}

class GridModel extends BaseElementModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.properties = params
    }
}

export default {
  type: "grid",
  view: GridView,
  model: GridModel
};
