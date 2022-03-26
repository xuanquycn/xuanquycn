from flask import Flask, url_for, render_template, request, redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from .models import db, Question, Answer, Customer, CustomerAnswer
import ast
from flask_migrate import Migrate


class RegistrationForm(Form):
    full_name = StringField('Họ tên', [validators.DataRequired(message="Vui lòng nhập họ tên")])
    email = StringField('Email', [validators.DataRequired(message="Vui lòng nhập email")])
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
        return "Đây là trang chủ!"
    
    @app.route("/init-db")
    def init():
        # Question.query.delete()
        # Answer.query.delete()
        # db.session.commit()
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
        
        for i in range(5):
            db.session.add(list_questions[i])
        for i in range(16):
            db.session.add(list_answer[i])
        db.session.commit()

        return render_template("index.html", data={"name": "Lê Xuân Quý"})
    
    @app.route('/customer', methods = ['GET'])
    def customer():
        customers = Customer.query.all()
        return render_template('customer/list.html', customers= customers)
    
    
    
    
    @app.route('/survey', methods = ['GET', 'POST'])
    def addCustomer():
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
            return "Gửi khảo sát thành công!"
    
    
    
        # p = Customer.query.filter_by(id=id).first()
        # if request.method == 'GET':
        #return render_template("customer.html")
        # else:
        #     if p:
        #         p.full_name = request.form['full_name']
        #         p.email = request.form['email']
        #         p.job = request.form['job']
        #         p.age = request.form['age']
        #         p.income = request.form['income']
        #     db.session.commit()
        # return redirect(url_for('customer'))
    
    
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