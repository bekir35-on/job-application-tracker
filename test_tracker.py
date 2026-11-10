"""Tests for the job application tracker."""

import tempfile
import unittest
from pathlib import Path

from tracker import add_application, filter_by_status, load_applications, next_id, update_status


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / "applications.csv"

    def tearDown(self):
        self.folder.cleanup()

    def test_next_id_starts_at_one(self):
        self.assertEqual(next_id([]), 1)

    def test_next_id_uses_highest_number(self):
        applications = [{"id": "2"}, {"id": "7"}]
        self.assertEqual(next_id(applications), 8)

    def test_add_application_saves_a_new_record(self):
        add_application(self.path, "Acme", "Analyst", "Reed", "Test note")
        saved = load_applications(self.path)
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["company"], "Acme")
        self.assertEqual(saved[0]["status"], "Applied")

    def test_update_status_changes_the_record(self):
        add_application(self.path, "Acme", "Analyst", "Reed", "")
        update_status(self.path, "1", "Offer")
        saved = load_applications(self.path)
        self.assertEqual(saved[0]["status"], "Offer")

    def test_update_status_returns_none_for_unknown_id(self):
        add_application(self.path, "Acme", "Analyst", "Reed", "")
        self.assertIsNone(update_status(self.path, "9", "Offer"))

    def test_filter_by_status_keeps_only_matching_records(self):
        applications = [
            {"id": "1", "status": "Applied"},
            {"id": "2", "status": "Rejected"},
            {"id": "3", "status": "Rejected"},
        ]
        result = filter_by_status(applications, "Rejected")
        self.assertEqual([app["id"] for app in result], ["2", "3"])

    def test_filter_by_status_returns_empty_list_when_no_match(self):
        applications = [{"id": "1", "status": "Applied"}]
        self.assertEqual(filter_by_status(applications, "Offer"), [])


if __name__ == "__main__":
    unittest.main()