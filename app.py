from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField
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
    Source = db.Column(db.String())

    def __init__(self, Name, CR, Type, Source):
        self.Name = Name
        self.CR = CR
        self.Type = Type
        self.Source = Source

    def __repr__(self):
        return f"<{self.Name}>"

def _get_form(data=None):
    form = FilterForm(data)
    form.cr.choices = [('All CRs', 'All CRs')]+[(r.CR,r.CR) for r in monstersModel.query.distinct('CR').order_by("CR")]
    form.Type.choices = [('All Types', 'All Types')]+[(r.Type,r.Type) for r in monstersModel.query.distinct('Type').order_by("Type")]
    form.Source.choices = [('All Sources', 'All Sources')]+[(r.Source,r.Source) for r in monstersModel.query.distinct('Source').order_by("Source")]
    return form
    
class FilterForm(FlaskForm):
    print("filterform")
    sort = SelectField('Sort by...', 
        validators=[DataRequired()], 
        choices=[('Name', 'Name'),('CR', 'CR'), ('Type', 'Type'),('Source', 'Source')]
    )
    cr = SelectMultipleField('CR',
        validators=[Optional()],
        choices=[]
    )
    Type = SelectMultipleField('Type',
        validators=[Optional()],
        choices=[]
    )
    Source = SelectMultipleField('Source',
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
                if not 'All CRs' in form.cr.data: 
                    print ("CR filter detected")
                    monsters = monsters.filter(monstersModel.CR.in_(form.cr.data))
                else:
                    print("All CRs selected")
            if form.Type.data:
                if not 'All Types' in form.Type.data: 
                    print ("Type filter detected")
                    monsters = monsters.filter(monstersModel.Type.in_(form.Type.data))
                else:
                    print("All Types selected")
            if form.Source.data:
                if not 'All Sources' in form.Source.data: 
                    print ("Source filter detected")
                    monsters = monsters.filter(monstersModel.Source.in_(form.Source.data))
                else:
                    print("All Sources selected")
            print ("successful form all good")
        else:
            print(form.errors)
            print("bullshit form i hate it")

    print("results")
    results = [{
        "name": monster.Name,
        "cr": monster.CR,
        "Type": monster.Type,
        "Source": monster.Source
    } for monster in monsters]

    return render_template("monsters.html",monsters=results,form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0')