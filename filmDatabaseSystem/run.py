import requests.cookies
from flask import *
from film import Film
from filmdatabase import FilmDatabase
from flask_sqlalchemy import Pagination
from flask_apscheduler import APScheduler
from flask_wtf import *
from User import *
from flask_login import LoginManager
from flask_login import UserMixin, login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


db = FilmDatabase()
db.load_database()
db.create_database()

userdb = Userdatabase()
userdb.load_user()
userdb.create_database()

nname = [""]

app = Flask(__name__)
app.config['SCHEDULER_API_ENABLED'] = True

scheduler = APScheduler()
scheduler.init_app(app)

app.secret_key = '942652464'

login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'login'


def get_user(user_name):
    return userdb.get_user_by_name(user_name)


class User(UserMixin):
    """用户类"""
    def __init__(self, user: SUser):
        self.username = user.username
        self.password_hash = generate_password_hash(user.password)
        self.id = user.keyid

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        if userdb.get_user_by_id(user_id) is None:
            return None
        else:
            return User(userdb.get_user_by_id(user_id))


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)


class LoginForm(FlaskForm):
    """登录表单类"""
    username = StringField('用户名', validators=[DataRequired()], render_kw={"placeholder": "请输入用户名"})
    password = PasswordField('密码', validators=[DataRequired()], render_kw={"placeholder": "请输入密码"})


@app.route('/login/', methods=('GET', 'POST'))  # 登录
def login():
    form = LoginForm()
    emsg = None
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        # print(generate_password_hash(password))
        user_info = get_user(user_name)  # 从用户数据中查找用户记录
        if user_info is None:
            emsg = "用户名或密码密码有误"
        else:
            user = User(user_info)  # 创建用户实体
            if user.verify_password(password):  # 校验密码
                login_user(user)  # 创建用户 Session
                return redirect(request.args.get('next') or url_for('index'))
            else:
                emsg = "用户名或密码密码有误"
    return render_template('login.html', form=form, emsg=emsg)


@app.route('/register', methods=['POST', 'GET'])
def register():
    errormessage = ''
    if request.method == 'POST':
        res = request.form
        name = res['Name']
        password = res['Password']
        passwordrec = res['Passwordrec']
        errormessage = None
        if userdb.get_user_by_name(name):
            errormessage = '用户名已存在'
        elif len(name) > 20 or len(name) == 0:
            errormessage = '用户名不合法'
        elif len(password) > 20 or len(password) < 4:
            errormessage = '请输入4-20位密码'
        elif password != passwordrec:
            errormessage = '两次密码输入不一致'
        else:
            userdb.add_user(name, password)
            return redirect(url_for('login'))
    return render_template('register.html', errormessage=errormessage)


@scheduler.task('interval', id='savedata', seconds=30)
def save():
    print('save success')
    db.save_database()
    userdb.save_user()


@app.route('/')
@login_required
def index():
    # return render_template('startest.html')
    data = {}
    db.resetclick()
    popular = []
    for nm in db.get_filmclickranklist()[:5]:
        popular.append(db.database[nm[0]])
    data['popular'] = popular
    return render_template('index.html', genrelist=db.genredb.keys(), data=data, user=current_user)


@app.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/searchresult', methods=['POST', 'GET'])
def searchresult(nowname=[''], personflag=False):
    if request.method == 'POST':
        res = request.form
        nowname = [res['Name']]
        page = 1
    else:
        namem = request.args.get('nowname', None)
        page = request.args.get('page', 1, type=int)
        personflag = request.args.get('personflag', False, type=bool)
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
    if personflag:
        res_list = db.get_film_by_person_name(fname)
        filmflag = len(res_list)
    else:
        genre_res = db.get_film_by_genre_name(fname)
        if genre_res:
            res_list = genre_res
            filmflag = len(res_list)
        else:
            partname_res = db.get_film_by_part_name(fname)  # name
            partperson_res = db.get_film_by_part_person_name(fname)  #name
            print(partperson_res)
            if len(partname_res) + len(partperson_res) != 0:
                for name in partname_res:
                    res_list += db.get_film_by_exact_name(name)
                filmflag = len(res_list)
                res_list += partperson_res
            else:
                fuzzname_res = db.get_film_by_fuzz_name(fname)
                fuzzperson_res = db.get_film_by_fuzz_person_name(fname)
                for name in fuzzname_res:
                    res_list += db.get_film_by_exact_name(name)
                filmflag = len(res_list)
                res_list += fuzzperson_res

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


@app.route('/famous/<name>', methods=['GET', 'POST'])
def famous(name=[]):
    data_list = []
    namem = request.args.get('name', None)
    page = request.args.get('page', 1, type=int)
    if namem:
        name = [namem]

    db.get_famous()
    for i in db.famouslist:
        data_list.append(db.database[i])
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
        if 'getrating' in request.form.keys():
            score = float(request.form['getrating']) * 2
            if score:
                db.database[id].judge_score(score)
                userdb.get_user_by_name(current_user.username).scoredict[str(id)] = True
            return redirect(url_for('details', id=id, flag=True))
        else:
            db.database[id].comments.insert(0, (current_user.username, request.form['newcomment']))
            return redirect(url_for('details', id=id, flag=True))
    film = db.database[id]
    db.database[id].add_click()
    # recommend
    rec = db.film_recommand(film, 5)
    recommend = []
    for data in rec:
        recommend.append(db.database[data[0]])
    data = dict()
    data['film'] = film
    data['recommend'] = recommend
    displayratingstars = str(id) in userdb.get_user_by_name(current_user.username).scoredict
    return render_template('details.html', data=data, genrelist=db.genredb.keys(), user=current_user, displayratingstars=displayratingstars)


if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)
