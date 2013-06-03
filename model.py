#!/usr/bin/python
#encoding:utf-8
import web
import datetime
#数据库连接
db = web.database(dbn = 'mysql', db = 'forprojects', user = 'lkprof', pw = 'dlnu')
#
def find_user(username,password):
    try:
        return db.query("select username from users where username=$username and password=$password")
    except notfinduser:
        return None
#sign up
def sign_up(username,email,password,sex):
    db.insert('users',
        name=username,
        email=email,
        password=password,
        sex=sex)

#new subject
def new_subject(title,content):
    db.insert('subjects',
        title = title,
        content = content,
        posted_on = datetime.datetime.utcnow())
#首页展示
def index_show():
    return db.query("select subjects.title,subjects.subject_id,subjects.posted_on,spend_time from spend_on_subject,\
        subjects,users where users.user_id=subjects.subject_user_id and \
        subjects.subject_id=spend_on_subject.spend_subject_id")

#根据title分组，获得title名称
def get_title(username):
    return db.query("select title from spend_on_subject,\
        subjects,users where users.name=$username and users.user_id=subjects.user_id and \
        subjects.subject_id=spend_on_subject.spend_subject_id group by title")

#输入新的时间投入
def new_spend(spend_time,summary):
    db.insert('spend_on_subject',
        spend_time=spend_time,
        summary=summary,
        posted_on=datetime.datetime.utcnow())


#获取所有文章
def get_posts():
    return db.select('entries', order = 'id DESC')
    
#获取文章内容
def get_post(id):
    try:
        return db.query("SELECT * FROM entries WHERE id=$id")
    except IndexError:
        return None

#删除文章
def del_post(id):
    db.delete('entries', where= "id=$id")
    
#修改文章
def update_post(id, title, text):
    db.update('entries',
        where = 'id = $id',
        vars = locals(),
        title = title,
        content = text)