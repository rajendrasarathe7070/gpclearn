from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from datetime import datetime
import json

@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint to keep server alive on Render.
    Returns server status, database info, and timestamp.
    """
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return JsonResponse({
        'status': 'ok',
        'message': 'Server is running',
        'timestamp': datetime.now().isoformat(),
        'service': 'eLearn-for-study',
        'database': db_status,
        'environment': 'production' if not __debug__ else 'development'
    })

@require_http_methods(["GET"])
def data_status(request):
    """
    Check data status - how many records are in each table
    """
    from core.models import Note, Book, Syllabus, PYQ, Doubt, User, Branch
    from accounts.models import Profile  # if exists
    
    stats = {
        'notes': Note.objects.count(),
        'books': Book.objects.count(),
        'syllabus': Syllabus.objects.count(),
        'pyq': PYQ.objects.count(),
        'doubts': Doubt.objects.count(),
        'users': User.objects.count(),
        'branches': Branch.objects.count(),
        'timestamp': datetime.now().isoformat(),
    }
    
    return JsonResponse(stats)
