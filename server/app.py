from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.get("/workouts")
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.post("/workouts")
def create_workout():
    json_data = request.get_json() or {}

    try:
        data = workout_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        workout = Workout(
            date=data["date"],
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes"),
        )
        db.session.add(workout)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400

    return jsonify(workout_schema.dump(workout)), 201


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({}), 204


@app.get("/exercises")
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.post("/exercises")
def create_exercise():
    json_data = request.get_json() or {}

    try:
        data = exercise_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        exercise = Exercise(
            name=data["name"],
            category=data["category"],
            equipment_needed=data.get("equipment_needed", False),
        )
        db.session.add(exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400
        
    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({}), 204


@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return jsonify({"error": "Workout or Exercise not found"}), 404

    json_data = request.get_json() or {}

    try:
        data = workout_exercise_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        we = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds"),
        )
        db.session.add(we)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400
    
    return jsonify(workout_exercise_schema.dump(we)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)