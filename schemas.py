
from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError,
)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
    )
    description = fields.Str(
        load_default="",
        validate=validate.Length(max=300),
    )
    created_at = fields.DateTime(dump_only=True)
    exercises = fields.Nested(
        "WorkoutExerciseSchema",
        many=True,
        dump_only=True,
    )

    @validates_schema
    def validate_workout(self, data, **kwargs):
        if not data.get("name", "").strip():
            raise ValidationError({
                "name": ["Workout name cannot be blank."]
            })


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
    )
    description = fields.Str(
        load_default="",
        validate=validate.Length(max=300),
    )
    muscle_group = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=50),
    )

    @validates_schema
    def validate_exercise(self, data, **kwargs):
        errors = {}

        if not data.get("name", "").strip():
            errors["name"] = ["Exercise name cannot be blank."]

        if not data.get("muscle_group", "").strip():
            errors["muscle_group"] = [
                "Muscle group cannot be blank."
            ]

        if errors:
            raise ValidationError(errors)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
    )
    sets = fields.Int(
        load_default=None,
        allow_none=True,
        validate=validate.Range(min=1),
    )
    reps = fields.Int(
        load_default=None,
        allow_none=True,
        validate=validate.Range(min=1),
    )
    duration_minutes = fields.Int(
        load_default=None,
        allow_none=True,
        validate=validate.Range(min=1),
    )
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def validate_measurement(self, data, **kwargs):
        if (
            data.get("reps") is None
            and data.get("duration_minutes") is None
        ):
            raise ValidationError({
                "reps": [
                    "Provide reps or duration_minutes."
                ]
            })
