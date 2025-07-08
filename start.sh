#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 --forwarded-allow-ips='*' --proxy-headers --log-level debug