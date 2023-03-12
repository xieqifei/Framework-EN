import { h, PolylineEdge, PolylineEdgeModel } from "@logicflow/core";
class MyPolylineEdgeModel extends PolylineEdgeModel {
    
  
}

class MyPolylineEdge extends PolylineEdge {

    getEndArrow() {
        const { model, graphModel } = this.props;
        const { id, properties: { arrowType } } = model;
        const { stroke, strokeWidth } = this.getArrowStyle();
        const pathAttr = {
          stroke,
          strokeWidth
        }
        return h('path', {
            ...pathAttr,
            fill: '#FFF',
            d: ''
          })
    }
}

export default {
  type: "mypolyline",
  model: MyPolylineEdgeModel,
  view: MyPolylineEdge
};
