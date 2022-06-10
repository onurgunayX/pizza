
from time import time
from flask import Blueprint
from flask import *
from flask import request #GET POST tan geliyor
from wsgiref.validate import validator
from flask import Flask,render_template,flash
from flask_sqlalchemy import SQLAlchemy

# WTF FORMS
from flask_wtf import FlaskForm
from sqlalchemy import null, true
from wtforms import StringField, SubmitField,SearchField,SelectField, EmailField, IntegerField, TextAreaField,TimeField,DateField,FileField,HiddenField,PasswordField
from wtforms.validators import *


class MyForm(FlaskForm):
    name=StringField(' İsminiz', validators=[DataRequired()])
    
    email = StringField('Email Adresiniz',validators=[DataRequired(),Email(check_deliverability=true)])

    many = IntegerField('Kaç Adet Pizza İstiyorsunuz', validators=[DataRequired(),NumberRange(1,3)]) 
    
    dough = SelectField(label='Hamur Tipi', choices=[("İnce Kenarlı", "İnce Kenarlı"),("Normal ", "Normal"), ("Kalın Kenarlı", "Kalın Kenarlı")])
    
    date=DateField('İstediğiniz Tarih')
   
    time=TimeField('İstediğiniz Saat')
    
    image= FileField(u'Image File')
    
    debit_card=PasswordField('Kart Numaranız', validators=[Length(min=1, max=16, message=None)])
    
    additional_notes  =  TextAreaField("Ek notlar...")
    
    submit=SubmitField("Siparişi Tamamla")


class myloginform(FlaskForm):
    email = StringField("Email Adresiniz", validators=[Email()] )
    password = PasswordField("Şifreniz", validators=[DataRequired()]) 

    submit = SubmitField("Giriş")


class myregisterform(FlaskForm):
    name=StringField("İsminiz", validators=[DataRequired()])
    email = StringField("Email Adresiniz", validators=[Email()] )
    password = PasswordField("Şifreniz", validators=[DataRequired()]) 

    submit = SubmitField("Kaydol")

