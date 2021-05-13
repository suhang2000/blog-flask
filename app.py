from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from Blog import Blog
from User import User
from util import ResData

app = Flask(__name__)
CORS(app, supports_credentials=True)

"""
接口说明：
1.返回的是json数据
2.结构如下
{
    code： 200, # 非200即错误
    data： # 数据位置，一般为数组
    message： '对本次请求的说明'
}
"""


@app.route('/api/login/user', methods=['GET'])
def login():
    userid = ''
    password = ''
    print('request args:', request.args)
    if request.args is not None:
        data = request.args.to_dict()
        userid = data.get('user_id')
        password = data.get('user_password')
    user = User()
    result = user.select_user(userid, password)
    # print(result)
    if result:
        resData = ResData(200, userid, 'login succeed')
    else:
        resData = ResData(400, '', 'login failed')
    return jsonify(resData)


@app.route('/api/register/user', methods=['POST'])
def register():
    resData = ResData(400, '', 'register failed')
    data = request.get_data()
    if data is not None:
        data = json.loads(data)
        print('data: ', data)
        user = User()
        result = user.insert_user(data)
        if result:
            resData = ResData(200, '', 'register succeed')
    return jsonify(resData)


@app.route('/api/resetpwd/user', methods=['POST'])
def reset_user_pwd():
    resData = {
        "code": 400,
        "data": '',
        "message": 'register failed'
    }
    data = request.get_data()
    if data is not None:
        data = json.loads(data)
        print('data: ', data)
        del data['phone_number']
        print(data)
        user = User()
        result = user.update_user(data)
        if result:
            resData = ResData(200, '', 'register succeed')
    return jsonify(resData)


if __name__ == '__main__':
    app.run(debug=True)
