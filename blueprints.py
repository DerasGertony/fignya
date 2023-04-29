import flask
from flask import redirect, url_for
from flask import request, jsonify, session
from requests import get
import db_session
from users import User
import base64
import requests
import sys


class mapa:
    def __init__(self):
        self.x = 135
        self.y = 63
        self.spn = (0.005, 0.005)
        self.l = ['sat', 'map', 'skl']
        self.index = 1
        self.pt = ''
        self.params = {}
        self.set_params()
        self.address = ''

    def set_params(self):
        self.params = {
            'll': str(self.x) + ',' + str(self.y),
            'l': str(self.l[self.index % 3]),
            'spn': str(self.spn[0]) + ',' + str(self.spn[1]),
            'pt': self.pt
        }

    def request(self):
        search_api_server = 'http://static-maps.yandex.ru/1.x/'
        response = requests.get(search_api_server, params=self.params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        return response

    def change_spn(self, x, y):
        if 0 <= x < 20 and 0 <= y < 20:
            self.spn = (x, y)
            self.set_params()
            return self.request()
        return 0

    def change_coord(self, way):
        if way == 0 and -170 < self.x < 170:
            self.x += self.spn[0]
        if way == 1 and -170 < self.x < 170:
            self.x -= self.spn[0]
        if way == 2 and -80 < self.y < 80:
            self.y -= self.spn[1]
        if way == 3 and -80 < self.y < 80:
            self.y += self.spn[1]
        self.set_params()
        return self.request()

    def change_type(self):
        self.index += 1
        self.set_params()
        return self.request()

    def find(self, text):
        global text_output, posting
        search_api_server = "http://geocode-maps.yandex.ru/1.x/"
        params = {
            'geocode': text,
            'format': 'json',
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b'
        }
        response = requests.get(search_api_server, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        json_response = response.json()
        try:
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.tc = toponym_coodrinates
            self.text_output = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['formatted']
            try:
                post = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']

                if posting:
                    text_output += " " + post
            except:
                pass
            toponym_coodrinates = toponym_coodrinates.split()
            self.x = float(toponym_coodrinates[0])
            self.y = float(toponym_coodrinates[1])
            self.pt = f'{self.x},{self.y},pm2ntm'
        except:
            pass
        self.set_params()
        return self.request()

    def clear_all(self):
        global text_output
        self.pt = ''
        text_output = ''
        return self.request()

    def add_post(self):
        global posting
        posting = not posting
        return self.request()


map1 = mapa()
blueprint = flask.Blueprint('users', __name__, template_folder='templates')


@blueprint.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Даров</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <div class="form-group">
                                        <label for="form-check">Кто вы?</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="enter" id="log" value="log" checked>
                                          <label class="form-check-label" for="log">
                                            Я уже Смешарик(войти)
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="enter" id="reg" value="reg">
                                          <label class="form-check-label" for="reg">
                                            Хочу стать смешариком(зарегистрироваться)
                                          </label>
                                        </div>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Пошли</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        return redirect(f'http://127.0.0.1:5000/{request.form["enter"]}', code=302)


@blueprint.route('/log', methods=['POST', 'GET'])
def log():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Форма для входа</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                    <button type="submit" class="btn btn-primary">Войти</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_sess = db_session.create_session()
        for user in db_sess.query(User).filter(User.email == email):
            if user.password == password:
                session['user_id'] = user.id
                return redirect(f'http://127.0.0.1:5000/user/{user.id}', code=302)
            else:
                return redirect('http://127.0.0.1:5000/log', code=302)
        return redirect('http://127.0.0.1:5000/log', code=302)


# import requests
# def request(self):
#    search_api_server = 'http://static-maps.yandex.ru/1.x/'
#    response = requests.get(search_api_server, params=self.params)
#    if not response:
#      print("Ошибка выполнения запроса:")
#      print("Http статус:", response.status_code, "(", response.reason, ")")
#      sys.exit(1)
#    return response
# map1.request().content



#raw_img = repr(img)
#"<img src='data:image/png;base64,{}'/>".format( base64.b64encode(raw_img) )



@blueprint.route('/user/<int:user_id>', methods=['POST', 'GET'])
def profile(user_id):
    if request.method == 'GET':
        db_sess = db_session.create_session()
        user = db_sess.query(User).all()[user_id - 1]
        if user_id == session['user_id']:
            x = base64.b64encode(user.image)
            print(x)

            # str_equivalent_image = base64.b64encode(bytes(x, 'utf-8')).decode()
            return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>{user.name}</title>
                          </head> 
                    <body>
                        <div>
                            <form class="login_form" method="post">
                                <input type="city" class="form-control" id="city" placeholder="" name='city'>
                                <button type="submit" class="btn btn-primary">go</button>   
                            </form>
                        </div>
                    <div class="row py-5 px-4">
                        <div class="col-md-5 mx-auto"> <!-- Profile widget -->
                            <div class="bg-white shadow rounded overflow-hidden">
                                <div class="px-4 pt-0 pb-4 cover">
                                    <div class="media align-items-end profile-head">
                                        <div class="profile mr-3">
              <img src="data:image/png;base64, {x}b />" alt="Red dot" /></div>
                                        <div class="media-body mb-5 text-white"><h4 class="mt-0 mb-0"{user.name}</h4>
                                            <p class="small mb-4"><i class="fas fa-map-marker-alt mr-2"></i>{user.name}</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="px-4 py-3"><h5 class="mb-0">About</h5>
                                    <div class="p-4 rounded shadow-sm bg-light"><p class="font-italic mb-0">
                                        {user.about}</p>
                                </div>
                                <div class="py-4 px-4">
                                    <div class="d-flex align-items-center justify-content-between mb-3"><h5
                                            class="mb-0">Levels</h5><a href="#" class="btn btn-link text-muted">Show
                                        all</a></div>
                                    <div class="row">
                                        <div class="col-lg-6 mb-2 pr-lg-1"<img src="https://images.unsplash.com/photo-1475724017904-b712052c192a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80" alt="" class="img-fluid rounded shadow-sm"></div>
                                        <div class="col-lg-6 mb-2 pl-lg-1"><img src="https://images.unsplash.com/photo-1475724017904-b712052c192a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80" alt="" class="img-fluid rounded shadow-sm"></div>
                                        <div class="col-lg-6 pr-lg-1 mb-2"><img src="https://images.unsplash.com/photo-1475724017904-b712052c192a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80" alt="" class="img-fluid rounded shadow-sm"></div>
                                        <div class="col-lg-6 pl-lg-1"><img src="https://images.unsplash.com/photo-1475724017904-b712052c192a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80" alt="" class="img-fluid rounded shadow-sm">></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    </body>
            '''
        else:
            return '0'
    elif request.method == 'POST':
        x = request.form['city']
        session['picture'] = x
        return redirect("http://127.0.0.1:5000/game", code=302)

        # TODO: here add static-map-api
        # s = ''
        # if user.id == session['user_id']:
        #     s = 'img1'
        # else:
        #     s = 'img2'
        # <class=f"{s}" img hidden src="landscape.jpg" alt="">
        # img1{
        #   display: block;
        # }
        # img2{
        #   display: none;
        # }


@blueprint.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Регистрация в Online-RogueLike</h1>
                            <div>
                                <form class="login_form" method="post" enctype="multipart/form-data">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                    <div class="form-group">
                                        <label for="nickname">Nickname</label>
                                        <textarea class="form-control" id="nickname" rows="1" name="nickname"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="about">Немного о себе</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group" >
                                        <label for="photo">Add avatar</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <button type="submit" class="btn btn-primary">Register</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        f = f.read()
        print(str(f))
        db_sess = db_session.create_session()

        user = User(name=request.form['nickname'],
                    about=request.form['about'],
                    email=request.form['email'],
                    image=str(f),
                    password=request.form['password'],
                    levels='',
                    items='')
        db_sess.add(user)
        db_sess.commit()
        return redirect("http://127.0.0.1:5000/log", code=302)


@blueprint.route('/game', methods=['POST', 'GET'])
def game():
    y = base64.b64encode(map1.find(str(session['picture'])).content)
    return f'''<!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet"
                  href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                  integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                  crossorigin="anonymous">
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>
            <title>Пример формы</title>
        </head>
        <body>
        <h1>Точка назначения</h1>
        <h2>{map1.text_output}</h2>
        <h2>{map1.tc}</h2>
        <div>
            <div>
            <img src="data:image/png;base64, {(str(base64.b64encode(map1.find(str(session['picture'])).content)))[2:-1]}" alt="Red dot" />
            </div>
        </div>
        </body>
        </html>'''
