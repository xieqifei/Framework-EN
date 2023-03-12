import {getRectLabel} from '../canvas_components/common'
import icons from '../canvas_components/icons'
import params from './parameters/company'
import {BaseElementModel,BaseElementView} from "./base_model/BaseElement";

class CompanyView extends BaseElementView {

  getShape() {
    const { model } = this.props;
    const svgPath = icons.company.svgPath
    return getRectLabel(model,svgPath)
  }
}

class CompanyModel extends BaseElementModel {
    initNodeData(data: any) {
        super.initNodeData(data)
        this.properties = params

    }
}

export default {
  type: "company",
  view: CompanyView,
  model: CompanyModel
};
