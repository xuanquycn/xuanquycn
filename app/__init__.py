from flask import Flask, url_for, render_template, request, redirect
from .models import db, Product
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    
    # app.config["SECRET_KEY"] ="123456"
    # app.config ["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///products.sqlite3'
    
    app.config.update(
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{app.instance_path}/products.db",
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )
    
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    
    @app.route("/")
    def index():
        p1 = Product(name="K5")
        p2 = Product(name="K8")
    
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

        return render_template("index.html", data={"name": "Lê Xuân Quý"})
    
    @app.route("/news")
    def news():
        return "Đây là trang tin tức!"
    
    
    @app.route("/product", methods = ['GET', "DELETE"])
    def product():
        products = Product.query.all()
        if request.method == 'GET':
             return render_template("product/list.html", products=products)
        elif request.method == "DELETE":
            Product.query.filter_by(id=id).delete()
            db.session.commit()
    
    @app.route("/news-detail/<int:id>")
    @app.route("/product/<int:id>")
    def detail(id):
        p = Product.query.filter_by(id=id).first()
        return render_template("product/detail.html", data = p)
    
    @app.route("/add")
    def add():
        return "Đây là trang tin tức!"
    
    @app.route('/edit/<int:id>', methods = ['GET', 'POST'])
    def edit(id):
        p = Product.query.filter_by(id=id).first()
        if request.method == 'GET':
            return render_template("product/edit.html", data = p)
        else:
            p.name = request.form['name']
            db.session.commit()
            return redirect(url_for('product'))
        
                
    return app