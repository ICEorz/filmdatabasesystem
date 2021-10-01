# _*_ coding:utf-8 _*_
import os.path
from bplustree import BPlusTree
from heap import maxheap
from fuzzywuzzy import fuzz
from binarysearch.binarySearch import *
import pickle
from film import Film


class FilmDatabase(object):
    def __init__(self):
        self.database = None
        self.clickranklist = None
        self.modify_flag = False
        self.persondb = None
        self.genredb = None

    def get_film_by_exact_name(self, name):
        res = self.database[name]
        return res

    def get_film_by_part_name(self, name):
        res = []
        for k, v in self.database.items():
            if name in k:
                res.append(k)
        return res

    def get_film_by_fuzz_name(self, name):
        def strcmp(a, b):
            return fuzz.ratio(a, name) <= fuzz.ratio(b, name)
        mh = maxheap.MaxHeap(maxsize=len(self.database), cmp=strcmp)
        for k, v in self.database.items():
            mh.push(k)
        res = []
        for i in range(30):
            if len(mh):
                res.append(mh.pop())
            else:
                break
        return res

    def get_film_by_person_name(self, name):
        return self.persondb[name]

    def get_film_by_part_person_name(self, name):
        res = []
        for k, v in self.persondb.items():
            if name in k:
                res.extend(v)
        return res

    def get_film_by_fuzz_person_name(self, name):
        def strcmp(a, b):
            return fuzz.ratio(a, name) <= fuzz.ratio(b, name)
        mh = maxheap.MaxHeap(maxsize=len(self.database), cmp=strcmp)
        for k, v in self.persondb.items():
            mh.push(k)
        res = []
        for i in range(30):
            if len(mh):
                res.append(mh.pop())
            else:
                break
        return res

    def get_film_by_genre_name(self, name):
        return self.genredb[name]

    def get_filmranklist(self):
        return self.clickranklist[-2:0:-1]

    def load_database(self):
        with open('./database/namedb.pkl', 'rb') as f:
            self.database = pickle.loads(f.read())
        with open('./database/clickranklist.pkl', 'rb') as f:
            self.clickranklist = pickle.loads(f.read())
        with open('./database/persondb.pkl', 'rb') as f:
            self.persondb = pickle.loads(f.read())
        with open('./database/genredb.pkl', 'rb') as f:
            self.genredb = pickle.loads(f.read())

    def save_database(self):
        with open('./database/namedb.pkl', 'wb') as f:
            f.write(pickle.dumps(self.database))
        with open('./database/clickranklist.pkl', 'wb') as f:
            f.write(pickle.dumps(self.clickranklist))
        with open('./database/persondb.pkl', 'wb') as f:
            f.write(pickle.dumps(self.persondb))
        with open('./database/genredb.pkl', 'wb') as f:
            f.write(pickle.dumps(self.genredb))

    def film_click(self, film: Film):
        def change(flist: list, name, click):
            upper = upper_bound(flist, click, key=lambda x: x[1])
            lower = lower_bound(flist, click, key=lambda x: x[1])
            now_pos = flist.index([name, click], lower, upper)
            flist[now_pos][1] += 1
            if now_pos == upper - 1:
                return
            else:
                flist[now_pos], flist[upper-1] = flist[upper-1], flist[now_pos]
        change(self.clickranklist, film.name, film.click)
        self.get_film_by_exact_name(film.name)[0].add_click()
        self.save_database()

    def resetclick(self):
        res = []
        res.append(['head', -float('inf')])
        res.append(['tail', float('inf')])
        for k, v in self.database.items():
            res.append([k, v.click])
        sorted(res, key=lambda t: t[1])
        self.clickranklist = res


