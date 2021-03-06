from flask import Flask, url_for, render_template, request, redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import Email
from .models import db, Question, Answer, Customer, CustomerAnswer
import ast
import base64
from io import BytesIO
from matplotlib.figure import Figure
import pandas as pd
from flask_migrate import Migrate


class RegistrationForm(Form):
    full_name = StringField('Họ tên', [validators.DataRequired(message="Vui lòng nhập họ tên")])
    email = StringField('Email', [validators.DataRequired(message="Vui lòng nhập email"), Email("Email không đúng định dạng")])
    job = StringField('Nghề nghiệp', [validators.DataRequired(message="Vui lòng nhập nghề nghiệp")])
    age = StringField('Tuổi', [validators.DataRequired(message="Vui lòng nhập tuổi")])
    income = StringField('Thu nhập', [validators.DataRequired(message="Vui lòng nhập thu nhập")])


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

    @app.route("/")
    def home():
        return redirect(url_for('start'))
    
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
                df.plot(ax=ax, kind="pie", title=item.title, ylabel="", autopct='%1.1f%%')
            # Save it to a temporary buffer.
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data.append(base64.b64encode(buf.getbuffer()).decode("ascii"))
        return render_template("bar.html", data = data)
    
    @app.route("/init-db")
    def init():
        Question.query.delete()
        Answer.query.delete()
        db.session.commit()
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
        list_answer.append(Answer(id = 17, content="Xám", question_id = 5))
        list_answer.append(Answer(id = 18, content="Tím", question_id = 5))
        list_answer.append(Answer(id = 19, content="Vàng", question_id = 5))
        
        for i in range(len(list_questions)):
            db.session.add(list_questions[i])
        for i in range(len(list_answer)):
            db.session.add(list_answer[i])
        db.session.commit()

        return render_template("index.html", data={"name": "Lê Xuân Quý"})
    
    @app.route('/customer', methods = ['GET'])
    def customer():
        customers = Customer.query.all()
        return render_template('customer/list.html', customers= customers)
    
    
    
    
    @app.route('/survey', methods = ['GET', 'POST'])
    def start():
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            customer = Customer(full_name = form.full_name.data, email =form.email.data,
                        job = form.job.data, age = form.age.data, income = form.income.data)
            db.session.add(customer)
            db.session.commit()
            return redirect(url_for('survey', customer_id=customer.id))
        return render_template('customer/add.html', form=form)
    
    
    @app.route('/survey/<int:customer_id>', methods = ['GET', 'POST'])
    def survey(customer_id):
        questions = Question.query.all()
        answers = Answer.query.all()
        customer_answer = CustomerAnswer.query.all()
        if request.method == 'GET':
            return render_template("survey/form.html", questions = questions, answers = answers, customer_id =customer_id, customer_answer = customer_answer)
        else:
            data = request.form['data']
            data = ast.literal_eval(data)
            print(data)
            for item in data:
                print(item)
                add = CustomerAnswer(answer_id= item['answer'], question_id= item['question'], customer_id = customer_id)
                db.session.add(add)
            db.session.commit()
            return redirect(url_for('bar'))
    
    return app