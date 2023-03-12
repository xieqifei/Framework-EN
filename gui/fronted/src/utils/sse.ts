export interface ResultData{
    type:string,
    name:string,
    id:string,
    result:{
        type:string,
        data:{
            [key: string]: any;
          },
        title?:string
    }
}

export class SSE{
    es:EventSource
    
    constructor(){
        this.es = new EventSource('/stream');
        this.es.addEventListener('end',function(e:MessageEvent){
        //    this.close()
        })
    }

    listenResult (callback: (arg0: any) => void){
        this.es.addEventListener('result',function(e:MessageEvent){
            const data:ResultData  = JSON.parse(e.data)
            callback(data)
        })
    }
    listenMessage (callback: (arg0: any) => void){
        this.es.addEventListener('message',function(e:MessageEvent){
            const data  = JSON.parse(e.data)
            callback(data)
        })
    }
    
    listenError(callback: (arg0: any) => void){
        this.es.addEventListener('error',function(e:MessageEvent){
            const data  = JSON.parse(e.data)
            callback(data)
        })
    }
    
    listenSuccess (callback: (arg0: any) => void){
        this.es.addEventListener('success',function(e:MessageEvent){
            const data  = JSON.parse(e.data)
            callback(data)
        })
    }
    close(){
        this.es.close()
    }
}

