#!/usr/bin/python
#encoding:utf-8
#载入框架
import web
from web import form
#载入数据库操作model（稍后创建）
import model

#URL映射
urls = (
        '/', 'Index',
        '/login', 'Login',
        '/signup','Signup',
        '/logout', 'Logout',
        '/newsubject','Newsubject',
        '/spend/(.*)', 'Spend',
        '/viewsubject/(/d+)', 'Viewsubject',
        '/edit/(/d+)', 'Edit',
        )
app = web.application(urls, globals())
#模板公共变量
t_globals = {
    'datestr': web.datestr,
    'cookie': web.cookies,
}
#指定模板目录，并设定公共模板
render = web.template.render('templates', base='base', globals=t_globals)

class Index:
    def GET(self):
        index_show=model.index_show()
        return render.index(index_show)
#创建登录表单
#login
class Login:
    login_form= form.Form(
                      form.Textbox('username'),
                      form.Password('password'),
                      form.Button('login')
                      )
    def GET(self):
        loginform= self.login_form()
        return render.login(loginform)
    def POST(self):
        login_result= self.login_form()
        if login_result.validates():
            if login_result.d.username == 'admin' and login_result.d.password == 'admin':
                web.setcookie('username', login_result.d.username)
        raise web.seeother('/')
#主页

#sign up
   
class Signup:
    vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
    vemail = form.regexp(r".*@.*", "must be a valid email address")

    signup_form = form.Form(
    form.Textbox("email", vemail, description="E-Mail"),
    form.Textbox("username", description="Username"), 
    form.Password("password", vpass, description="Password"),
    form.Password("password2", description="Repeat password"),
    form.Textbox("sex", description="Sex"),
    form.Button("submit", type="submit", description="Register"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)
    def GET(self):
        # do $:f.render() in the template
        f =self.signup_form()
        return render.signup(f)
    def POST(self):
        f =self.signup_form()
        if not f.validates():
            return render.signup(f)
        else:
            model.sign_up(f.d.username,f.d.email,f.d.password,f.d.sex)
            raise web.seeother('/login')
            # do whatever is required for registration
#newsubject
class Newsubject:
    form = web.form.Form(
                         web.form.Textbox('title',
                         web.form.notnull,
                         size=30,
                         description='Post title: '),
                         web.form.Textarea('content',
                         web.form.notnull,
                         rows=20,
                         cols=40,
                         description='Post content: '),
                         web.form.Button('Post entry'),
                         )
    def GET(self):
        form = self.form()
        return render.newsubject(form)
    def POST(self):
        form = self.form()
        if not form.validates():
            return render.newsubject(form)
        model.new_subject(form.d.title,form.d.content)
        raise web.seeother('/')      

#spend on subject
class Spend:
    form = web.form.Form(
                         web.form.Textbox('spend_time',
                         web.form.notnull,
                         size=30,
                         description='Spend time: '),
                         web.form.Textarea('summary',
                         web.form.notnull,
                         rows=30,
                         cols=80,
                         description='Input summary: '),
                         web.form.Button('submit'),
                         )
    def GET(self):
        form = self.form()
        return render.spend(form)
    def POST(self):
        form = self.form()
        if not form.validates():
            return render.spend(form)
        model.new_spend(form.d.spend_time, form.d.summary)
        raise web.seeother('/')


#退出登录
class Logout:
    def GET(self):
        web.setcookie('username', '', expires=-1)
        raise web.seeother('/')
#定义404错误显示内容
def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.")
    
app.notfound = notfound
#运行
if __name__ == '__main__':
    app.run()