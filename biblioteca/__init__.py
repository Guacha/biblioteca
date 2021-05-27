from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)

#! Esta llave no debería estar expuesta públicamente para propósitos comerciales
app.config["SECRET_KEY"] = 'a815622fcd4aac7961bddb66718292de'

# Definición de la URL y configuración de la BD
# TODO: Migrar a PostgreSQL database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://bibliotech_app:bibliotech2021@localhost/bibliotech"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#Manejo de login y sesiones
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Configuración del módulo ADMIN
from biblioteca import views
from biblioteca import models
admin = Admin(app, name="BiblioTech", template_mode='bootstrap4', index_view=views.HomeView())
admin.add_view(views.BookView(models.Book, db.session))
admin.add_view(views.LoanView(models.Loan, db.session))

# Importar rutas y modelos
from biblioteca import routes