from flask import Flask, jsonify, request
from markupsafe import escape
from flask_cors import CORS
import json
from itsdangerous import URLSafeTimedSerializer
from Blog import Blog
from Comments import Comments
from User import User
from Admin import Admin
from Report import Report
from util import ResData
from sensitiveDetection import GFW
from flask_mail import Mail, Message
from config import MAIL_CONFIG
import os

app = Flask(__name__)
app.config.update(MAIL_CONFIG)
mail = Mail(app)
print(os.getcwd())
gfw = GFW()

with open(os.path.join(os.path.dirname(__file__), 'sensitivewords.txt'), "r") as f:
    lines = f.read().splitlines()
    gfw.set(lines)
CORS(app, supports_credentials=True)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=300):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


@app.route('/api/sendEmail/', methods=['POST'])
def send_mail():
    data = request.get_data()
    if data is not None:
        data = json.loads(data)
        print(data)
        email = data.get('email')
        print(email)
        user = User()
        if user.get_user_info_by_email(email):
            msg = Message("验证密码", sender=app.config["MAIL_USERNAME"], recipients=[email])
            token = generate_confirmation_token(email)
            msg.body = "您正在重置博客密码\nhttp://127.0.0.1:5000/api/verifyToken/{}".format(token)
            print(msg)
            mail.send(msg)
            return ResData(200, '', '请在五分钟内到邮箱重置密码')
        else:
            return ResData(400, '', '邮箱未注册!')


@app.route('/api/verifyToken/<token>')
def verify_token(token):
    email = confirm_token(token)
    user = User()
    if email:
        result = user.reset_password(email)
        if result:
            return ResData(200, '', '您的密码重置为123456，请尽快修改密码')
        else:
            return ResData(400, '', '密码修改失败！')


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


@app.route('/api/login/user', methods=['POST'])
def login():
    username = ''
    user_password = ''
    data = request.get_data()
    if data is not None:
        data = json.loads(data)
        username = data.get('username')
        user_password = data.get('user_password')
    user = User()
    result = user.select_user(username, user_password)
    if result:
        resData = ResData(200, username, '登录成功')
    else:
        resData = ResData(400, '', '登录失败')
    print(result)
    return jsonify(resData)


@app.route('/api/login/admin', methods=['post'])
def admin_login():
    admin_id = ''
    admin_password = ''
    data = request.get_data()
    print(data)
    if data is not None:
        data = json.loads(data)
        print(data)
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
    data = request.get_data()
    if data is not None:
        data = json.loads(data)
        print('data: ', data)
        user = User()
        user_info = user.get_user_info_by_name(data.get('username'))
        print(user_info)
        if user_info:
            resData = ResData(400, '', '用户已存在')
        elif user.get_user_info_by_email(data.get('email')):
            resData = ResData(400, '', '邮箱已被占用')
        else:
            result = user.insert_user(data)
            if result:
                resData = ResData(200, '', '注册成功')
    return jsonify(resData)


@app.route('/api/home/user/<username>')
def getUserInfo(username):
    username = escape(username)
    user = User()
    userInfo = user.getInfoByUsername(username)
    if userInfo['user_password']:
        userInfo.pop('user_password')
    resData = ResData(200, userInfo, 'success')
    print(resData)
    return jsonify(resData)


@app.route('/api/home/user/info', methods=['POST'])
def resetUserInfo():
    resData = ResData(400, '', 'failed')
    data = request.get_data()
    if data is not None:
        data = json.loads(data)
        print('user info: ', data)
        user = User()
        if user.update_user_info(data):
            resData = ResData(200, '', 'success')
    return jsonify(resData)


@app.route('/api/home/user/avatar', methods=['POST'])
def changeAvatar():
    resData = ResData(400, '', 'failed')
    data = request.get_data()
    if data is not None:
        data = json.loads(data)
        print('avatar: ', data)
        username = data['username']
        avatar = data['profile_photo']
        user = User()
        if user.changephoto_byname(avatar, username):
            resData = ResData(200, '', 'success')
    return jsonify(resData)

@app.route('/api/resetpwd/user', methods=['POST'])
def reset_user_pwd():
    data = request.get_data()
    if data is not None:
        data = json.loads(data)
        print('data: ', data)
        user = User()
        if user.select_user(data.get('username'), data.get('password_now')):
            user_info = user.get_user_info_by_name(data.get('username'), "user_id")
            print(user_info['user_id'])
            del data['password_now']
            print(data)
            result = user.update_user(data, user_info['user_id'])
            resData = ResData(200, '', '密码修改成功')
        else:
            resData = ResData(400, '', '用户名或密码错误')
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
    pagesize = 10
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
    total = int(len(result))  # int(len(result) / pagesize) + 1
    tempresult = []
    # print(result)
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
    # print(result)
    resData = ResData(200, result, 'select succeed')
    return jsonify(resData)


