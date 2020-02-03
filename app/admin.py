from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import db, Draw, Participant

admin = Admin(name="secret-santa", template_mode="bootstrap3")


class DrawModelView(ModelView):
    inline_models = (Participant,)


admin.add_view(DrawModelView(Draw, db.session))
