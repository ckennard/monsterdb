from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField
from wtforms.validators import DataRequired,Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import distinct
import json
from fractions import Fraction
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

with open('/etc/config.json') as config_file:
  config = json.load(config_file)

app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class monstersModel(db.Model):
    __tablename__ = 'bestiary'

    id = db.Column(db.Integer, primary_key=True) 
    Name = db.Column(db.String())
    CR = db.Column(db.String())
    Type = db.Column(db.String())
    Source = db.Column(db.String())
    Alignment = db.Column(db.String())
    Size = db.Column(db.String())
    Environment = db.Column(db.String())
    Party = db.Column(db.String())
    Link = db.Column(db.String())

    def __init__(self, Name, CR, Type, Source, Alignment, Size, Environment, Party, Link):
        self.Name = Name
        self.CR = CR
        self.Type = Type
        self.Source = Source
        self.Alignment = Alignment
        self.Size = Size
        self.Environment = Environment
        self.Party = Party
        self.Link = Link


def _get_form(data=None):
    form = FilterForm(data)
    # form.cr.choices = [('All CRs', 'All CRs')]+[(r.CR,r.CR) for r in monstersModel.query.distinct('CR').order_by("CR")]
    choices = [r.CR for r in monstersModel.query.distinct('CR').order_by("CR")]
    stringlist = sorted([i for i in choices if "/" in i])
    intlist = sorted([int(i) for i in choices if "/" not in i ])
    choices = stringlist+intlist
    form.cr.choices = [('All CRs', 'All CRs')]+[(str(r),str(r)) for r in choices]
    form.Type.choices = [('All Types', 'All Types')]+[(r.Type,r.Type.capitalize()) for r in monstersModel.query.distinct('Type').order_by("Type")]
    form.Source.choices = [('All Sources', 'All Sources'), ('1pp', '1pp'), ('3pp', '3pp')]+[(r.Source,r.Source) for r in monstersModel.query.distinct('Source').order_by("Source")]
    form.Alignment.choices = [('All Alignments', 'All Alignments')]+[(r.Alignment,r.Alignment) for r in monstersModel.query.distinct('Alignment').order_by("Alignment")]
    form.Size.choices = [('All Sizes', 'All Sizes'),('Fine','Fine'),('Diminutive','Diminutive'),('Tiny','Tiny'),('Small', 'Small'),('Medium','Medium'),('Large','Large'),('Huge','Huge'),('Gargantuan','Gargantuan'),('Colossal','Colossal')]
    form.Environment.choices = [('All Environments', 'All Environments')]+[(r.Environment,r.Environment) for r in monstersModel.query.distinct('Environment').order_by("Environment")]
    return form
    
class FilterForm(FlaskForm):
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
    Alignment = SelectMultipleField('Alignment',
        validators=[Optional()],
        choices=[]
    )
    Size = SelectMultipleField('Size',
        validators=[Optional()],
        choices=[]
    )
    Environment = SelectMultipleField('Environment',
        validators=[Optional()],
        choices=[]
    )

@app.route('/', methods=['GET','POST'])
@cache.cached(timeout=10000)
def handle_monsters():
    monsters = monstersModel.query
    if request.method == 'GET':
        form = _get_form()

    else:
        form = _get_form(request.form)
        if form.validate():
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
                    if not '1pp' in form.Source.data and not '3pp' in form.Source.data:
                        print ("Source filter detected")
                        monsters = monsters.filter(monstersModel.Source.in_(form.Source.data))
                    elif '1pp' in form.Source.data:
                        print ("1pp Source filter detected")
                        monsters = monsters.filter(monstersModel.Party.in_(form.Source.data))
                    elif '3pp' in form.Source.data:
                        print ("3pp Source filter detected")
                        monsters = monsters.filter(monstersModel.Party.in_(form.Source.data))
                else:
                    print("All Sources selected")
            if form.Alignment.data:
                if not 'All Alignments' in form.Alignment.data:
                    print ("Alignment filter detected")
                    monsters = monsters.filter(monstersModel.Alignment.in_(form.Alignment.data))
                else:
                    print("All Alignments selected")
            if form.Size.data:
                if not 'All Sizes' in form.Size.data: 
                    print ("Size filter detected")
                    monsters = monsters.filter(monstersModel.Size.in_(form.Size.data))
                else:
                    print("All Sizes selected")
            if form.Environment.data:
                if not 'All Environments' in form.Environment.data: 
                    print ("Environment filter detected")
                    monsters = monsters.filter(monstersModel.Environment.in_(form.Environment.data))
                else:
                    print("All Environments selected")
            print ("successful form all good")
        else:
            print(form.errors)
            print("bullshit form i hate it")

    results = [{
        "name": monster.Name,
        "cr": monster.CR,
        "Type": monster.Type,
        "Source": monster.Source,
        "Alignment": monster.Alignment,
        "Size": monster.Size,
        "Environment": monster.Environment,
        "Link": monster.Link
    } for monster in monsters]

    return render_template("monsters.html",monsters=results,form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0')