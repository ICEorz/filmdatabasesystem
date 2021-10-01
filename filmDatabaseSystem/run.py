import requests.cookies
from flask import *
from film import Film
from filmdatabase import FilmDatabase
from flask_sqlalchemy import Pagination

db = FilmDatabase()
db.load_database()
nname = [""]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/searchresult', methods=['POST', 'GET'])
def searchresult(nowname=nname):
    if request.method == 'POST':
        res = request.form
        nowname = [res['Name']]
        page = 1
    else:
        page = request.args.get('page', 1, type=int)
    '''
        查找电影名
        查找人名
        查找类型名
        部分电影名 + 部分人名
        模糊搜索电影名 + 人名
    '''
    res_list = None

    fname = nowname[0]
    nameres = db.get_film_by_exact_name(fname)
    if nameres:
        res_list = [nameres[0].name]
    else:
        personres = db.get_film_by_person_name(fname)
        if personres:
            res_list = [personres[0].name]
        else:
            genreres = db.get_film_by_genre_name(fname)
            if genreres:
                res_list = genreres
            else:
                partlist = db.get_film_by_part_name(fname) + db.get_film_by_part_person_name(fname)
                if partlist:
                    res_list = partlist
                else:
                    res_list = db.get_film_by_fuzz_name(fname) + db.get_film_by_fuzz_person_name(fname)
    isperson = []
    for k in res_list:
        if db.get_film_by_person_name(k):
            isperson.append(True)
        else:
            isperson.append(False)

    datalist = []
    for k in range(len(res_list)):
        datalist.append((res_list[k], isperson[k]))
    # 分页
    limit = 10


    start = (page - 1) * limit
    end = page * limit if len(datalist) > page * limit else len(datalist)
    per_page = int(request.args.get('per_page', 2))

    paginate = Pagination(datalist, page, per_page=10, total=len(datalist), items=datalist[start:end])
    data = paginate.items
    return render_template('searchresult.html', paginate=paginate, data=data)


@app.route('/details/<name>')
def details(name):
    film = db.get_film_by_exact_name(name)[0]
    db.film_click(film)
    data = {}
    data['imgpath'] = '/image/filmimage/' + str(film.id) + '.jpg'
    data['film'] = film
    return render_template('details.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
