import type LogicFlow from "@logicflow/core";

export default (lf:LogicFlow)=>{
    lf.extension.menu.setMenuConfig({
        nodeMenu: [
          {
            text: 'Delete',
            callback(node: { id: string; }) {
              lf.deleteNode(node.id);
            },
          },
          {
            text: 'Copy',
            callback(node: { id: string; }) {
              lf.cloneNode(node.id);
            },
    
          },
          {
            text: 'Edit Text',
            callback(node: { id: string; }) {
              lf.editText(node.id);
            },
    
          },
        ], // 覆盖默认的节点右键菜单
        edgeMenu: [
          {
            text: 'Delete',
            callback(edge: { id: string; }) {
              lf.deleteEdge(edge.id);
            },
          },
          {
            text: 'Edit Text',
            callback(edge: { id: string; }) {
              lf.editText(edge.id);
            },
    
          },
        ], // 删除默认的边右键菜单
        graphMenu: [],  // 覆盖默认的边右键菜单，与false表现一样
      });
}

export {}