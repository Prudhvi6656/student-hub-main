# StudyHub - Flask app for students

Track courses, grades (10-point CGPA), assignment deadlines and focus time.

## Features
- Register / login (hashed passwords, CSRF protection, per-user data isolation)
- Courses with credits; weighted assessments (pending ones are ignored) -> course % -> grade point -> CGPA
- Task manager with due dates, priority, course link, pending/done filters, overdue highlighting
- Focus timer (focus + break modes) that logs sessions through a JSON API, feeding a study streak and daily goal
- Target planner: shows the average % needed on pending assessments to reach each grade point
- Searchable course notes
- Modern UI: sidebar layout, dark mode, charts, mobile bottom-nav
- Dashboard: CGPA, overdue tasks, completed tasks, weekly study time, per-course progress
- JSON endpoints: `POST /api/sessions`, `GET /api/stats`

## Run
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements-dev.txt
    python wsgi.py            # http://127.0.0.1:5000
    pytest                    # tests
    flake8 app tests wsgi.py --max-line-length=100

## Docker
    docker build -t studyhub . && docker run -p 5000:5000 -v studyhub-data:/app/instance studyhub

## Jenkins
New Item -> Pipeline -> Pipeline script from SCM -> repo URL, script path `Jenkinsfile`.
Agent needs python3-venv, docker and curl. Set a real SECRET_KEY for production.

## Structure
    app/__init__.py   app factory, extensions
    app/models.py     User, Course, Assessment, Task, StudySession
    app/grades.py     grade / CGPA maths (pure functions)
    app/auth.py       register, login, logout
    app/main.py       dashboard, courses, tasks, timer, API
    app/templates/    Bootstrap 5 Jinja templates
    tests/            pytest suite
