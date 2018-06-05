from flask import Flask
from flask_script import Manager


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    app = Flask(__name__)

    from blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app

app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    app.secret_key = "sdfsafsf"
    app.run(debug=False)