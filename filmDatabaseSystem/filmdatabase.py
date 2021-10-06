# _*_ coding:utf-8 _*_
import os.path
from bplustree import BPlusTree
from heap import maxheap
from fuzzywuzzy import fuzz
from binarysearch.binarySearch import *
import pickle
from film import Film
import string
import zhon.hanzi
from kmp.kmp import *
import json
from quicksort.quicksort import quick_sort
import numpy as np


class FilmDatabase(object):
    def __init__(self):
        self.database = None
        self.clickranklist = None
        self.scoreranklist = None
        self.modify_flag = False
        self.filmdb = None
        self.persondb = None
        self.genredb = None
        self.famouslist = None

    @staticmethod
    def remove_all_punc(s):
        for i in string.punctuation:
            s = s.replace(i, '')
        for i in zhon.hanzi.punctuation:
            s = s.replace(i, '')
        return s

    # def key_to_val(self, res: list):
    #     rl = []
    #     for idx in res:
    #         rl.append(self.database[idx])
    #     return rl

    def get_film_by_exact_name(self, name):
        res = self.filmdb[name]
        if res is None:
            return None
        else:
            return res

    def get_film_by_part_name(self, name):
        res = []
        name = self.remove_all_punc(name)
        nexti = get_next(name)
        for k in self.filmdb.keys():
            if self.remove_all_punc(k) == name:
                res.insert(0, k)
            elif kmp(self.remove_all_punc(k), name, nexti):
                res.append(k)
        return res

    def get_film_by_fuzz_name(self, name):
        def strcmp(a, b):
            return fuzz.ratio(a, name) <= fuzz.ratio(b, name)
        mh = maxheap.MaxHeap(maxsize=len(self.database), cmp=strcmp)
        for k in self.filmdb.keys():
            mh.push(k)
        res = []
        for i in range(30):
            if len(mh):
                res.append(mh.pop())
            else:
                break
        return res

    def get_film_by_person_name(self, name):
        res = self.persondb[name]
        if res is None:
            return None
        else:
            return res

    def get_film_by_part_person_name(self, name):
        res = list()
        name = self.remove_all_punc(name)
        nexti = get_next(name)
        for k in self.persondb.keys():
            if self.remove_all_punc(k) == name:
                res.insert(0, k)
            elif kmp(self.remove_all_punc(k), name, nexti):
                res.append(k)
        return res

    def get_film_by_fuzz_person_name(self, name):

        def strcmp(a, b):
            return fuzz.ratio(a, name) <= fuzz.ratio(b, name)
        mh = maxheap.MaxHeap(maxsize=len(self.database), cmp=strcmp)
        for k in self.persondb.keys():
            mh.push(k)
        res = list()
        for i in range(30):
            if len(mh):
                res.append(mh.pop())
            else:
                break
        return res

    def get_film_by_genre_name(self, name):
        filmres = self.genredb[name]
        if filmres is None:
            return None
        else:
            return filmres

    def get_filmclickranklist(self):
        return self.clickranklist[-2:0:-1]

    def get_filmscoreranklist(self):
        return self.scoreranklist[-2:0:-1]

    def load_dataset(self):
        with open('./dataset/dataset.json', 'r') as f:
            database = list()
            diclist = json.load(f)
            for i, data in enumerate(diclist):
                database.append(
                    Film(
                        name=data['name'],
                        director=data['director'],
                        author=data['author'],
                        actor=data['actor'],
                        genre=data['genre'],
                        date=data['date'],
                        detailed_info=data['detailed_info'],
                        region=data['region'],
                        time=data['time'],
                        douban=data['douban'],
                        imdb=data['imdb'],
                        img=data['img'],
                        click=0,
                        keyid=int(i),
                        score=0,
                        espeople=0,
                        comments=[]
                    )
                )
            self.database = database

    def load_database(self):
        with open('./database/database.json', 'r') as f:
            database = list()
            diclist = json.load(f)
            for i, data in enumerate(diclist):
                database.append(
                    Film(
                        name=data['name'],
                        director=data['director'],
                        author=data['author'],
                        actor=data['actor'],
                        genre=data['genre'],
                        date=data['date'],
                        detailed_info=data['detailed_info'],
                        region=data['region'],
                        time=data['time'],
                        douban=data['douban'],
                        imdb=data['imdb'],
                        img=data['img'],
                        click=data['click'],
                        keyid=data['keyid'],
                        score=data['score'],
                        espeople=data['espeople'],
                        comments=data['comments']
                    )
                )
            self.database = database

    def create_database(self):
        self.filmdb = BPlusTree(50)
        self.persondb = BPlusTree(50)
        self.genredb = BPlusTree(50)
        for i, data in enumerate(self.database):
            self.filmdb.insert(data.name, i)
            for person in set(data.director + data.author + data.director):
                self.persondb.insert(person, i)
            for genre in data.genre:
                self.genredb.insert(genre, i)
        self.resetclick()
        self.resetscore()

    def load_index(self):
        with open('./database/filmdb.pkl', 'rb') as f:
            self.filmdb = pickle.loads(f.read())
        with open('./database/persondb.pkl', 'rb') as f:
            self.persondb = pickle.loads(f.read())
        with open('./database/genredb.pkl', 'rb') as f:
            self.genredb = pickle.loads(f.read())

    def save_index(self):
        with open('./database/filmdb.pkl', 'wb') as f:
            f.write(pickle.dumps(self.filmdb))
        with open('./database/persondb.pkl', 'wb') as f:
            f.write(pickle.dumps(self.persondb))
        with open('./database/genredb.pkl', 'wb') as f:
            f.write(pickle.dumps(self.genredb))

    def save_ranklist(self):
        with open('./database/clickranklist.pkl', 'wb') as f:
            f.write(pickle.dumps(self.clickranklist))
        with open('./database/scoreranklist.pkl', 'wb') as f:
            f.write(pickle.dumps(self.scoreranklist))

    def clear_score_and_click(self):
        for data in self.database:
            data.click = 0
            data.score = 0
            data.espeople = 0
        self.save_database()

    def save_database(self):
        save_list = []
        for data in self.database:
            tmp = dict()
            tmp['name'] = data.name
            tmp['director'] = data.director
            tmp['author'] = data.author
            tmp['actor'] = data.actor
            tmp['genre'] = data.genre
            tmp['date'] = data.date
            tmp['detailed_info'] = data.detailed_info
            tmp['region'] = data.region
            tmp['time'] = data.time
            tmp['douban'] = data.douban
            tmp['imdb'] = data.imdb
            tmp['img'] = data.img
            tmp['click'] = data.click
            tmp['keyid'] = data.keyid
            tmp['score'] = data.score
            tmp['espeople'] = data.espeople
            tmp['comments'] = data.comments
            save_list.append(tmp)
        with open('./database/database.json', 'w') as f:
            json.dump(save_list, f)

    # def film_click(self, filmid: int):
    #     film = self.database[filmid]
    #
    #     def change(flist: list, id, click):
    #         upper = upper_bound(flist, click, key=lambda x: x[1])
    #         lower = lower_bound(flist, click, key=lambda x: x[1])
    #         now_pos = flist.index([id, click], lower)
    #         flist[now_pos][1] += 1
    #         if now_pos == upper - 1:
    #             return
    #         else:
    #             flist[now_pos], flist[upper-1] = flist[upper-1], flist[now_pos]
    #
    #     change(self.clickranklist, filmid, film.click)
    #     film.add_click()
    #     self.save_database()
    #     self.save_ranklist()

    # def film_score(self, filmid: int, newscore:float):
    #     film = self.database[filmid]
    #     old_score = film.score
    #     film.judge_score(newscore)
    #     new_score = film.score
    #
    #     def change(flist: list, id, score: float, newscore: float):
    #         lower = lower_bound(flist, score, key=lambda x: x[1])
    #         now_pos = flist.index([id, round(float(score), 1)], lower)
    #         flist.pop(now_pos)
    #         upper = upper_bound(flist, newscore, key=lambda x: x[1])
    #         flist.insert(upper, [id, round(float(newscore), 1)])
    #
    #     change(self.scoreranklist, filmid, old_score, new_score)
    #     self.save_database()
    #     self.save_ranklist()

    def resetclick(self):
        res = list()
        res.append(['head', -float('inf')])
        res.append(['tail', float('inf')])
        for data in self.database:
            res.append([data.keyid, data.click])
        quick_sort(res, 0, len(res) - 1, key=lambda t: t[1])
        self.clickranklist = res

    def resetscore(self):
        res = list()
        res.append(['head', -float('inf')])
        res.append(['tail', float('inf')])
        for data in self.database:
            res.append([data.keyid, round(float(data.score), 1)])
        quick_sort(res, 0, len(res) - 1, key=lambda t: t[1])
        self.scoreranklist = res

    def get_famous(self):
        res = []
        for d in self.database:
            if '改编' in d.detailed_info:
                res.append(d.keyid)
        self.famouslist = res

    def film_recommand(self, film: Film, k):
        simlist = []
        for i in range(len(self.database)):
            if i == film.keyid:
                continue
            else:
                simlist.append(
                    (i, film_similarity(film, self.database[i]))
                )
        quick_sort(simlist, 0, len(simlist) - 1, key=lambda t: t[1])
        return simlist[-1-k:-1][::-1]


