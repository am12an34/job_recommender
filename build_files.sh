#!/bin/bash

echo "🚀 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt || { echo "❌ Failed to install dependencies"; exit 1; }

echo "🚀 Running collectstatic..."
python manage.py collectstatic --noinput || { echo "❌ collectstatic failed"; exit 1; }

echo "🚀 Starting Django server..."
gunicorn job_recimnder.wsgi:application --bind 0.0.0.0:8000
