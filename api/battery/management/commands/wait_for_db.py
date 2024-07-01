from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        """
        A management command to wait for the database to become available.

        Args:
            self: The command instance.

        Returns:
            None

        Raises:
            Psycopg2Error: If there is an issue with the database connection to postgres.
            OperationalError: If there is an issue with the database connection to django.

        Examples:
            This command is typically used to delay execution until the database is ready.
        """
        self.stdout.write("Checking database connection...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError) as e:
                self.stdout.write(f"Database unavailable due to {e}, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
