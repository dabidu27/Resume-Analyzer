# we will add celery and redis because we want the next flow:
# User uploads resume

# User uploads job description

# User triggers analysis

# API responds immediately

# Analysis runs in background

# User polls analysis status

# celery enables concurency
# without celery, a user runs an analysis, django cannot process other requests while pdf parsing, ml etc. happen
# user A → upload → analyze_resume()
#              cpu heavy
# user B → upload → blocked (waits)
# with celery, django hands off heavy work immediately, celery workers process jobs in parallel, and multiple users can run analyses at the same time

# redis acts like a queue for tasks - stores tasks and hands them to celery workers

# User A → POST /analyze
#          ↓
#          Redis queue ← job stored here
#          ↓
#          Django responds immediately

# Celery Worker:
#    pulls job from Redis
#    runs analysis in background

# User B → POST /analyze
#          ↓
#          Redis queue ← another job
#          ↓
#          Django responds immediately

import os
from celery import Celery

# tells celery to use resume_analyzer/settings as the django configuration,
# now celery knows our database, installed apps, models, serializers etc.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_analyzer.settings")

# we initializer the background jobs systems
app = Celery("resume_analyzer")

# look inside settings.py and find every line that starts with CELERY
app.config_from_object("django.conf:settings", namespace="CELERY")

# finds tasks.py file and finds the tasks there
app.autodiscover_tasks()
