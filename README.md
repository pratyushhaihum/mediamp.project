# mediamp.project
Flask Backend with Authentication & Celery
> JWT authentication(login,signup,register)
>
> PostgreSql Database with Sql Alchemy
>
> Celery for Background Tasks
>
> Redis for Task Queue
>
> Dockerized Deployement

## Directory Structure

flask_jwt_auth_backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   └── user.py
│   ├── routes/
│   │   └── auth_routes.py
│   ├── tasks.py
│   ├── utils/
│   │   ├── db.py
│   │   └── celery.py
├── run.py
├── requirements.txt
 └── .env
