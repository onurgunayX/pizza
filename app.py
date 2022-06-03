
from datetime import datetime
from flask import *
from flask import request #GET POST tan geliyor
from wsgiref.validate import validator
from flask import Flask,render_template,flash
from flask_sqlalchemy import SQLAlchemy
# WTF FORMS
from flask_wtf import FlaskForm
from sqlalchemy import null
#from wtforms import StringField, SubmitField,SearchField,SelectField, EmailField, IntegerField, TextAreaField,TimeField
from wtforms.validators import *
from flask_login import UserMixin #27.05.2022
from flask_login import login_user, current_user, logout_user, login_required #27.05.2022
from flask_login import LoginManager #27.05.2022

#Login password encryption için #27.05.2022
from flask_bcrypt import Bcrypt

from orderForm import MyForm, myloginform
from searchForm import SearchForm
#from orderDB import order_database

app=Flask(__name__)
app.config['SECRET_KEY']="mysecret_key"

#app.register_blueprint(order_database)


#Setting up user login parts #27.05.2022 - Login için
login_manager = LoginManager(app)
login_manager.login_view = 'login' #For directing to a please log in page. Otherwise throws a system error.
login_manager.login_message_category = 'info' #Optional?

#USER LOGIN FUNCTION - #27.05.2022 - Login için
@login_manager.user_loader
def load_user(id):
    return pizza_users_db.query.get(int(id)) 

bcrypt = Bcrypt(app) #27.05.2022 Şifre encryption için gerekli.



#Burasi cokomelli py? ile html arasi gizli protokol CSRF TOKEN? 
# HTML deki karsiligi {{form.hidden_tag()}}
 #mysecret_key --> 0sfajjahskOAHSKL123C Gibi bir SEY OLUR GENELDE version controlde public yapilmaz
db = SQLAlchemy(app) #Defining the db object
class orderForm_db(db.Model): #11.05.2022 - our first database table -Nullable'lar eklenecek.
    id = db.Column(db.Integer, primary_key=True) #data type, Nullable, primary_key, parameters according to data_type (Ex:String length)
    name_db = db.Column(db.String(200))
    email_db = db.Column(db.String(200))
    many_db = db.Column(db.Integer)
    dough_db = db.Column(db.String(200))
    date_db = db.Column(db.Date)
    time_db = db.Column(db.DateTime)
    image_db = db.Column(db.String(200))
    debit_card_db = db.Column(db.BigInteger)
    additional_notes_db = db.Column(db.String(200))
    record_time_db = db.Column(db.DateTime, default=datetime.utcnow)
    #initial_status_db = db.Column(db.String(20), nullable=True) #Örnek nullable
        
    def __repr__(self):
        return '<Name %r>' % self.id 

class pizza_users_db(db.Model, UserMixin): #27.05.2022 - Login için  ////  Dikkat!! UserMixin UNUTMAYINIZ
    id = db.Column(db.Integer, primary_key=True)
    name_db = db.Column(db.String(200))
    email_db = db.Column(db.String(200))
    password_db = db.Column(db.String(100))
        
    def __repr__(self):
        return '<Name %r>' % self.id


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("User is already logged in")
        return redirect(url_for('home'))
    
    form = myloginform()
    
    if form.validate_on_submit():
                
        print("Form validated")
        user = pizza_users_db.query.filter_by(email_db=form.email.data).first()
        #TB Not : Atölyede bu konuya bir bakalım. #27.05.2022
        # Eğer şifre doğru olsa bile aranan user'in emaili yanlış ise hata veriyordu çünkü user objesini bulamadığı için 
        # o userın emailini de bulamıyordu. passsword_db attribute yok diyordu. Bu şekilde if kontrolü ile çalışıyor.
        if user:
            password = user.password_db
            print("passcheck hashed", password, "user name : ", user.name_db)
            
            password_check = bcrypt.check_password_hash(password, form.password.data) #Boolean getiriyor. True ise bir alttaki if içerisinde user'i login ediyoruz. #27.05.2022
            print(password_check)
            #print("passcheck", password_check)
        
        if user and password_check:
            print("Pass Check", password_check)
            print("/// Found this user and his password is correct!!! /// Password Hashing technique is used!! I am logging the user in ;) /// ")
            login_user(user)
            
            print("User seems to be logged in now..")
            flash('Giriş İşleminiz başarıyla tamamlandı.', 'success')
            
            return redirect(url_for('Order'))
            
        else:
            flash('There has been a problem during logging in. Please check your username and password', 'error')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout") #27.05.2022
def logout():
    if current_user.is_authenticated:
        
        logout_user()
        print("Tekrar beklerizzz")
        flash('Tekrar beklerizzz', 'success')
    return redirect(url_for('bye'))

@app.route("/register")
def Register():
    return render_template("register.html")