def film_similarity(film1: Film, film2: Film):
    director = list(set(film1.director + film2.director))
    author = list(set(film1.author + film2.author))
    actor = list(set(film1.actor + film2.actor))
    genre = list(set(film1.genre + film2.genre))
    lend, lenau, lenac, lenge = len(director), len(author), len(actor), len(genre)
    vec1 = np.zeros(lend + lenau + lenac + lenge)
    vec2 = np.zeros(lend + lenau + lenac + lenge)
    for i in range(lend):
        if director[i] in film1.director:
            vec1[i] = 1
        if director[i] in film2.director:
            vec2[i] = 1
    for i in range(lenau):
        if author[i] in film1.author:
            vec1[i + lend] = 1
        if author[i] in film2.author:
            vec2[i + lend] = 1
    for i in range(lenac):
        if actor[i] in film1.actor:
            vec1[i + lend + lenau] = 1
        if actor[i] in film2.actor:
            vec2[i + lend + lenau] = 1
    for i in range(lenge):
        if genre[i] in film1.genre:
            vec1[i + lend + lenau + lenac] = 1
        if genre[i] in film2.genre:
            vec2[i + lend + lenau + lenac] = 1
    return cos_dist(vec1, vec2)


def cos_dist(vec1, vec2):
    dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return dist1