@app.route('/api/add/article', methods=['POST'])
def addarticle():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        for k, v in data.items():
            if (len(gfw.check(str(v))) > 0):
                resData = ResData(400, '', '文本中存在敏感词')
                return jsonify(resData)
        blog = Blog()
        # print(data)
        result = blog.insert_blog(data)
        if result == 1:
            resData = ResData(200, '', '添加成功')
        else:
            resData = ResData(400, '', '数据库侧出现错误')
        return jsonify(resData)


@app.route('/api/fix/article', methods=['POST'])
def fixarticle():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        for k, v in data.items():
            if (len(gfw.check(str(v))) > 0):
                resData = ResData(400, '', '文本中存在敏感词')
                return jsonify(resData)
        uid = data['blog_id']
        u_id = str(uid)
        data['blog_id'] = u_id
        blog = Blog()
        result = blog.select_blog_with_conditions({'blog_id': data['blog_id']})
        # print(data)
        if len(result) == 1:
            result = blog.fix_blog_information(data)
            if result == 1:
                resData = ResData(200, '', '修改成功')
            else:
                resData = ResData(400, '', '数据库侧出现错误')
        else:
            resData = ResData(400, '', '数据库侧不存在该博客')
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
                resData = ResData(200, '', '删除成功')
            else:
                resData = ResData(400, '', '数据库侧出现错误')
        else:
            resData = ResData(400, '', '数据库侧不存在该博客')
        return jsonify(resData)


@app.route('/api/userInfo_select', methods=['GET'])
def select_byname():
    uname = ''
    if request.args is not None:
        data = request.args.to_dict()
        uname = data.get('username')
    user = User()
    user = user.select_byname(uname)
    resdata = {
        "code": 200,
        "data": user,
        "message": 'success'
    }
    return jsonify(resdata)


@app.route('/api/changeusername', methods=['GET'])
def select_user_byname():
    newname = ''
    uname = ''
    print('request args:', request.args)
    if request.args is not None:
        data = request.args.to_dict()
        newname = data.get('value')
        uname = data.get('username')
    user = User()
    result = user.select_user_byname(newname)
    if result == True:
        resdata = ResData(400, '', '已存在该昵称')
    else:
        result1 = user.changename_byname(newname, uname)
        if result1 == True:
            resdata = {
                "code": 200,
                "data": '',
                "message": '请用新的用户名登陆'
            }
        else:
            print(998)
    return jsonify(resdata)


@app.route('/api/changegender', methods=['GET'])
def changegender():
    newgender = ''
    uname = ''
    print('request args:', request.args)
    if request.args is not None:
        data = request.args.to_dict()
        newgender = data.get('value')
        uname = data.get('username')
    user = User()
    result = user.changegender_byname(newgender, uname)
    print(result)
    if result == True:
        user = user.select_byname(uname)
        resdata = {
            "code": 200,
            "data": user,
            "message": '修改成功'
        }
    else:
        resdata = {
            "code": 400,
            "data": '',
            "message": '请输入"F" 或 "M" '
        }
    return jsonify(resdata)


@app.route('/api/changenum', methods=['GET'])
def changenum():
    newnum = ''
    uname = ''
    print('request args:', request.args)
    if request.args is not None:
        data = request.args.to_dict()
        newnum = data.get('value')
        uname = data.get('username')
    user = User()
    result = user.changenum_byname(newnum, uname)

    if result == True:
        user = user.select_byname(uname)
        resdata = {
            "code": 200,
            "data": user,
            "message": '修改成功'
        }
    else:
        resdata = {
            "code": 400,
            "data": '',
            "message": '请输入正确的11位的电话号码 '
        }
    return jsonify(resdata)


@app.route('/api/changepsd', methods=['GET'])
def changepsd():
    newpsd = ''
    uname = ''
    print('request args:', request.args)
    if request.args is not None:
        data = request.args.to_dict()
        newpsd = data.get('value')
        uname = data.get('username')
    user = User()
    result = user.changepsd_byname(newpsd, uname)

    if result == True:
        resdata = {
            "code": 200,
            "data": '',
            "message": '请用新的密码登陆'
        }
    else:
        resdata = {
            "code": 400,
            "data": '',
            "message": '修改密码失败'
        }
    return jsonify(resdata)


@app.route('/api/changephoto', methods=['GET'])
def changephoto():
    newphoto = ''
    uname = ''
    print('request args:', request.args)
    if request.args is not None:
        data = request.args.to_dict()
        newphoto = data.get('photo')
        print(newphoto)
        uname = data.get('username')
    user = User()
    result = user.changephoto_byname(newphoto, uname)

    if result == True:
        user = user.select_byname(uname)
        resdata = {
            "code": 200,
            "data": user,
            "message": '更换成功'
        }
    else:
        resdata = {
            "code": 400,
            "data": '',
            "message": '修改图片失败'
        }
    return jsonify(resdata)