@app.route("/bye")
def bye():
   

   
    flash('Diyetiniz Başarılı Şekilde Devam Ediyor', 'success')
  
   
    return render_template("bye.html")


@app.errorhandler(404)
def error(e):
    return render_template('error.html')




app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sql5492986:hQuHbnspdj@sql5.freemysqlhosting.net/sql5492986"


@app.route("/order",methods=["GET","POST"])
@login_required
def Order():
    form=MyForm()
    name_entered=None
    email_entered=None
    many_entered=None
    dough_entered=None
    additional_notes_entered=None
    date_entered=None
    time_entered=None
    image_entered=None
    debit_card_entered=None
    
    if request.method=="POST":
        if form.validate_on_submit(): #validate etmeyi yariyor true false
            print('Validated')
            name_entered=form.name.data
            email_entered=form.email.data
            many_entered=form.many.data
            dough_entered=form.dough.data
            additional_notes_entered=form.additional_notes.data
            date_entered=form.date.data
            time_entered=form.time.data
            image_entered=form.image.data
            debit_card_entered=form.debit_card.data
       
            new_record = orderForm_db(
                name_db = form.name.data,
                email_db = form.email.data,
                many_db = form.many.data,
                dough_db = form.dough.data,
                additional_notes_db = form.additional_notes.data,
                date_db=form.date.data,
                time_db=form.time.data,
                image_db=form.image.data,
                debit_card_db=form.debit_card.data)
                
          
            try:            
                db.session.add(new_record)
                db.session.commit()
                flash("Girdiğiniz kayıt başarıyla database'e kaydedildi...", "success") #Flash mesaj demosu
            
            except:
         
                flash("Bilgi kayıt aşamasında bir sorun oluştu.", "success") 
        return render_template("successorder.html",form=form, name_entered=name_entered,email_entered=email_entered,many_entered=many_entered,dough_entered=dough_entered, additional_notes_entered=additional_notes_entered,date_entered=date_entered,
            time_entered=time_entered,
            image_entered=image_entered,
            debit_card_entered=debit_card_entered)
        flash("POST icindesin")
    
    if request.method=="GET":
        if form.validate_on_submit(): #validate etmeyi yariyor true false
            form.name.data='test'
        flash("GET icindesin")
    
    
    return render_template("order.html",form=form, name_entered=name_entered,email_entered=email_entered,many_entered=many_entered,dough_entered=dough_entered, additional_notes_entered=additional_notes_entered,date_entered=date_entered,
            time_entered=time_entered,
            image_entered=image_entered,
            debit_card_entered=debit_card_entered)


@app.route("/search",methods=["GET","POST"])
@login_required
def Search():
    form=SearchForm()
    searchBox= None
    if request.method=="POST":
        if form.validate_on_submit(): #validate etmeyi yariyor true false
            print('Validated')
            searchBox_entered=form.searchBox.data
            record_to_show =orderForm_db.query.filter_by(id=searchBox_entered).first()
            return render_template("show_one.html", record_to_show=record_to_show)
          
  
   
    
    return render_template('search.html',form=form)

@app.route('/delete_one/<int:id>') 
def delete_one(id): 

    record_to_delete = orderForm_db.query.filter_by(id=id).first()
    db.session.delete(record_to_delete)
    db.session.commit() #Commit çoğu zaman unutulabiliyor.
   

    return render_template("home.html")



@app.route('/update_one/<int:id>', methods=["GET", "POST"]) #To be deleted #11.05.2022
def update_one(id): #id parametre olarak burada unutulabiliyor!! #11.05.2022

    record_to_update = orderForm_db.query.filter_by(id=id).first()
    form = MyForm()
    if request.method == "POST":
        #form = myform()
        record_to_update.name_db = form.name.data   #request.form["name"]
        print("ID to be updated :", record_to_update.id)
        record_to_update.email_db = form.email.data
 
       
       
        try:
            db.session.commit()
            flash("Müşteri bilgileri başarıyla güncellendi.", "success")
           #  return render_template("show_all.html", record_to_update = record_to_update, form=form)
        except:
            flash("Müşteri bilgilerinin güncellenmesinde bir sorun oluştu! Lütfen IT Yöneticisine bilgi veriniz.", "success")
            # return render_template("show_all.html", record_to_update = record_to_update, form=form)
        
        #return render_template("update_one.html", record_to_update = record_to_update, form=form)

    if request.method == "GET":
        #form = myform()
        form.name.data = record_to_update.name_db
        form.email.data = record_to_update.email_db
       
    
    
        print("ID to be updated :", record_to_update.id)

        return render_template("update_one.html", record_to_update = record_to_update, form=form)
    
    #return render_template("show_all.html")

if __name__=="__main__":
    app.debug=True
    app.run()