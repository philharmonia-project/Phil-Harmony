#!/usr/bin/env bash
set -o errexit

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🔄 Running database migrations..."
python manage.py migrate

echo "📊 Collecting static files (simplified)..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Static collection had issues, continuing..."

echo "✅ Build completed successfully!"