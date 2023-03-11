import type LogicFlow from "@logicflow/core";
import icons from './icons'
import "@logicflow/extension/lib/style/index.css";

export default function setPanel(lf:LogicFlow){
    
    lf.extension.dndPanel.setPatternItems([
        // {
        //   label: 'Select area',
        //   icon: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAAH6ji2bAAAABGdBTUEAALGPC/xhBQAAAOVJREFUOBGtVMENwzAIjKP++2026ETdpv10iy7WFbqFyyW6GBywLCv5gI+Dw2Bluj1znuSjhb99Gkn6QILDY2imo60p8nsnc9bEo3+QJ+AKHfMdZHnl78wyTnyHZD53Zzx73MRSgYvnqgCUHj6gwdck7Zsp1VOrz0Uz8NbKunzAW+Gu4fYW28bUYutYlzSa7B84Fh7d1kjLwhcSdYAYrdkMQVpsBr5XgDGuXwQfQr0y9zwLda+DUYXLaGKdd2ZTtvbolaO87pdo24hP7ov16N0zArH1ur3iwJpXxm+v7oAJNR4JEP8DoAuSFEkYH7cAAAAASUVORK5CYII=',
        //   callback: () => {
        //     lf.extension.selectionSelect.openSelectionSelect();
        //     lf.once('selection:selected', () => {
        //       lf.extension.selectionSelect.closeSelectionSelect();
        //     });
        //   }
        // },
        {
          type: 'node',
          text: '',
          label: 'Node',
          icon: icons.node.icon,
        },
        {
          type: 'pvmodule',
          text: 'PV Module',
          label: 'PV Module',
          icon: icons.pvmodule.icon,
          className: 'important-node'
        },
        
        {
          type: 'bss',
          text: 'BSS',
          label: 'BSS',
          icon: icons.bss.icon,
          className:'import_icon'
        },
        {
            type:'grid',
            text:'Grid',
            label:'Grid',
            icon:icons.grid.icon
        },
        {
            type:'cs',
            text:'Charging station',
            label:'Charging station',
            icon:icons.cs.icon
        }
      ]);
}