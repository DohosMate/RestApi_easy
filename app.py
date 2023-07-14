from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/plants')
def get_plants():
    plants = Plant.query.all()
    output = []
    for plant in plants:
        plant_data = {"name": plant.name, "description": plant.description}
        output.append(plant_data)
    return {"plants": output}


@app.route('/plants/<id>')
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return {"name": plant.name, "description": plant.description}


@app.route('/plants', methods=['POST'])
def add_plant():
    plant = Plant(
        name=request.json['name'],
        description=request.json['description'])
    db.session.add(plant)
    db.session.commit()
    return {'id': plant.id}

@app.route('/plants/<id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if plant is None:
        return {'error': 'not found'}
    db.session.delete(plant)
    db.session.commit()
    return {'deleted': plant.name}