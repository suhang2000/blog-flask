from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from Blog import Blog
from User import User
from Admin import Admin
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


@app.route('/api/login/admin', methods=['GET'])
def admin_login():
    admin_id = ''
    admin_password = ''
    print('request args:', request.args)
    if request.args is not None:
        data = request.args.to_dict()
        admin_id = data.get('admin_id')
        admin_password = data.get('admin_password')
    admin = Admin()
    result = admin.select_admin(admin_id, admin_password)
    # print(result)
    if result:
        resData = ResData(200, admin_id, 'login succeed')
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
    resData = ResData(400, '', 'register failed')
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


@app.route('/api/select/user', methods=['POST'])
def selectuser():
    data = request.get_data()
    data = json.loads(data)
    print("data:", data)
    user = User()
    result = user.select_user_with_conditions(data)
    resData = ResData(200, result, 'select succeed')
    return jsonify(resData)


@app.route('/api/select/user/page', methods=['POST'])
def selectuserbypage():
    pagesize = 2
    datas = request.get_data()
    datas = json.loads(datas)
    data = {}
    for k, v in datas.items():
        if k != 'page':
            data[k] = v
    print(data)
    page = int(datas['page']) - 1
    user = User()
    result = user.select_user_with_conditions(data)
    total = int(len(result) / pagesize) + 1
    tempresult = []
    print(result)
    if page * pagesize > len(result):
        result = ''
    else:
        pageend = 0
        if (page + 1) * pagesize > len(result):
            pageend = len(result)
        else:
            pageend = (page + 1) * pagesize
        i = page * pagesize
        j = 0
        while i < pageend:
            tempresult.append(result[i])
            i = i + 1
        result = tempresult
    result.append({'total': total})
    print(result)
    resData = ResData(200, result, 'select succeed')
    return jsonify(resData)


@app.route('/api/fix/user', methods=['POST'])
def fixuser():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        uid = data['user_id']
        u_id = str(uid)
        data['user_id'] = u_id
        user = User()
        result = user.select_user_with_conditions({'user_id': data['user_id']})
        print(data)
        if len(result) == 1:
            result = user.fix_user_information(data)
            if result == 1:
                resData = ResData(200, '', 'fix succeed')
            else:
                resData = ResData(200, '', 'fix failed')
        else:
            resData = ResData(400, '', 'select failed')
        return jsonify(resData)


@app.route('/api/select/article/page', methods=['POST'])
def selectarticlebypage():
    pagesize = 2
    datas = request.get_data()
    datas = json.loads(datas)
    data = {}
    for k, v in datas.items():
        if k != 'page':
            data[k] = v
    print(data)
    page = int(datas['page']) - 1
    blog = Blog()
    result = blog.select_blog_with_conditions(data)
    total = int(len(result) / pagesize) + 1
    tempresult = []
    print(result)
    if page * pagesize > len(result):
        result = ''
    else:
        pageend = 0
        if (page + 1) * pagesize > len(result):
            pageend = len(result)
        else:
            pageend = (page + 1) * pagesize
        i = page * pagesize
        j = 0
        while i < pageend:
            tempresult.append(result[i])
            i = i + 1
        result = tempresult
    result.append({'total': total})
    print(result)
    resData = ResData(200, result, 'select succeed')
    return jsonify(resData)


@app.route('/api/fix/article', methods=['POST'])
def fixarticle():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        uid = data['blog_id']
        u_id = str(uid)
        data['blog_id'] = u_id
        blog = Blog()
        result = blog.select_blog_with_conditions({'blog_id': data['blog_id']})
        print(data)
        if len(result) == 1:
            result = blog.fix_blog_information(data)
            if result == 1:
                resData = ResData(200, '', 'fix succeed')
            else:
                resData = ResData(200, '', 'fix failed')
        else:
            resData = ResData(400, '', 'select failed')
        return jsonify(resData)

@app.route('/api/delete/article', methods=['POST'])
def deletearticle():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        uid = data['blog_id']
        u_id = str(uid)
        data['blog_id'] = u_id
        blog = Blog()
        result = blog.select_blog(data['blog_id'])
        print(data)
        if result == True:
            result = blog.delete_blog(data['blog_id'])
            if result == True:
                resData = ResData(200, '', 'delete succeed')
            else:
                resData = ResData(400, '', 'delete failed')
        else:
            resData = ResData(400, '', 'delete failed')
        return jsonify(resData)

if __name__ == '__main__':
    app.run(debug=True)
