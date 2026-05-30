#!/bin/bash
set -o errexit

echo "====================================="
echo "🚀 Starting Render Deployment"
echo "====================================="
echo ""

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🗄️  Running migrations..."
python manage.py migrate

echo ""
echo "📊 Loading data from SQLite backup (if exists)..."
if [ -f "data.json" ]; then
    echo "✅ Found data.json - Loading data..."
    python manage.py loaddata data.json || echo "⚠️  Data loading skipped or partial"
else
    echo "ℹ️  No data.json found - Starting with fresh database"
fi

echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "====================================="
echo "✅ Deployment setup complete!"
echo "====================================="
