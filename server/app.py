from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.get("/workouts")
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([
        {"id": w.id, "date": str(w.date), "duration_minutes": w.duration_minutes, "notes": w.notes}
        for w in workouts
    ]), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify({"id": workout.id, "date": str(workout.date)}), 200


@app.post("/workouts")
def create_workout():
    data = request.get_json()
    workout = Workout(
        date=data["date"],
        duration_minutes=data["duration_minutes"],
        notes=data.get("notes"),
    )
    db.session.add(workout)
    db.session.commit()
    return jsonify({"id": workout.id}), 201


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
    return jsonify([
        {"id": e.id, "name": e.name, "category": e.category, "equipment_needed": e.equipment_needed}
        for e in exercises
    ]), 200


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify({"id": exercise.id, "name": exercise.name}), 200


@app.post("/exercises")
def create_exercise():
    data = request.get_json()
    exercise = Exercise(
        name=data["name"],
        category=data["category"],
        equipment_needed=data.get("equipment_needed", False),
    )
    db.session.add(exercise)
    db.session.commit()
    return jsonify({"id": exercise.id}), 201


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

    data = request.get_json() or {}
    we = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds"),
    )
    db.session.add(we)
    db.session.commit()
    return jsonify({"id": we.id}), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)