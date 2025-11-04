from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# create appimizi temsil eder
db = SQLAlchemy()  # SQLalchemy ile bir db örneği çağırdık


def createApp():
    app = Flask(__name__)  # FLASK Appimizi oluşturudğumuz kısmı artık buraya aldık
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:0606@localhost:5432/ecommerce"
    )

    db.init_app(app)

    return app
