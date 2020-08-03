from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
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

class SortForm(FlaskForm):
    sort = SelectField('sort', 
        validators=[DataRequired()], 
        choices=[('Name', 'Name'),('CR', 'CR'), ('XP', 'XP')]
    )

class CRForm(FlaskForm):
    crSelect = QuerySelectField(monstersModel.query.distinct('CR'))

@app.route('/monsters', methods=['GET','POST'])
def handle_monsters():
    if request.method == 'GET':
        monsters = monstersModel.query.all()
        form = SortForm()

        crSelect = CRForm()
        monstersCR = monstersModel.query.distinct('CR')
        uniqueCRs = [
            monsterCR.CR
         for monsterCR in monstersCR]


    else:
        form = SortForm(request.form)
        if form.validate(): 
            monsters = monstersModel.query.order_by(form.sort.data)
            print ("successful form all good")
        else:
            print(form.errors)
            print("bullshit form i hate it")

    results = [{
        "name": monster.Name,
        "cr": monster.CR,
        "xp": monster.XP
    } for monster in monsters]

    return render_template("monsters.html",monsters=results,form=form,uniqueCRs=uniqueCRs,crSelect=crSelect)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')