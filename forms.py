from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, SelectField
from wtforms.validators import Email, Length, DataRequired, NumberRange, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    description = StringField('Description', validators=[
        DataRequired(),
        Length(max=100)
    ])
    amount = FloatField('Amount (₹)', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ])
    category = SelectField('Category', choices=[
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Shopping', 'Shopping'),
        ('Health', 'Health'),
        ('Entertainment', 'Entertainment'),
        ('Bills', 'Bills'),
        ('Other', 'Other'),
    ], validators=[DataRequired()])
    submit = SubmitField('Add Expense')