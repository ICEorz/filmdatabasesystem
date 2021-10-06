# -*- coding: utf-8 -*-
import jieba
import numpy as np
import re
from filmdatabase import *
from tqdm import tqdm


def get_word_sim(s1, s2):
    cut1 = jieba.cut(s1)
    cut2 = jieba.cut(s2)
    list_word1 = (','.join(cut1)).split(',')
    list_word2 = (','.join(cut2)).split(',')
    key_word = list(set(list_word1 + list_word2))
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    for i in range(len(key_word)):
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    sim = float(np.dot(word_vector1, word_vector2) / (np.linalg.norm(word_vector1) * np.linalg.norm(word_vector2)))
    return sim


if __name__ == '__main__':
    db = FilmDatabase()
    # db.load_database()
    # db.create_database()
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
    db.database = database
    print(database[0].name)
    print(database[1].detailed_info)
    print(database[1655].detailed_info)
    print(get_word_sim(database[0].detailed_info, database[1].detailed_info))
    simlist = []
    for i in tqdm(range(db.database)):
        if db.database[i].detailed_info == '暂无简介':
            simlist.append([])
            continue
        else:
            tmplist = []
            for j in range(len(db.database)):
                if i == j or db.database[j].detailed_info == '暂无简介':
                    continue
                else:
                    tmplist.append(
                        (j, get_word_sim(db.database[i].detailed_info, db.database[j].detailed_info))
                    )
            tmplist = sorted(tmplist, key=lambda x: x[1])
            simlist.append([tmplist[-1][0], tmplist[-2][0], tmplist[-3][0]])
    print(simlist)


    def cos_dist(vec1, vec2):
        """
        :param vec1: 向量1
        :param vec2: 向量2
        :return: 返回两个向量的余弦相似度
        """
        dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        return dist1
