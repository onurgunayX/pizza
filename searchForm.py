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


class SearchForm(FlaskForm):
    searchBox=IntegerField(' Sipariş Numaranız', validators=[DataRequired()])
    
    search_submit_button=SubmitField("Siparişi BUL")
