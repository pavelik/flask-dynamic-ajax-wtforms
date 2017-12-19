from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.config.from_object('config')


# FORMS
import wtforms
from wtforms.widgets.core import HTMLString, html_params, escape
from wtforms.csrf.session import SessionCSRF
from wtforms.validators import DataRequired


class MyForm(wtforms.Form):
    # WTForms CSRF Handling
    class Meta:
        csrf = app.config['WTF_CSRF_ENABLED']
        csrf_class = SessionCSRF
        csrf_secret = app.config['SECRET_KEY']

        @property
        def csrf_context(self):
            return session

    firstname = wtforms.FieldList(wtforms.StringField(), min_entries=1)
    lastname = wtforms.StringField(validators=[DataRequired()])
    boolean = wtforms.BooleanField()
    email = wtforms.FieldList(wtforms.StringField(), min_entries=1)

# VIEWS
@app.route('/', methods=["GET", "POST"])
def index():

    # get data from database and generate form at this point
    obj = "Test" # Test data to populate form field

    form = MyForm()
    for x in range(2):
        form.firstname.append_entry(obj)
    form.email.append_entry()

    if request.method == "POST":

        form = MyForm(request.form)

        for fieldlist in form: # check console logs to verify if data was received
            try:
               _ = (entry for entry in fieldlist)
            except TypeError:
                print fieldlist.name, fieldlist.data
                continue
            for entry in fieldlist:
                print entry.name, entry.data

        if form.validate():
            # data is valid, so at this point save data to database
            return jsonify({'success':'Yay!'})

        else:
            # errors occured during validation
            return (jsonify({'errors':'Data not saved! Lastname is required!'}))

    return render_template('form.html', form=form)


if __name__ == '__main__':

    app.run()
