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
    Type = db.Column(db.String())

    def __init__(self, Name, CR, Type):
        self.Name = Name
        self.CR = CR
        self.Type = Type

    def __repr__(self):
        return f"<{self.Name}>"

def _get_form(data=None):
    form = FilterForm(data)
    form.cr.choices = [(r.CR,r.CR) for r in monstersModel.query.distinct('CR').order_by("CR")]
    form.Type.choices = [(r.Type,r.Type) for r in monstersModel.query.distinct('Type').order_by("Type")]
    return form
    
class FilterForm(FlaskForm):
    print("filterform")
    sort = SelectField('sort', 
        validators=[DataRequired()], 
        choices=[('Name', 'Name'),('CR', 'CR'), ('Type', 'Type')]
    )
    cr = SelectField('cr',
        validators=[Optional()],
        choices=[]
    )
    Type = SelectField('Type',
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
            if form.Type.data:
                print("form.Type")
                monsters = monsters.filter_by(Type=form.Type.data)
            print ("successful form all good")
        else:
            print(form.errors)
            print("bullshit form i hate it")

    print("results")
    results = [{
        "name": monster.Name,
        "cr": monster.CR,
        "Type": monster.Type
    } for monster in monsters]

    return render_template("monsters.html",monsters=results,form=form)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')