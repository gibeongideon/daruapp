#!/usr/bin/env bash
celery -A daruapp beat -l DEBUG
#celery -A daruapp beat -l INFO
