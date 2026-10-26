# Workout API Backend

## Overview
A RESTful API built with Flask and Flask-SQLAlchemy for managing workouts and exercises. It supports creating, viewing, and deleting workouts and exercises, as well as adding exercises to workouts.

## Technologies
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite

## Features
- View all workouts and individual workouts
- Create and delete workouts
- View all exercises and individual exercises
- Create and delete exercises
- Add exercises to workouts with sets, reps, or duration
- Validate input data and handle errors
- Enforce database constraints and relationships

## Setup

1. Install Python and Pipenv.
2. Install project dependencies:

   ```bash
   pipenv install
   ```

3. Activate the environment:

   ```bash
   pipenv shell
   ```

4. Apply database migrations:

   ```bash
   flask db upgrade
   ```

5. Seed sample data if needed:

   ```bash
   python seed.py
   ```

   **Warning:** The seed script may reset existing database data. Use it only when you are happy to recreate the sample database.

6. Start the server:

   ```bash
   python app.py
   ```

The API runs at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List workouts |
| GET | `/workouts/<id>` | View one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List exercises |
| GET | `/exercises/<id>` | View one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<id>/exercises` | Add an exercise to a workout |

## Example Requests

Create a workout:

```json
{
  "name": "Morning Workout",
  "description": "A beginner workout"
}
```

Create an exercise:

```json
{
  "name": "Push-ups",
  "description": "A bodyweight exercise",
  "muscle_group": "Chest"
}
```

Add an exercise to a workout:

```json
{
  "exercise_id": 1,
  "sets": 3,
  "reps": 10
}
```

## Database
Database migrations are managed using Flask-Migrate. The database includes workouts, exercises, and a workout-exercise association table.

## Testing
The API has been manually tested for creating and retrieving records, adding exercises to workouts, input validation, duplicate names, missing IDs, and deletion.

## Author
Allan Mucheru
