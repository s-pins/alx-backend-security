from django.core.management.base import BaseCommand, CommandParser
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Blocks an IP address by adding it to the BlockedIP list.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('ip_address', type=str, help='The IP address to block.')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(f'IP address {ip_address} is already blocked.'))
        else:
            BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP address {ip_address}.'))