@app.route('/api/select/admin', methods=['GET'])
def admin_select():
    admin_id = ''
    print('request args:', request.args)
    if request.args is not None:
        data = request.args.to_dict()
        admin_id = data.get('admin_id')
    admin = Admin()
    result = admin.select_admin_without_password(admin_id)
    # print(result)
    if len(result) == 1:
        resData = ResData(200, result, 'fetch succeed')
    else:
        resData = ResData(400, '', 'fetch failed')
    return jsonify(resData)


@app.route('/api/fix/admin', methods=['POST'])
def fixadmin():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        adminid = data['admin_id']
        admin_id = str(adminid)
        data['admin_id'] = admin_id
        admin = Admin()
        result = admin.select_admin_without_password(adminid)
        print(data)
        if len(result) == 1:
            result = admin.fix_admin_information(data)
            if result == 1:
                resData = ResData(200, '', 'Fix succeed! please login with your new password!')
            else:
                resData = ResData(200, '', 'Fix failed! There must be some problems with our back end.')
        else:
            resData = ResData(400, '', 'We cannot certify witch account you are fixing.')
        return jsonify(resData)


@app.route('/api/delete/user', methods=['POST'])
def deleteuser():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        user_id = data['user_id']
        user_id = str(user_id)
        # print(user_id)
        user = User()
        result = user.delete_user_with_id(user_id)
        if result == 1:
            resData = ResData(200, '', 'Delete success!')
            return jsonify(resData)
        else:
            resData = ResData(200, '', 'Delete failed!')
            return jsonify(resData)


@app.route('/api/select/report/page', methods=['POST'])
def selectreportbypage():
    pagesize = 10
    datas = request.get_data()
    datas = json.loads(datas)
    data = {}
    for k, v in datas.items():
        if k != 'page':
            data[k] = v
    print(data)
    page = int(datas['page']) - 1
    report = Report()
    result = report.select_report_with_conditions(data)
    total = int(len(result))  # int(len(result) / pagesize) + 1
    tempresult = []
    # print(result)
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
    # print(result)
    resData = ResData(200, result, 'select succeed')
    return jsonify(resData)


@app.route('/api/delete/report', methods=['POST'])
def deletereport():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        blog_id = data['blog_id']
        blog_id = str(blog_id)
        # print(user_id)
        report = Report()
        result = report.delete_report_with_id(blog_id)
        resData = ResData(200, '', 'Delete success!')
        return jsonify(resData)


@app.route('/api/select/comments/page', methods=['POST'])
def selectcommentsbypage():
    pagesize = 2
    datas = request.get_data()
    datas = json.loads(datas)
    data = {}
    for k, v in datas.items():
        if k != 'page':
            data[k] = v
    print(data)
    page = int(datas['page']) - 1
    comments = Comments()
    result = comments.select_comment_with_conditions(data)
    total = int(len(result))  # int(len(result) / pagesize) + 1
    tempresult = []
    # print(result)
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
    # print(result)
    resData = ResData(200, result, 'select succeed')
    return jsonify(resData)


@app.route('/api/add/comment', methods=['POST'])
def addcomment():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        for k, v in data.items():
            if (len(gfw.check(str(v))) > 0):
                resData = ResData(400, '', '文本中存在敏感词')
                return jsonify(resData)
        comments = Comments()
        # print(data)
        result = comments.insert_comment(data)
        if result == 1:
            resData = ResData(200, '', '评论成功')
        else:
            resData = ResData(400, '', '数据库侧出现错误')
        return jsonify(resData)


@app.route('/api/delete/comment', methods=['POST'])
def deletecomment():
    if request.args is not None:
        data = request.get_data()
        data = json.loads(data)
        uid = data['comment_id']
        u_id = str(uid)
        data['comment_id'] = u_id
        comments = Comments()
        result = comments.select_comment(data['comment_id'])
        print(data)
        if result == True:
            result = comments.delete_comment(data['comment_id'])
            if result == True:
                resData = ResData(200, '', '删除成功')
            else:
                resData = ResData(400, '', '数据库侧出现错误')
        else:
            resData = ResData(400, '', '数据库侧不存在该评论')
        return jsonify(resData)


@app.route('/api/report/article', methods=['POST'])
def report():
    data = request.get_data()
    data = json.loads(data)
    # print(data)
    report = Report()
    result = report.insert_report(data)
    if result == 1:
        resData = ResData(200, '', 'Report success!')
        return resData
    else:
        resData = ResData(200, '', 'Report failed!')
        return resData


if __name__ == '__main__':
    app.run(debug=True)
