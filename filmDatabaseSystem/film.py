# _*_ coding:utf-8 _*_
import os.path

from bplustree import BPlusTree
from heap import maxheap
from fuzzywuzzy import fuzz
from binarysearch.binarySearch import *
import pickle


class Film(object):
    def __init__(self, name, director, author, actor, genre, date, detailed_info, click, id=0, score:float=0, espeople=0):
        self.name = name
        self.director = director
        self.author = author
        self.actor = actor
        self.genre = genre
        self.date = date
        self.detailed_info = detailed_info
        self.click = click
        self.id = id
        self.score = score
        self.espeople = espeople

    def __str__(self):
        return ("电影名：" + self.name + '\n'
                + "导演：" + " ".join(e for e in self.director) + '\n'
                + "编剧：" + " ".join(e for e in self.author) + '\n'
                + "类型：" + " ".join(e for e in self.genre) + '\n'
                + "演员：" + " ".join(e for e in self.actor) + '\n'
                + "上映日期：" + self.date + '\n'
                + "简介：" + self.detailed_info + '\n'
                + "点击量：" + str(self.click) + '\n'
                + "id=" + str(self.id) + '\n'
                + "评分：" + str(self.score) + '\n'
                + "评分人数：" + str(self.espeople) + '\n')

    def add_click(self):
        self.click += 1

    def judge_score(self, score):
        allscore = self.score * self.espeople + score
        self.espeople += 1
        self.score = allscore / self.espeople

    def __lt__(self, other):
        return self.name < other

    def __le__(self, other):
        return self.name <= other

    def __eq__(self, other):
        return self.name == other


