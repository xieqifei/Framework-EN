import type LogicFlow from '@logicflow/core';

type ControlItem = {
  key: string;
  iconClass: string;
  title: string;
  text: string;
  onClick?: Function;
  onMouseEnter?: Function;
  onMouseLeave?: Function;
};

class Control {
  private lf: LogicFlow;
  static pluginName = 'control';
  private controlItems: ControlItem[] = [
    {
      key: 'zoom-out',
      iconClass: 'lf-control-zoomOut',
      title: 'Zoom-out',
      text: 'Zoom-out',
      onClick: () => {
        this.lf.zoom(false);
      },
    },
    {
      key: 'zoom-in',
      iconClass: 'lf-control-zoomIn',
      title: 'Zoom-in',
      text: 'Zoom-in',
      onClick: () => {
        this.lf.zoom(true);
      },
    },
    {
      key: 'reset',
      iconClass: 'lf-control-fit',
      title: 'Reset',
      text: 'Reset',
      onClick: () => {
        this.lf.resetZoom();
      },
    },
    {
      key: 'undo',
      iconClass: 'lf-control-undo',
      title: 'Undo',
      text: 'Undo',
      onClick: () => {
        this.lf.undo();
      },
    },
    // {
    //   key: 'redo',
    //   iconClass: 'lf-control-redo',
    //   title: 'Redo',
    //   text: 'Redo',
    //   onClick: () => {
    //     this.lf.redo();
    //   },
    // },
    {
        key: 'clear',
        iconClass: 'lf-control-clear',
        title: 'Clear',
        text: 'Clear',
        onClick: () => {
          this.lf.render({});
        },
      }
  ];
  private domContainer: HTMLElement | undefined;
  private toolEl: HTMLElement | undefined;
  constructor({ lf }: { lf: LogicFlow }) {
    this.lf = lf;
  }
  render(lf: any, domContainer: HTMLElement | undefined) {
    this.destroy();
    const toolEl = this.getControlTool();
    this.toolEl = toolEl;
    domContainer?.appendChild(toolEl);
    this.domContainer = domContainer;
  }
  destroy() {
    if (this.domContainer && this.toolEl && this.domContainer.contains(this.toolEl)) {
      this.domContainer.removeChild(this.toolEl);
    }
  }
  addItem(item: ControlItem) {
    this.controlItems.push(item);
  }
  removeItem(key: string) {
    const index = this.controlItems.findIndex((item) => item.key === key);
    return this.controlItems.splice(index, 1)[0];
  }

  private getControlTool(): HTMLElement {
    const NORMAL = 'lf-control-item';
    const DISABLED = 'lf-control-item disabled';
    const controlTool = document.createElement('div');
    const controlElements: HTMLDivElement[] = [];
    controlTool.className = 'lf-control';
    this.controlItems.forEach((item) => {
      const itemContainer = document.createElement('div');
      const icon = document.createElement('i');
      const text = document.createElement('span');
      itemContainer.className = DISABLED;
      item.onClick && (itemContainer.onclick = item.onClick.bind(null, this.lf));
      item.onMouseEnter && (itemContainer.onmouseenter = item.onMouseEnter.bind(null, this.lf));
      item.onMouseLeave && (itemContainer.onmouseleave = item.onMouseLeave.bind(null, this.lf));
      icon.className = item.iconClass;
      text.className = 'lf-control-text';
      text.title = item.title;
      text.innerText = item.text;
      itemContainer.append(icon, text);
      switch (item.text) {
        case 'Undo':
          this.lf.on('history:change', ({ data: { undoAble } }) => {
            itemContainer.className = undoAble ? NORMAL : DISABLED;
          });
          break;
        case 'Redo':
          this.lf.on('history:change', ({ data: { redoAble } }) => {
            itemContainer.className = redoAble ? NORMAL : DISABLED;
          });
          break;
        default:
          itemContainer.className = NORMAL;
          break;
      }
      controlElements.push(itemContainer);
    });
    controlTool.append(...controlElements);
    return controlTool;
  }
}

export default Control;

export { Control };