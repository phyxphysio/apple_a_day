"""Test custom management commands."""

from unittest.mock import patch
from django.core.management import call_command
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("battery.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands.

    Args:
        SimpleTestCase (class): The base class for writing simple tests without database interaction.
    """

    def test_wait_for_db_ready(self, patched_check):
        """Runs test as if database is ready

        Args:
            patched_check (Mock): A mock of the `check` method that simulates the database being available.
        """
        patched_check.return_value = True
        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Runs test as if database is not ready

        Args:
            patched_sleep (MOCK): A mock of the `sleep` method that doesn't sleep.
            patched_check (Mock): A mock of the `check` method that simulates the database being available.
        """
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
