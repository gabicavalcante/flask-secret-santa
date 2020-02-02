from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import db, Draw

admin = Admin(name='secret-santa', template_mode='bootstrap3')
admin.add_view(ModelView(Draw, db.session))