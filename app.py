from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from Blog import Blog
from User import User

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
        resData = {
            "code": 200,
            "data": userid,
            "message": 'login succeed'
        }
    else:
        resData = {
            "code": 400,
            "data": '',
            "message": 'login failed'
        }
    return jsonify(resData)


if __name__ == '__main__':
    app.run(debug=True)
