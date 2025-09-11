import json
import os.path

class SID:
    def __init__(self):
        self.sid = None
        self.path = os.path.join(os.path.dirname(__file__), 'data.json')
        print(self.path)
        self.__load_sid()

    def __load_sid(self):
        if not self.sid:
            if not os.path.exists(self.path):  
                with open(self.path, encoding='utf-8', mode='w') as data:
                    json.dump({'sid': ''}, data, indent=4)

            with open(self.path, 'r', encoding='utf-8') as f:
                self.sid = json.load(f)['sid']
    
    def get_sid(self):
        return self.sid
    
    def __load_config(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_sid(self, sid):
        data = self.__update_sid(sid)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def __update_sid(self, sid):
        data = self.__load_config()
        self.sid = sid['sid']
        data['sid']=sid['sid']
        return json.loads(json.dumps(data, indent=4))
    
