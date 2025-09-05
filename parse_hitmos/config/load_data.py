import json
import os.path

class SID:
    def __init__(self):
        self.sid = None
        self.path = os.path.join(os.path.dirname(__file__), 'data.json')
        self.load_sid()

    def load_sid(self):
        if not self.sid:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.sid = json.load(f)['sid']
    
    def get_sid(self):
        return self.sid
    
    def load_config(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_sid(self, sid):
        data = self.update_sid(sid)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def update_sid(self, sid):
        data = self.load_config()
        self.sid = sid['sid']
        data['sid']=sid['sid']
        return json.loads(json.dumps(data, indent=4))
    
