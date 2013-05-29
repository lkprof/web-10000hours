#encoding:utf-8
#载入框架
import web
from web import form
#载入数据库操作model（稍后创建）
import model

#URL映射
urls = (
        '/', 'Index',
        '/home','Home'
        '/signup','Signup'
        '/login', 'Login',
        '/logout', 'Logout',
        '/newsubject','Newsubject'
        '/spend', 'Spend'


        '/view/(/d+)', 'View',
        '/new', 'New',
        '/delete/(/d+)', 'Delete',
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

#创建登录表单
login = form.Form(
                      form.Textbox('email'),
                      form.Password('password'),
                      form.Button('login')
                      )
#home,login类
class Index:
    def GET(self):
        login_form = login()
        index_show = model.index_show()
        return render.index(index_show, login_form)
    def POST(self):
        login_form = login()
        results=model.find_user()
        if login_form.validates():
            if results.email==login_form.d.email:
                web.setcookie('username', results.username)
        raise web.seeother('/')
#sign up
class Signup:
    vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
    vemail = form.regexp(r".*@.*", "must be a valid email address")

    singup_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Textbox("email", vemail, description="E-Mail"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", description="Repeat password"),
    form.Textbox("sex", description="Sex"),
    form.Button("submit", type="submit", description="Register"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)
    def GET(self):
        # do $:f.render() in the template
        f = signup_form()
        return render.Signup(f)

    def POST(self):
        f = signup_form()
        if not f.validates():
            return render.Signup(f)
        else:
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
                         rows=30,
                         cols=80,
                         description='Post content: '),
                         web.form.Button('Post entry'),
                         )
    def GET(self):
        form = self.form()
        return render.new(form)
    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_subject(form.d.title, form.d.content)
        raise web.seeother('/')      

#spend on subject
class Spend:
    def 


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