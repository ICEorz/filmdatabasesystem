# _*_ coding:utf-8 _*_
import time

import film
import json
import pickle
from bplustree import BPlusTree

def add_film(newfilm):
    all_data = []
    with open('./dataset/processeddata.pkl', 'rb') as f:
        all_data = pickle.loads(f.read())
    all_data.append(newfilm)
    with open('./dataset/processeddata.pkl', 'wb') as f:
        f.write(pickle.dumps(all_data))


def delete_film(filmname):
    all_data = []
    with open('./dataset/processeddata.pkl', 'rb') as f:
        all_data = pickle.loads(f.read())
    for data in all_data[:]:
        if data.name == filmname:
           all_data.remove(data)
    with open('./dataset/processeddata.pkl', 'wb') as f:
        f.write(pickle.dumps(all_data))


def load250():
    write_data = []
    with open('./dataset/sourcedata.json', 'r') as f:
        all_data = json.load(f)
        for data in all_data:
            name = data['name'].split()[0]
            director_list = data['director']
            director = []
            for direc in director_list:
                director.append(direc['name'].split()[0])
            author_list = data['author']
            author = []
            for au in author_list:
                author.append(au['name'].split()[0])
            actor_list = data['actor']
            actor = []
            for i in range(min(len(actor_list), 5)):
                actor.append(actor_list[i]['name'].split()[0])
            genre = data['genre']
            date = data['datePublished']
            detailed_info = data['detailed_info']
            write_data.append(film.Film(name, director, author, actor, genre, date, detailed_info, 0))

    with open('./dataset/processeddata.pkl', 'wb') as f:
        f.write(pickle.dumps(write_data))


def save250():
    all_dict = {}
    genre_dict = {}
    with open('./dataset/processeddata.pkl', 'rb') as f:
        all_data = pickle.loads(f.read())
        for data in all_data:
            director = data.director
            author = data.author
            actor = data.actor
            genre = data.genre
            for di in director + author + actor:
                if di not in all_dict:
                    all_dict[di] = [data.name]
                else:
                    if data.name not in all_dict[di]:
                        all_dict[di].append(data.name)

            for ge in genre:
                if ge not in genre_dict:
                    genre_dict[ge] = [data.name]
                else:
                    if data.name not in genre_dict[ge]:
                        genre_dict[ge].append(data.name)

        with open('./database/namedb.pkl', 'wb') as dd:
            tr = BPlusTree(10)
            for data in all_data:
                tr.insert(data.name, data)
            dd.write(pickle.dumps(tr))


    with open('./database/persontofilm.pkl', 'wb') as f:
        f.write(pickle.dumps(all_dict))

    with open('./database/persontofilm.pkl', 'rb') as f:
        readdict = pickle.loads(f.read())

    with open('./database/genredict.pkl', 'wb') as f:
        f.write(pickle.dumps(genre_dict))

    with open('./database/genredict.pkl', 'rb') as f:
        readdict = pickle.loads(f.read())
        for k, v in readdict.items():
            print(k, v)

def generate_heap():
    with open('./database/clickranklist.pkl', 'wb') as f:
        with open('./database/namedb.pkl', 'rb') as s:
            s = pickle.loads(s.read())


if __name__ == '__main__':

    # myl = ['犯罪', '剧情', '爱情', '同性', '动作', '灾难', '喜剧', '战争', '动画', '奇幻', '历史', '科幻', '悬疑', '冒险', '音乐',
    #        '歌舞', '惊悚', '古装', '传记', '家庭', '运动', '西部', '情色', '儿童', '纪录片', '武侠', '恐怖']
    # for v in myl:
    #     print('<input type = "radio" name = "genre" value = "%s" /> %s ' % (v, v))
    # save250()

    indexstr = ' /$$$$$$$$ /$$ /$$               /$$$$$$$  /$$        /$$$$$$                    \
    | $$_____/|__/| $$              | $$__  $$| $$       /$$__  $$                    \
    | $$       /$$| $$ /$$$$$$/$$$$ | $$  \ $$| $$$$$$$ | $$  \__/ /$$   /$$  /$$$$$$$\
    | $$$$$   | $$| $$| $$_  $$_  $$| $$  | $$| $$__  $$|  $$$$$$ | $$  | $$ /$$_____/\
    | $$__/   | $$| $$| $$ \ $$ \ $$| $$  | $$| $$  \ $$ \____  $$| $$  | $$|  $$$$$$ \
    | $$      | $$| $$| $$ | $$ | $$| $$  | $$| $$  | $$ /$$  \ $$| $$  | $$ \____  $$\
    | $$      | $$| $$| $$ | $$ | $$| $$$$$$$/| $$$$$$$/|  $$$$$$/|  $$$$$$$ /$$$$$$$/\
    |__/      |__/|__/|__/ |__/ |__/|_______/ |_______/  \______/  \____  $$|_______/ \
                                                                   /$$  | $$          \
                                                                  |  $$$$$$/          \
                                                                   \______/           '

    time.sleep(5)
