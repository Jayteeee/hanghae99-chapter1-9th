from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import certifi

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.3jj7o.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('prac4.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('prac4.html', msg=msg)

@app.route('/user/<username>')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('prac4.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

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

@app.route('/sign_in/index3.html')
def index3():
    return render_template('index3.html')

@app.route('/index4.html')
def index4():
    return render_template('index4.html')

@app.route("/review", methods=["POST"])
def review_post():
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
        'num':count,
        'store':store_receive,
        'menu':menu_receive,
        'localname': localname_receive,
        'star': star_receive,
        'comment': comment_receive,
        'image': image_receive,
        'address': address_receive

    }
    db.project01.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route("/project01", methods=["GET"])
def project01_get():
    project01_list = list(db.project01.find({}, {'_id': False}))
    return jsonify({'projects01': project01_list})

# index_sub로 연결하면서 mnt_no 데이터를 전송
@app.route('/index5')
def index5():
    num_receive = request.args.get('num_give')
    return render_template('index5.html', num = num_receive)

@app.route('/index5_show', methods=['GET'])
def show_index5():
    num_receive = request.args.get('num_give')
    reviews = db.project01.find_one({'num':int(num_receive)},{'_id':False})
    return jsonify({'review_list':reviews})

# @app.route("/review_show", methods=["GET"])
# def show_review(store_num):
#     num = db.project01.find_one({'num': int(store_num)}, {'_id': False})
#     return jsonify({'num': num})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)