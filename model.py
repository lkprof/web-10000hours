 #!/usr/bin/python
#encoding:utf-8
import web
import datetime
#数据库连接
db = web.database(dbn = 'mysql', db = 'forprojects', user = 'lkprof', pw = 'dlnu')
def find_user():
    try:
        return db.query("select username from users where email=$email and password=$password")
    except notfinduser:
        return None
#sign up
def sign_up(f):
    db.insert('users',
        name=f.username,
        email=f.email,
        password=f.password,
        sex=f.sex)

#new subject
def new_subject(title, text):
    db.insert('subjects',
        title = title,
        content = text,
        posted_on = datetime.datetime.utcnow())


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