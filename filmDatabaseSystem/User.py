import json
from bplustree import BPlusTree
from werkzeug.security import generate_password_hash


class SUser(object):
    def __init__(self, username, password, keyid, scoredict):
        self.username = username
        self.password = password
        self.keyid = keyid
        self.scoredict = scoredict
    # def todict(self):
    #     return {
    #         "name": self.username,
    #         "password": self.password,
    #         "id": self.keyid + 3,
    #         "dict": self.scoredict
    #     }


class Userdatabase(object):
    def __init__(self):
        self.database = None
        self.userdb = None

    def load_user(self):
        with open('./database/userdb.json', 'r') as f:
            diclist = json.load(f)
            database = list()
            for i, data in enumerate(diclist):
                database.append(
                    SUser(
                        username=data['username'],
                        password=data['password'],
                        keyid=i,
                        scoredict=data['scoredict']
                    )
                )
            self.database = database

    def save_user(self):
        with open('./database/userdb.json', 'w') as f:
            diclist = list()
            for data in self.database:
                tmp = dict()
                tmp['username'] = data.username
                tmp['password'] = data.password
                tmp['scoredict'] = data.scoredict
                diclist.append(tmp)
            json.dump(diclist, f)

    def create_database(self):
        tr = BPlusTree(50)
        for data in self.database:
            tr.insert(data.username, data.keyid)
        self.userdb = tr

    def add_user(self, name, password):
        user = SUser(name, password, len(self.database), dict())
        self.database.append(user)
        self.userdb.insert(name, user.keyid)

    def get_user_by_id(self, userid: str):
        userid = int(userid)
        if userid >= len(self.database):
            return None
        else:
            return self.database[userid]

    def get_user_by_name(self, name):
        res = self.userdb[name]
        if res is None:
            return None
        else:
            return self.database[res[0]]


if __name__ == '__main__':
    db = Userdatabase()
    db.load_user()
    db.create_database()
    # db.database = [SUser('flag', '0', 0, dict()), SUser('zyy', 'zyy001213', 1, dict()), SUser('hwj is sb', 'harry68', 2, dict())]
    db.get_user_by_name('hwj').scoredict['3'] = True
    print('3' in db.get_user_by_name('hwj').scoredict)
    # db.save_user()
