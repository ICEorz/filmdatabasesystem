import requests.cookies
from flask import *
from film import Film
from filmdatabase import FilmDatabase
from flask_sqlalchemy import Pagination
from flask_apscheduler import APScheduler

db = FilmDatabase()
db.load_database()
db.create_database()
nname = [""]

app = Flask(__name__)
app.config['SCHEDULER_API_ENABLED'] = True

scheduler = APScheduler()
scheduler.init_app(app)


@scheduler.task('interval', id='savedata', seconds=30)
def save():
    print('save success')
    db.save_database()


@app.route('/')
def index():
    # return render_template('startest.html')
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
        部分电影名 + 部分人名
        
        查找类型名
        
        模糊搜索电影名 + 人名
    '''
    res_list = list()
    filmflag = 0 # 标注从什么地方开始是人
    fname = nowname[0]
    nameres = db.get_film_by_exact_name(fname) # film list

    genre_res = db.get_film_by_genre_name(fname)
    # not empty
    if genre_res:
        res_list = genre_res
        filmflag = len(res_list)
    #empty -> personname
    else:
        person_res = db.get_film_by_person_name(fname)
        # not empty
        if person_res:
            res_list = person_res
            filmflag = len(res_list)
        # empty -> film, part film, part person
        else:
            partname_res = db.get_film_by_part_name(fname)  # name
            partperson_res = db.get_film_by_part_person_name(fname)  #name
            for name in partname_res:
                res_list += db.get_film_by_exact_name(name)
            filmflag = len(res_list)
            res_list += partperson_res

    # dataprocess
    data_list = []
    for i in range(filmflag):
        data_list.append(
            [
                False,  # isperson
                db.database[res_list[i]]  # data
            ]
        )
    for i in range(filmflag, len(res_list)):
        data_list.append(
            [
                True,  # isperson
                res_list[i]  # name
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


@app.route('/ranklist/<name>', methods=['GET', 'POST'])
def ranklist(name=[]):
    data_list = []
    namem = request.args.get('name', None)
    page = request.args.get('page', 1, type=int)
    print(page)
    print(name)
    if namem:
        name = [namem]

    if name == 'score':
        db.resetscore()
        for nm in db.get_filmscoreranklist():
            data_list.append(db.database[nm[0]])
    else:
        db.resetclick()
        for nm in db.get_filmclickranklist():
            data_list.append(db.database[nm[0]])
    # pagination
    limit = 10
    start = (page - 1) * limit
    end = page * limit if len(data_list) > page * limit else len(data_list)

    paginate = Pagination(data_list, page, per_page=10, total=len(data_list), items=data_list[start:end])
    data = paginate.items
    return render_template('ranklist.html', pagename=name, paginate=paginate, data=data, genrelist=db.genredb.keys())


@app.route('/details/<id>', methods=['POST', 'GET'])
def details(id, flag=False):
    # print(flag)
    id = int(id)
    if request.method == 'POST' and flag is False:
        score = float(request.form['getrating']) * 2
        # print(score)
        if score:
            db.database[id].judge_score(score)
            # db.save_database()
        return redirect(url_for('details', id=id, flag=True))
    film = db.database[id]
    db.database[id].add_click()
    # db.save_database()
    data = dict()
    data['film'] = film
    return render_template('details.html', data=data, genrelist=db.genredb.keys())


if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)
