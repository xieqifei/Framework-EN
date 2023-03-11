import { ElNotification } from "element-plus";
import { h } from "vue";

const es = new EventSource('/stream');
const addNodeResultFigure = (data: { result: { src: string; }; })=>{
    var nodeResultContainer = document.getElementById("node-result-container");
    var child = document.createElement("div");

    child.innerHTML = `<img
      src="${data.result.src}" style="height:300px"
    />`;
    nodeResultContainer?.appendChild(child)
}

const addElementResult = (data: { result: { type: string; src: any; }; name: any; })=>{
    if(data.result.type == 'img'){
        var child = document.createElement("div");
        child.innerHTML=`
        <div>
        ${data.name}
        </div>
        <img
          src='${data.result.src}' style="height:300px"
        />
        `
        var elementResultImageContainer = document.getElementById("element-result-figure-container");
        elementResultImageContainer?.appendChild(child)
    }

}

const startSSE = ()=>{
    
    es.addEventListener('message', function(e) {
        const data = JSON.parse(e.data);
        ElNotification({
            title: 'Message',
            message: data.msg,
            type: 'info',
          })
    });

    
    es.addEventListener('result',function(e:MessageEvent){
        const data  = JSON.parse(e.data)
        if(data.type=='node'){
            addNodeResultFigure(data)
        }else{
            addElementResult(data)
        }
    })
    
    es.addEventListener('error',function(e:MessageEvent){
        const data = JSON.parse(e.data);
        ElNotification({
            title: 'Error',
            message:data.msg,
            type: 'error',
          })
    })
    
}

const closeSSE = ()=>{
    es.close()
}


export {
    startSSE,
    closeSSE
}