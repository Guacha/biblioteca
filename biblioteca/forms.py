from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

from biblioteca import db
from biblioteca.models import *


class RegisterForm(FlaskForm):
    fname = StringField('Primer Nombre',
                        validators=[DataRequired(), Length(min=3, max=50)])
    lname = StringField('Primer Apellido',
                        validators=[DataRequired(), Length(min=3, max=75)])
    num_doc = IntegerField('No. Documento',
                           validators=[DataRequired()])
    email = StringField('Correo Electrónico',
                        validators=[DataRequired(), Email()])
    phone = IntegerField('Número Telefónico (Opcional)',
                         validators=[Optional()])
    pw = PasswordField('Contraseña',
                       validators=[DataRequired()])
    confirm_pw = PasswordField('Confirmar Contraseña',
                       validators=[DataRequired(), EqualTo('pw')])
    
    submit = SubmitField('Registrarse')
    
    def validate_num_doc(self, num_doc):
        u = db.session.query(User).filter_by(num_id=num_doc.data).first()
        if u:
            raise ValidationError("Ya existe un usuario registrado con ese documento")
        
    def validate_email(self, email):
        u = db.session.query(User).filter_by(email=email.data).first()
        if u:
            raise ValidationError("Ya existe un usuario registrado con ese email")
    
    def validate_phone(self, phone):
        if phone.data:
            u = db.session.query(User).filter_by(phone=phone.data).first()
        if u:
            raise ValidationError("Ya existe un usuario registrado con ese Número de teléfono")
    
    
class LoginForm(FlaskForm):
    num_doc = IntegerField('No. Documento',
                           validators=[DataRequired()])

    pw = PasswordField('Contraseña',
                       validators=[DataRequired()])

    remember = BooleanField('Mantener sesión iniciada')
    
    submit = SubmitField('Registrarse')
    
    
    
    
    