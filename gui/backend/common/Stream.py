import json

import datetime


class Stream:
    def __init__(self,announcer) -> None:
        self.now = datetime.datetime.now().time()
        self.announcer = announcer
        
    def format_sse(self,data: dict, event:str=None) -> str:
        msg = f'data: {json.dumps(data)}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
        return msg

    def pack_message(self,msg:str):
        data = {'msg':msg}
        return self.format_sse(data,'message')

    def pack_error(self,msg:str):
        data = {'msg':str(msg)}
        return self.format_sse(data,'error')

    def pack_result(self,data:dict):
        return self.format_sse(data,'result')

    def pack_success(self,msg:str):
        data = {'msg':msg}
        return self.format_sse(data,'success')

    def send_message(self,msg):
        # msg = f'{msg}'
        self.announcer.announce(self.pack_message(msg))
        
    def send_error(self,msg):
        # msg = f'{self.now}: {msg}'
        self.announcer.announce(self.pack_error(msg))
        
    def send_success(self,msg):
        data = {'msg':msg}
        self.announcer.announce(self.pack_success(msg))
        
    def send_result(self,type:str,name:str,id:str,result:dict):
        data = {
            'type':type,
            'name':name,
            'id':id,
            'result':result
        }
        self.announcer.announce(self.pack_result(data))

    def send_end(self):
        self.announcer.announce(self.format_sse({'msg':'ok'},'end'))