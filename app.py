from flask import Flask, render_template, request, session, jsonify

from wtforms import Form, StringField, BooleanField, FormField, FieldList
from wtforms.csrf.session import SessionCSRF
from wtforms.validators import DataRequired

# INIT
app = Flask(__name__)
app.config.from_object('config')


# FORMS
class ResidenceForm(Form):
    place = StringField()
    zipcode = StringField()


class MyForm(Form):
    # WTForms CSRF Handling
    class Meta:
        csrf = app.config['WTF_CSRF_ENABLED']
        csrf_class = SessionCSRF
        csrf_secret = app.config['SECRET_KEY']

        @property
        def csrf_context(self):
            return session

    firstname = FieldList(StringField(), min_entries=1)
    lastname = StringField(validators=[DataRequired()])
    boolean = BooleanField()
    email = FieldList(StringField(), min_entries=1)
    residence = FieldList(FormField(ResidenceForm), min_entries=1)


# VIEWS
@app.route('/', methods=["GET", "POST"])
def index():

    # get data from database and generate form at this point
    obj = "Test"  # Test data to populate form field

    form = MyForm()
    for x in range(2):
        form.firstname.append_entry(obj)
    form.email.append_entry()

    if request.method == "POST":

        # get data from ajax request
        form = MyForm(request.form)

        for fieldlist in form:   # check console logs if data was received
            try:
                _ = (entry for entry in fieldlist)
            except TypeError:
                print fieldlist.name, fieldlist.data
                continue
            for entry in fieldlist:
                print entry.name, entry.data

        # server-side validation
        if form.validate():
            # data is valid, so at this point save data to database
            return jsonify({'success': 'Yay!'})

        else:
            # errors occured during validation
            return (jsonify({'errors': 'Data not saved! Lastname required!'}))

    return render_template('form.html', form=form)


if __name__ == '__main__':

    app.run()
