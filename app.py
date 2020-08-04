from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired,Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import distinct

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ThanksP0stgres!@localhost:5432/bestiary"
app.config['SECRET_KEY'] = "tylerskelton"
db = SQLAlchemy(app)

class monstersModel(db.Model):
    __tablename__ = 'bestiary'

    id = db.Column(db.Integer, primary_key=True) 
    Name = db.Column(db.String())
    CR = db.Column(db.Integer())
    XP = db.Column(db.Integer())

    def __init__(self, Name, CR, XP):
        self.Name = Name
        self.CR = CR
        self.XP = XP

    def __repr__(self):
        return f"<{self.Name}>"

def _get_form(data=None):
    form = FilterForm(data)
    form.cr.choices = [(r.CR,r.CR) for r in monstersModel.query.distinct('CR').order_by("CR")]
    return form
    
class FilterForm(FlaskForm):
    sort = SelectField('sort', 
        validators=[DataRequired()], 
        choices=[('Name', 'Name'),('CR', 'CR'), ('XP', 'XP')]
    )
    cr = SelectField('cr',
        validators=[Optional()],
        choices=[]
    )

@app.route('/monsters', methods=['GET','POST'])
def handle_monsters():
    monsters = monstersModel.query
    if request.method == 'GET':
        form = _get_form()

    else:
        form = _get_form(request.form)
        if form.validate():
            monsters = monsters.order_by(form.sort.data)
            if form.cr.data:
                monsters = monsters.filter_by(CR=form.cr.data)
            print ("successful form all good")
        else:
            print(form.errors)
            print("bullshit form i hate it")

    results = [{
        "name": monster.Name,
        "cr": monster.CR,
        "xp": monster.XP
    } for monster in monsters]

    return render_template("monsters.html",monsters=results,form=form)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')