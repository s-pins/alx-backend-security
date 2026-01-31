import requests
from django.core.cache import cache
from django.http import HttpResponseForbidden
from ipware import get_client_ip

from .models import BlockedIP, RequestLog


class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        if ip:
            if BlockedIP.objects.filter(ip_address=ip).exists():
                return HttpResponseForbidden("Your IP address has been blocked.")

            geolocation = cache.get(ip)
            if not geolocation:
                try:
                    response = requests.get(f"http://ip-api.com/json/{ip}")
                    response.raise_for_status()
                    data = response.json()
                    if data["status"] == "success":
                        geolocation = {
                            "country": data.get("country"),
                            "city": data.get("city"),
                        }
                        cache.set(ip, geolocation, 60 * 60 * 24)  # Cache for 24 hours
                except requests.exceptions.RequestException as e:
                    # Log the error, but don't block the request
                    print(f"Geolocation lookup failed for {ip}: {e}")
                    geolocation = {"country": None, "city": None}

            country = None
            city = None

            if isinstance(geolocation, dict):
                country = geolocation.get("country")
                city = geolocation.get("city")

            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                country=country,
                city=city,
            )

        response = self.get_response(request)
        return response
