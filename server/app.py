from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TESTING"] = True

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# ---------------------
# CREATE TABLES AND ADD DEFAULT PLANT
# ---------------------
with app.app_context():
    db.create_all()

    # Add default Plant if DB is empty
    if not Plant.query.first():
        default_plant = Plant(
            name="Douglas Fir",
            image="https://example.com/douglas_fir.jpg",
            price=100.0
        )
        db.session.add(default_plant)
        db.session.commit()


# ---------------------
# ROUTES
# ---------------------
@app.route("/plants", methods=["GET"])
def get_plants():
    plants = Plant.query.all()
    return jsonify([p.to_dict() for p in plants]), 200


@app.route("/plants/<int:id>", methods=["GET"])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict()), 200


@app.route("/plants", methods=["POST"])
def create_plant():
    data = request.get_json()
    plant = Plant(
        name=data["name"],
        image=data.get("image"),
        price=data.get("price", 0)
    )
    db.session.add(plant)
    db.session.commit()
    return jsonify(plant.to_dict()), 201
