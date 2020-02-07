from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import db, Draw, Participant
from flask_admin.actions import action

admin = Admin(name="secret-santa", template_mode="bootstrap3")


class DrawModelView(ModelView):
    inline_models = (Participant,)
    form_excluded_columns = ("created_at", "in_process")
    column_searchable_list = (Draw.responsible_number,)

    @action("run", "Run", "Are you sure you want to run this draw?")
    def action_approve(self, id):
        try:
            query = Draw.query.filter(Draw.id.in_(id))

            count = 0
            for draw in query.all():
                if draw.in_process:
                    draw.run()
                    count += 1

            flash(
                ngettext(
                    "User was successfully approved.",
                    "%(count)s users were successfully approved.",
                    count,
                    count=count,
                )
            )
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext("Failed to approve users. %(error)s", error=str(ex)), "error")


# admin.add_view(DrawModelView(Draw, db.session))
# admin.add_view(ModelView(Participant, db.session))
