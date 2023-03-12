import { BaseNodeModel, h, RectNodeModel } from "@logicflow/core";

const fontSize = 18
const fontColor = "rgb(24, 125, 255)"
const viewColor = "rgb(24, 125, 255)"

const getRectLabel = (model:BaseNodeModel,svgPath:string)=>{
    const { x, y, width, height, radius,} = model;
    const style = model.getNodeStyle();
    return h("g", {}, [
        h("rect", {
          ...style,
          x: x - width / 2,
          y: y - height / 2,
          rx: radius,
          ry: radius,
          width,
          height
        }),
        h("svg",
            {
              x: x - width / 2 + 5,
              y: y - height / 2 + 5,
              width: width,
              height: height,
              viewBox: "0 0 1274 1024"
            },
            [
              h("path", {
                fill: style.stroke,
                d: svgPath
              }),
            ]
          )
      ]);
}

const getRequiredNodeNumber= (model:BaseNodeModel)=>{
  let count = 0
  for(let key in model.properties){
    if(key.startsWith('node_')){
      count++
    }
  }
  return count
}

const getElementConnectedNodes = (model:BaseNodeModel)=>{
  let nodes: BaseNodeModel[] = []
  nodes = nodes.concat(model.outgoing.nodes,model.incoming.nodes)
  // console.log(nodes)
  return nodes
}

const getConnectedNodeNumber = (model:BaseNodeModel)=>{
  return model.incoming.nodes.length+model.outgoing.nodes.length
}


export{
    fontSize,
    fontColor,
    viewColor,
    getRequiredNodeNumber,
    getElementConnectedNodes,
    getConnectedNodeNumber,
    getRectLabel,
}