from flask import Flask, url_for, render_template, request, redirect
from .models import db, Question, Answer
from flask_migrate import Migrate

import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np
import pandas as pd

def create_app():
    app = Flask(__name__)
    
    # app.config["SECRET_KEY"] ="123456"
    # app.config ["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///products.sqlite3'
    
    app.config.update(
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{app.instance_path}/survey.db",
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )
    
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.route("/bar")
    def bar():
        data = []
        questions = Question.query.all()
        # Generate the figure **without using pyplot**.
        for item in questions:
            df = pd.read_sql_query(f"SELECT customeranswer.id, answer.content FROM customeranswer LEFT JOIN answer ON answer.id = customeranswer.answer_id WHERE customeranswer.question_id = {item.id}", db.session.bind)    
            df = df["content"].value_counts()
            fig = Figure()
            ax = fig.subplots()
            
            if item.type=="checkbox":
                df.plot(ax=ax, kind="bar", title=item.title, ylabel="")
            else:
                df.plot(ax=ax, kind="pie", title=item.title, ylabel="")
            # Save it to a temporary buffer.
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data.append(base64.b64encode(buf.getbuffer()).decode("ascii"))
        # fig = Figure()
        # ax = fig.subplots()
        
        # ax.set_title("Thiết kế")
        # labels = ("Không hài lòng", "Hài lòng", "Rất hài lòng")
        # values = (47, 42, 11)
        # explode = (0, 0, 0)
        # ax.pie(values, labels=labels, autopct="%.2f%%", explode=explode)
        # # Save it to a temporary buffer.
        # buf = BytesIO()
        # fig.savefig(buf, format="png")
        # # Embed the result in the html output.
        # data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return render_template("bar.html", data = data)
    
    @app.route("/init-db")
    def init():
        list_questions = []
        list_answer = []
        list_questions.append(Question(id= 1, title="Thiết kế", type = "radio"))
        list_questions.append(Question(id= 2, title="Ứng dụng đa dạng , tiện ích", type = "radio"))
        list_questions.append(Question(id= 3, title="Giá cả", type = "radio"))
        list_questions.append(Question(id= 4, title="Chất lượng sản phẩm tốt", type = "radio"))
        list_questions.append(Question(id= 5, title="Màu sắc ưa thích", type = "checkbox"))
        
        list_answer.append(Answer(id = 1, content="Không hài lòng", question_id = 1))
        list_answer.append(Answer(id = 2, content="Hài lòng", question_id = 1))
        list_answer.append(Answer(id = 3, content="Rất hài lòng", question_id = 1))
        
        list_answer.append(Answer(id = 4, content="Không hài lòng", question_id = 2))
        list_answer.append(Answer(id = 5, content="Hài lòng", question_id = 2))
        list_answer.append(Answer(id = 6, content="Rất hài lòng", question_id = 2))
        
        list_answer.append(Answer(id = 7, content="Hợp lý", question_id = 3))
        list_answer.append(Answer(id = 8, content="Đắt", question_id = 3))
        list_answer.append(Answer(id = 9, content="Rẻ", question_id = 3))
        
        list_answer.append(Answer(id = 10, content="Kém", question_id = 4))
        list_answer.append(Answer(id = 11, content="Tốt", question_id = 4))
        list_answer.append(Answer(id = 12, content="Rất tốt", question_id = 4))
        
        list_answer.append(Answer(id = 13, content="Xanh", question_id = 5))
        list_answer.append(Answer(id = 14, content="Trắng", question_id = 5))
        list_answer.append(Answer(id = 15, content="Đen", question_id = 5))
        list_answer.append(Answer(id = 16, content="Hồng", question_id = 5))
        
        for i in range(4):
            db.session.add(list_questions[i])
        for i in range(15):
            db.session.add(list_answer[i])
        db.session.commit()

        return render_template("index.html", data={"name": "Lê Xuân Quý"})
    
    @app.route("/news")
    def news():
        return "Đây là trang tin tức!"
    
    
    # @app.route("/product", methods = ['GET', "DELETE"])
    # def product():
    #     products = Product.query.all()
    #     if request.method == 'GET':
    #          return render_template("product/list.html", products=products)
    #     elif request.method == "DELETE":
    #         Product.query.filter_by(id=id).delete()
    #         db.session.commit()
    
    # @app.route("/news-detail/<int:id>")
    # @app.route("/product/<int:id>")
    # def detail(id):
    #     p = Product.query.filter_by(id=id).first()
    #     return render_template("product/detail.html", data = p)
    
    # @app.route("/add")
    # def add():
    #     return "Đây là trang tin tức!"
    
    # @app.route('/edit/<int:id>', methods = ['GET', 'POST'])
    # def edit(id):
    #     p = Product.query.filter_by(id=id).first()
    #     if request.method == 'GET':
    #         return render_template("product/edit.html", data = p)
    #     else:
    #         p.name = request.form['name']
    #         db.session.commit()
    #         return redirect(url_for('product'))
        
                
    return app