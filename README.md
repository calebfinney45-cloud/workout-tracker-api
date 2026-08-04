# Workout Tracker API

## Description

A backend REST API for a workout tracking application used by personal
trainers. The API tracks **Workouts** and reusable **Exercises**, linking
them through a **WorkoutExercise** join table that records the reps, sets,
and/or duration performed for each exercise within a given workout.

Built with **Flask**, **Flask-SQLAlchemy**, **Flask-Migrate**, and
**Marshmallow**.

### Entities & Relationships

- `Exercise` — reusable exercise definitions (`name`, `category`, `equipment_needed`)
- `Workout` — a single training session (`date`, `duration_minutes`, `notes`)
- `WorkoutExercise` — join table linking a `Workout` to an `Exercise`, with
  `reps`, `sets`, and `duration_seconds`

A `Workout` has many `WorkoutExercise`s and many `Exercise`s through
`WorkoutExercise`. An `Exercise` has many `WorkoutExercise`s and many
`Workout`s through `WorkoutExercise`.

### Validation

- **Table constraints**: unique exercise names, a unique `(workout_id, exercise_id)`
  pair, positive workout duration, non-negative reps/sets/duration values,
  and a check constraint on allowed exercise categories.
- **Model validations** (`@validates`): exercise name/category checks,
  positive workout duration, valid date, non-negative reps/sets/duration.
- **Schema validations** (Marshmallow): required fields, `Length`, `OneOf`,
  and `Range` validators mirroring the constraints above.

## Installation

1. Clone the repo and move into it:
```bash
   git clone https://github.com/calebfinney45-cloud/workout-tracker-api.git
   cd workout-tracker-api
```
2. Install dependencies with Pipenv:
```bash
   pipenv install
   pipenv shell
```
3. Move into the `server/` directory (this is where the Flask app lives):
```bash
   cd server
```
4. Set the Flask app environment variable:
```bash
   export FLASK_APP=app.py      # Windows (cmd): set FLASK_APP=app.py
```
5. Create the database tables via migrations:
```bash
   flask db upgrade head
```
6. Seed the database with example data:
```bash
   python seed.py
```

## Running the App

From inside the `server/` directory:

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5555`.

You can re-run `python seed.py` at any time to reset the seed data (it
clears all existing rows first).

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/workouts` | List all workouts |
| `GET` | `/workouts/<id>` | Show a single workout, including its associated exercises with reps/sets/duration |
| `POST` | `/workouts` | Create a workout. Body: `{"date": "YYYY-MM-DD", "duration_minutes": <int>, "notes": "<string>"}` |
| `DELETE` | `/workouts/<id>` | Delete a workout (also deletes its associated `WorkoutExercise` rows) |
| `GET` | `/exercises` | List all exercises |
| `GET` | `/exercises/<id>` | Show a single exercise, including the workouts/sets it's associated with |
| `POST` | `/exercises` | Create an exercise. Body: `{"name": "<string>", "category": "<string>", "equipment_needed": <bool>}` |
| `DELETE` | `/exercises/<id>` | Delete an exercise (also deletes its associated `WorkoutExercise` rows) |
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. Body: `{"reps": <int>, "sets": <int>, "duration_seconds": <int>}` (all optional) |

Valid exercise categories: `cardio`, `strength`, `flexibility`, `balance`, `plyometric`.

All validation errors return a `400` status with an `errors` field describing
what went wrong. Requests for missing resources return a `404`.

## Project Structure

```
workout-tracker-api/
├── Pipfile
├── README.md
├── .gitignore
└── server/
    ├── app.py          # Flask app + routes
    ├── models.py       # SQLAlchemy models, relationships, constraints, validations
    ├── schemas.py      # Marshmallow schemas + schema validations
    ├── seed.py         # Seed script
    └── migrations/     # Flask-Migrate migration history
```