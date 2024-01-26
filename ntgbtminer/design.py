from config import Db
from views import getLogs
from utils import readEnv





class Logs:
    def __init__(self, ENV):
        self.conn = Db(ENV)
        pass

    def insert(self, logs):        
        self.conn.insert(logs)

    def getLogs(self):
        return [{"log": 1}]
    


ENV = readEnv()

l = Logs(ENV)

logs = l.getLogs()

l.insert(logs)

