"""
WSGI Application for Vercel Deployment
"""
from main import app

# Export for Vercel
__all__ = ['app']
