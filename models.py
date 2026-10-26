
from datetime import datetime

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

from extensions import db


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False, default="")
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Workout name cannot be empty")

        if len(value.strip()) > 100:
            raise ValueError("Workout name is too long")

        return value.strip()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False, default="")
    muscle_group = db.Column(db.String(50), nullable=False)

    workouts = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise name cannot be empty")

        if len(value.strip()) > 100:
            raise ValueError("Exercise name is too long")

        return value.strip()

    @validates("muscle_group")
    def validate_muscle_group(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Muscle group cannot be empty")

        if len(value.strip()) > 50:
            raise ValueError("Muscle group is too long")

        return value.strip()


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)

    workout = db.relationship(
        "Workout",
        back_populates="exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workouts"
    )

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="uq_workout_exercise"
        ),
        CheckConstraint(
            "sets IS NULL OR sets > 0",
            name="ck_sets_positive"
        ),
        CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="ck_reps_positive"
        ),
        CheckConstraint(
            "duration_minutes IS NULL OR duration_minutes > 0",
            name="ck_duration_positive"
        ),
        CheckConstraint(
            "reps IS NOT NULL OR duration_minutes IS NOT NULL",
            name="ck_exercise_measurement_required"
        ),
    )

    @validates("sets", "reps", "duration_minutes")
    def validate_measurements(self, key, value):
        if value is not None:
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or value <= 0
            ):
                raise ValueError(
                    f"{key} must be a positive integer"
                )

        return value
