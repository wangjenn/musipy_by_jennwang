#!/usr/bin/env python
from app import app as application

if __name__ == '__main__':
    # For production, use gunicorn instead
    # Run with: gunicorn -w 4 -b 0.0.0.0:9000 run_production:application
    application.run(host='0.0.0.0', port=9000, debug=False)
