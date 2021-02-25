from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from configs.configurations import Development, Testing, Production

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)



@app.route('/')
def index():
    return render_template("/landing/index.html")

@app.route('/admin')
def admin():
    return render_template("/admin/admin.html")


if __name__ =="__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)
