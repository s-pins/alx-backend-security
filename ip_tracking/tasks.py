from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # IPs with more than 100 requests in the last hour
    suspicious_requests = RequestLog.objects.filter(timestamp__gte=one_hour_ago) \
        .values('ip_address') \
        .annotate(request_count=Count('id')) \
        .filter(request_count__gt=100)

    for item in suspicious_requests:
        ip = item['ip_address']
        reason = f"Exceeded 100 requests in the last hour ({item['request_count']} requests)."
        SuspiciousIP.objects.update_or_create(ip_address=ip, defaults={'reason': reason})

    # IPs accessing sensitive paths
    sensitive_paths = ['/admin', '/login']
    suspicious_paths = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').distinct()

    for item in suspicious_paths:
        ip = item['ip_address']
        reason = "Accessed sensitive paths."
        SuspiciousIP.objects.update_or_create(ip_address=ip, defaults={'reason': reason})

