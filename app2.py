from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.xzxzt.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index3.html')

@app.route("/project01", methods=["POST"])
def project01_post():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    menu_receive = request.form['menu_give']
    comment_receive = request.form['comment_give']


    doc = {
        'name':name_receive,
        'address':address_receive,
        'menu': menu_receive,
        'comment': comment_receive
    }
    db.project01.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

# @app.route("/bucket/done", methods=["POST"])
# def bucket_done():
#     sample_receive = request.form['sample_give']
#     print(sample_receive)
#     return jsonify({'msg': 'POST(완료) 연결 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    return jsonify({'msg': '방문해주셔서 감사합니다.!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)