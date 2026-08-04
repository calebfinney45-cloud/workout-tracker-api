from marshmallow import Schema, fields, validate
from models import VALID_CATEGORIES

class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    category = fields.String(required=True, validate=validate.OneOf(VALID_CATEGORIES))
    equipment_needed = fields.Boolean(load_default=False)

class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))
    notes = fields.String(allow_none=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=0))

exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()