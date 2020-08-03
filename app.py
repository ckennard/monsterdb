
# Previous imports remain...
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ThanksP0stgres!@localhost:5432/bestiary"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
        return f"<Monster {self.Name}>"

@app.route('/monsters', methods=['GET'])
def handle_monsters():
    if request.method == 'GET':
        monsters = monstersModel.query.all()
        results = [
            {
                "name": monster.Name,
                "cr": monster.CR,
                "xp": monster.XP
            } for monster in monsters]

        return {"count": len(results), "monsters": results}

if __name__ == '__main__':
    app.run(host='0.0.0.0')

