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
    return render_template('index.html', genrelist=db.genredb.keys())


@app.route('/searchresult', methods=['POST', 'GET'])
def searchresult(nowname=['']):
    if request.method == 'POST':
        res = request.form
        nowname = [res['Name']]
        page = 1
    else:
        namem = request.args.get('nowname', None)
        page = request.args.get('page', 1, type=int)
        if namem:
            nowname = [namem]
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
            res_list = personres
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

    # dataprocess
    data_list = []
    for item in res_list:
        if db.get_film_by_exact_name(item):
            fm = db.get_film_by_exact_name(item)[0]
            data_list.append(
                [
                    False,  # isperson
                    fm,  # data
                ]
            )
        else:
            data_list.append(
                [
                    True,  # isperson
                    item  # name
                ]
            )
    # pagination
    limit = 10
    start = (page - 1) * limit
    end = page * limit if len(data_list) > page * limit else len(data_list)
    per_page = int(request.args.get('per_page', 2))

    paginate = Pagination(data_list, page, per_page=10, total=len(data_list), items=data_list[start:end])
    data = paginate.items
    return render_template('searchresult.html', pagename=nowname, paginate=paginate, data=data, genrelist=db.genredb.keys())


@app.route('/ranklist/<name>', methods=['GET'])
def ranklist(name=[]):
    data_list = []
    namem = request.args.get('name', None)
    page = request.args.get('page', 1, type=int)
    print(page)
    print(name)
    if namem:
        name = [namem]

    if name == 'score':
        for nm in db.get_filmscoreranklist():
            data_list.append(db.get_film_by_exact_name(nm[0])[0])
    else:
        for nm in db.get_filmclickranklist():
            data_list.append(db.get_film_by_exact_name(nm[0])[0])
    # pagination
    limit = 10
    start = (page - 1) * limit
    end = page * limit if len(data_list) > page * limit else len(data_list)

    paginate = Pagination(data_list, page, per_page=10, total=len(data_list), items=data_list[start:end])
    data = paginate.items
    return render_template('ranklist.html', pagename=name, paginate=paginate, data=data, genrelist=db.genredb.keys())


@app.route('/details/<name>')
def details(name):
    film = db.get_film_by_exact_name(name)[0]
    db.film_click(film)
    data = {}
    data['imgpath'] = '/image/filmimage/' + str(film.id) + '.jpg'
    data['film'] = film
    return render_template('details.html', data=data, genrelist=db.genredb.keys())


if __name__ == '__main__':
    app.run(debug=True)
