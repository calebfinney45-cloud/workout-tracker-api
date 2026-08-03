#!/usr/bin/env python3
from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    push_up = Exercise(name="Push Up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    db.session.add_all([push_up, squat, running])
    db.session.commit()

    leg_day = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Leg day.")
    db.session.add(leg_day)
    db.session.commit()

    db.session.add(WorkoutExercise(workout=leg_day, exercise=squat, reps=10, sets=4))
    db.session.commit()
    print("Seeding complete!")