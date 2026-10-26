
from app import app, db
from models import Workout, Exercise, WorkoutExercise


with app.app_context():
    # Reset the database for development seeding.
    db.drop_all()
    db.create_all()

    # Create sample workouts.
    strength = Workout(
        name="Full Body Strength",
        description="A beginner-friendly strength session",
    )
    cardio = Workout(
        name="Cardio Session",
        description="A cardiovascular training session",
    )

    # Create reusable exercises.
    pushups = Exercise(
        name="Push-ups",
        description="A bodyweight upper-body exercise",
        muscle_group="Chest",
    )
    squats = Exercise(
        name="Squats",
        description="A lower-body exercise",
        muscle_group="Legs",
    )
    running = Exercise(
        name="Running",
        description="A cardiovascular exercise",
        muscle_group="Cardio",
    )

    db.session.add_all([
        strength, cardio, pushups, squats, running
    ])
    db.session.flush()

    # Connect exercises to workouts.
    db.session.add_all([
        WorkoutExercise(
            workout=strength,
            exercise=pushups,
            sets=3,
            reps=10,
        ),
        WorkoutExercise(
            workout=strength,
            exercise=squats,
            sets=3,
            reps=12,
        ),
        WorkoutExercise(
            workout=cardio,
            exercise=running,
            duration_minutes=20,
        ),
    ])

    db.session.commit()
    print("Database seeded successfully!")
