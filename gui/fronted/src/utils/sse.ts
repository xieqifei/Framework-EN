import { ElNotification } from "element-plus";

const es = new EventSource('/stream');
interface ResultData{
    type:string,
    name:string,
    id:string,
    result:{
        type:string,
        data:string|{},
        title:string
    }
}

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

const listenResult = (callback: (arg0: any) => void)=>{
    es.addEventListener('result',function(e:MessageEvent){
        const data:ResultData  = JSON.parse(e.data)
        callback(data)
    })
}

const listenMessage = (callback: (arg0: any) => void)=>{
    es.addEventListener('message',function(e:MessageEvent){
        const data  = JSON.parse(e.data)
        callback(data)
    })
}

const listenError = (callback: (arg0: any) => void)=>{
    es.addEventListener('error',function(e:MessageEvent){
        const data  = JSON.parse(e.data)
        callback(data)
    })
}

const listenSuccess = (callback: (arg0: any) => void)=>{
    es.addEventListener('success',function(e:MessageEvent){
        const data  = JSON.parse(e.data)
        callback(data)
    })
}

const startSSE = ()=>{
    
    es.addEventListener('message', function(e) {
        const data = JSON.parse(e.data);
        ElNotification({
            title: 'Message',
            message: data.msg,
            type: 'info',
            showClose: false,
          })
    });

    
    // es.addEventListener('result',function(e:MessageEvent){
    //     const data  = JSON.parse(e.data)
    //     if(data.type=='node'){
    //         addNodeResultFigure(data)
    //     }else{
    //         addElementResult(data)
    //     }
    // })
    
    es.addEventListener('error',function(e:MessageEvent){
        const data = JSON.parse(e.data);
        ElNotification({
            title: 'Error',
            message: data.msg,
            type: 'error',
            showClose: false,
          })
    })

    es.addEventListener('success',function(e:MessageEvent){
        const data = JSON.parse(e.data);
        ElNotification({
            title: 'Success',
            message: data.msg,
            type: 'success',
            showClose: false,
          })
    })
}

const closeSSE = ()=>{
    es.close()
}

export {
    startSSE,
    closeSSE,
    listenResult,
    listenMessage,
    listenError,
    listenSuccess,
};
export type { ResultData };