if __name__ == '__main__':
    def reset_db():
        db = FilmDatabase()
        db.load_dataset()
        db.create_database()
        # db.load_database()
        '''
            director --list
            author --list 
            actor --list  
            detailed_info --str 
            date --str 
            region --list 
            time --str 暂无时长
        '''

        def is_Chinese(word):
            for ch in word:
                if '\u4e00' <= ch <= '\u9fff':
                    return True
            return False

        strss = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        for data in db.database:
            data.actor = data.actor[:5]
            if data.director == ['null']:
                data.director = ['暂无导演信息']
            if data.author == ['null']:
                data.director = ['暂无编剧信息']
            if data.actor == ['null']:
                data.actor = ['暂无演员信息']
            if data.detailed_info == 'null' or data.detailed_info is None or (not is_Chinese(data.detailed_info[0]) and data.detailed_info[0] not in strss):
                data.detailed_info = '暂无简介'
            if data.date == 'null':
                data.date = '暂无上映日期'
            if data.region == ['null']:
                data.region = ['暂无国家/地区']
            if data.time == 'null':
                data.time = '暂无时长'
            if data.douban == 'null':
                data.douban = None
            if data.imdb == 'null':
                data.imdb = None
            #     print(data.name)
            #     data.detailed_info = '暂无简介'
        # print(db.database[0].name)
        db.clear_score_and_click()
        db.save_database()

        print(db.database[0].imdb)


    db = FilmDatabase()
    db.load_database()
    db.create_database()
    print(db.database[256].img)
    db.database[256].img = 'https://img2.doubanio.com/view/photo/s_ratio_poster/public/p1592298962.webp'
    db.save_database()
    # print(db.get_film_by_part_person_name('鲁伯特·哈维'))
    # print(film_similarity(db.database[0], db.database[1]))
    # tmp = db.film_recommand(db.database[0], 10)
    # for data in tmp:
    #     print(db.database[data[0]].name)

    # print(db.database[0].imdb)
    # def famousadapt():
    #     strss = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    #     db = FilmDatabase()
    #     db.load_dataset()
    #     db.create_database()
    #     print(db.database[0].detailed_info[0] in strss)

        # for d in db.database:
        #     if '改编' in d.detailed_info:
        #         print(d.name)


    # db = FilmDatabase()
    # db.load_dataset()
    # db.create_database()
    # db.save_database()
    # print(db.database[0])

    # reset_db()
    # s = db.get_film_by_exact_name('小王子')
    # for i in s:
    #     print(i.img)
    # print(db.database)
    # for k in db.filmdb.keys():
    #     print(k)

    # for k, v in db.database.items():
    #     if '小说' in v[0].detailed_info and '改编' in v[0].detailed_info:
    #         print(k, v[0].detailed_info)
    # db.save_database()
    # db.resetscore()
    # print(db.scoreranklist)
    # # db.resetscore()
    # # print(db.scoreranklist)
    # db.film_score(db.get_film_by_exact_name('小丑')[0], 7.0)
    # print(db.scoreranklist)
    # print(db.get_film_by_exact_name('小丑')[0].score)
    # db.save_database()



    # print(db.database.values()[1].score)
    # for d in db.database.values():
    #     d.score=0
    #     d.espeople=0
    # path = './static/image/filmimage/'
    # for k in db.database.keys():
    #     print(k)
    # print("龙黑" > "龙")
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
