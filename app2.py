from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import certifi

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.qlgvb.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta_chapter1


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index3.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 되었습니다.'})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup/index3.html')
def index3():
    return render_template('index3.html')


@app.route('/index4.html')
def index4():
    return render_template('index4.html')


@app.route("/review", methods=["POST"])
def review_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        user_info = db.users.find_one({"username": payload["id"]})
        store_receive = request.form['store_give']
        localname_receive = request.form['localname_give']
        star_receive = request.form['star_give']
        address_receive = request.form['address_give']
        menu_receive = request.form['menu_give']
        comment_receive = request.form['comment_give']
        image_receive = request.form['image_give']

        review_list = list(db.project01.find({}, {'_id': False}))
        count = len(review_list) + 1

        doc = {
            'num': count,
            'store': store_receive,
            'menu': menu_receive,
            'localname': localname_receive,
            'star': star_receive,
            'comment': comment_receive,
            'image': image_receive,
            'address': address_receive,
            'username': user_info['username']

        }
        db.project01.insert_one(doc)

        return jsonify({'result': 'success', 'msg': '등록 완료!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))


# <!-- 검색 기능 구현 -->#
@app.route('/search', methods=['GET'])  # /search로 키워드를 받아 빵집 이름과 일치 결과를 찾아냅니다.
def search_get():
    doc = []  # 검색을 마친 자료가 들어갈 배열입니다.
    store_receive = request.args.get('store_give')  # Ajax에서 store_give로 보낸 데이터를 받습니다.
    stores = list(db.project01.find({}, {'_id': False}))  # 빵집의 전체 목록을 stores 변수로 받아옵니다.
    for store in stores:
        if store_receive in store['store']:  # store_receive로 받은 검색어를 찾아봅니다.
            doc.append(store)  # 일치하는 빵집을 doc 배열에 집어넣습니다.
    search_list = {'search_list': doc}  # API로 전달할 수 있는 자료에 배열 형태는 없으므로, 딕셔너리로 만들어야 합니다.
    return jsonify({'search_list': search_list, 'msg': '검색완료!'})


@app.route("/project01", methods=["GET"])
def project01_get():
    project01_list = list(db.project01.find({}, {'_id': False}))
    return jsonify({'projects01': project01_list})


# index_sub로 연결하면서 mnt_no 데이터를 전송
@app.route('/index5')
def index5():
    num_receive = request.args.get('num_give')
    return render_template('index5.html', num=num_receive)


@app.route('/index5_show', methods=['GET'])
def show_index5():
    num_receive = request.args.get('num_give')
    reviews = db.project01.find_one({'num': int(num_receive)}, {'_id': False})
    return jsonify({'review_list': reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