if __name__ == '__main__':
    db = FilmDatabase()
    db.load_database()
    print(db.database.values()[1].score)
    # for d in db.database.values():
    #     d.score=0
    #     d.espeople=0
    path = './static/image/filmimage/'
    for data in db.database.values():
        if os.path.exists(path + data.name + '.jpg'):
            os.rename(path + data.name + '.jpg', path + data.id + '.jpg')

    # for k, v in db.persondb.items():
    #     print(k, v)
    # print(len(db.database))

    # tr = BPlusTree(25)
    # for data in db.database.values():
    #     # print(data.actor)
    #     for ac in data.actor:
    #         if tr[ac] == None:
    #             tr.insert(ac, data.name)
    #         elif tr[ac] is not None and data.name not in tr[ac]:
    #             tr.insert(ac, data.name)
    #         else:
    #             continue
    #     for ac in data.director:
    #         if tr[ac] == None:
    #             tr.insert(ac, data.name)
    #         elif tr[ac] is not None and data.name not in tr[ac]:
    #             tr.insert(ac, data.name)
    #         else:
    #             continue
    #     for ac in data.author:
    #         if tr[ac] == None:
    #             tr.insert(ac, data.name)
    #         elif tr[ac] is not None and data.name not in tr[ac]:
    #             tr.insert(ac, data.name)
    #         else:
    #             continue
    # print(tr.items())
    # print(db.persondb.items())
    # print(db.get_film_by_person_name('姜文'))
    # for data in db.database.values():
    #     print(data.name, data.genre)
    #     for ge in data.genre:
    #         tr.insert(ge, data.name)
    # print(tr.items())
    # with open('./database/genredb.pkl', 'wb') as f:
    #     f.write(pickle.dumps(tr))
    #     print(1)

    # for k in db.persondb.items():
    #     print(k)
    # db.save_database()
    # with open('./database/persondb.pkl', 'wb') as f:
    #     f.write(pickle.dumps(tr))
    #     print(1)
    # for j in db.database.values():
    #     print(j)
    # # db.database.delete('小丑')
    # s: Film = Film('小丑', ['托德·菲利普斯'], ['托德·菲利普斯', '斯科特·西尔弗', '鲍勃·凯恩', '比尔·芬格', '杰瑞·罗宾逊'],
    #                         ['华金·菲尼克斯', '罗伯特·德尼罗', '马克·马龙', '莎姬·贝兹', '谢伊·惠格姆'], ['剧情', '惊悚', '犯罪'], '2019-08-31', '湿冷无望的哥谭市，卑微的亚瑟·弗兰克（华金·菲尼克斯 Joaquin Phoenix 饰）依靠扮演小丑赚取营生。与之相依为命的母亲患有精神疾病，而亚瑟深记母亲的教诲，无论遭受怎样的挫折都笑对人生，却因此让自己背负着莫大的压力，濒临崩溃。他梦想成为一名脱口秀演员，怎奈生活一次次将失望狠狠地砸在他的头上。不仅如此，他因意外丢掉了工作，偶然瞥见母亲的秘密，又使他心中燃起对那个与之地位悬殊却从未谋面的父亲的殷切渴望。命运习惯了事与愿违，空荡荡的地铁内，悲伤的小丑在无法自已的癫狂笑声中大开杀戒……\n\n\t本片荣获第76届威尼斯电影节金狮奖。', click=0, id=250)
    # # db.database.insert('ss', 10)
    # # db.database.insert('11', 3)
    # # for i, a in enumerate(db.database.items()):
    # tr = BPlusTree(10)
    # for i in db.database.items():
    #     tr.insert(i[0], i[1][0])
    # tr.insert('小丑', s)
    # db.database = tr
    # db.save_database()
    # print(tr['小丑'][0])


    #     print(i, a[0], a[1][0].id)
    #     a[1][0].id = i
    # db.save_database()

    # '2019-08-31'
    #
    # for i, k in enumerate(db.database.values()):
    #     # if not os.path.exists(path+k+'.jpg'):
    #     #     print(k)
    #     k.id = i
    #     print(k)
    # db.save_database()
    # for k, v in db.database.items():
    #     print(k, v)
    #     print(v[0].id)
    #     os.rename(path + k + '.jpg', path + 'film' + str(v[0].id) + '.jpg')

    # with open('./database/clickranklist.pkl', 'wb') as f:
    #     []

    # print(db.database)
    # ranklist = [['head', -float('inf')]]
    # for k, v in db.database.items():
    #     print(k, v[0].click)
    #     ranklist.append([k, v[0].click])
    # ranklist.append(['tail', float('inf')])
    # ranklist = sorted(ranklist, key=lambda x: x[1])
    # def change(flist: list, name, click):
    #     upper = upper_bound(ranklist, 0, len(ranklist) - 1, click, key=lambda x: x[1])
    #     lower = lower_bound(ranklist, 0, len(ranklist) - 1, click, key=lambda x: x[1])
    #     print(upper, lower)
    #     now_pos = flist.index([name, click], lower, upper)
    #     flist[now_pos][1] += 1
    #     if now_pos == upper - 1:
    #         return
    #     else:
    #         flist[now_pos], flist[upper-1] = flist[upper-1], flist[now_pos]
    # print(ranklist)
    # with open('./database/clickranklist.pkl', 'wb') as f:
    #     f.write(pickle.dumps(ranklist))
    # with open('./database/clickranklist.pkl', 'rb') as f:
    #     rl = pickle.loads(f.read())
    #     print(rl)
    # db.film_click(db.get_film_by_exact_name('一一')[0])
    # db.film_click(db.get_film_by_exact_name('一一')[0])
    # print(db.get_film_by_exact_name('一一')[0])
    # print(db.get_filmranklist())
    # print(db.clickranklist)
