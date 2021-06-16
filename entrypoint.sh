#!/bin/sh
poetry run gunicorn -b 0.0.0.0:$PORT "todo_app.app:create_app()"