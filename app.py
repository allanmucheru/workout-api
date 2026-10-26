
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from extensions import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

from models import Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Workout API is running"}), 200


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return error_response("Workout not found", 404)
    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400
    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)
    except IntegrityError:
        db.session.rollback()
        return error_response("Workout name already exists", 409)


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return error_response("Workout not found", 404)
    db.session.delete(workout)
    db.session.commit()
    return "", 204


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return error_response("Exercise not found", 404)
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400
    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)
    except IntegrityError:
        db.session.rollback()
        return error_response("Exercise name already exists", 409)


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return error_response("Exercise not found", 404)
    db.session.delete(exercise)
    db.session.commit()
    return "", 204


@app.route("/workouts/<int:workout_id>/exercises", methods=["POST"])
def add_exercise_to_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return error_response("Workout not found", 404)

    try:
        data = workout_exercise_schema.load(request.get_json() or {})
        exercise_id = data.pop("exercise_id")
        exercise = db.session.get(Exercise, exercise_id)

        if exercise is None:
            return error_response("Exercise not found", 404)

        association = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            **data
        )
        db.session.add(association)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(association)), 201
    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400
    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)
    except IntegrityError:
        db.session.rollback()
        return error_response(
            "Duplicate exercise assignment or invalid database values", 409
        )


if __name__ == "__main__":
    app.run(debug=True)
