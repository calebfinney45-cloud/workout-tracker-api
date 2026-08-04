from marshmallow import Schema, fields, validate

from models import VALID_CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=1, error="name must not be empty"),
    )
    category = fields.String(
        required=True,
        validate=validate.OneOf(
            VALID_CATEGORIES,
            error=f"category must be one of: {', '.join(VALID_CATEGORIES)}",
        ),
    )
    equipment_needed = fields.Boolean(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)

    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="duration_minutes must be a positive integer"),
    )
    notes = fields.String(required=False, allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)

    reps = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="reps must be >= 0"))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=0, error="sets must be >= 0"))
    duration_seconds = fields.Integer(
        allow_none=True, validate=validate.Range(min=0, error="duration_seconds must be >= 0")
    )


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()