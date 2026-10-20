"""The LabBook traceability matrix, kept as code so CI fails when a requirement loses its tests."""
import tests.test_labbook as labbook_tests
from sd_tools import trace_gaps

REQUIREMENTS = {
    "FR-01": "A user can book a workstation for a time slot",
    "FR-02": "No two active bookings overlap on one workstation",
    "FR-03": "Bookings only within opening hours on a single day",
    "FR-04": "Students book at most 10 h per Monday-Sunday week",
    "FR-05": "Out-of-service workstations cannot be booked",
    "FR-06": "The booker or a technician may cancel",
    "FR-07": "Booking lifecycle and check-in by the booker only",
    "FR-08": "Users are notified of confirmations and cancellations",
    "FR-09": "A slot must end after it starts and last at most 8 hours",
    "NFR-01": "Every booking state change is auditable",
    "NFR-02": "Rules can be added without changing the booking service",
    "NFR-03": "Storage can change without changing the service",
    "NFR-04": "A failing notification must not cancel a booking",
    "NFR-05": "The booking service is testable in isolation with substitute rules",
    "FR-10": "A user can list their own bookings in time order",
    "NFR-06": "Repositories reject saving bookings that were never added",
}
LINKS = {
    "FR-01": ["test_book_confirm_notify"],
    "FR-02": ["test_no_overlap_ignores_cancelled", "test_book_confirm_notify"],
    "FR-03": ["test_opening_hours"],
    "FR-04": ["test_weekly_quota_students_only"],
    "FR-05": ["test_cli"],
    "FR-06": ["test_cancel_permissions"],
    "FR-07": ["test_state_machine", "test_check_in_and_errors"],
    "FR-08": ["test_book_confirm_notify", "test_cancel_permissions"],
    "FR-09": ["test_timeslot_validation_and_overlap"],
    "NFR-01": ["test_book_confirm_notify"],
    "NFR-02": ["test_new_rule_plugs_in_without_changing_service"],
    "NFR-03": ["test_repository_contract"],
    "NFR-04": ["test_failing_subscriber_does_not_break_booking"],
    "NFR-05": ["test_service_with_fake_rules_is_easy_to_test"],
    "FR-10": ["test_my_bookings_sorted"],
    "NFR-06": ["test_save_unknown_booking_raises"],
}


def test_every_requirement_traced_and_every_test_justified():
    tests = {n for n in dir(labbook_tests) if n.startswith("test_")}
    assert trace_gaps(REQUIREMENTS, LINKS, tests) == {
        "untested_requirements": [], "unknown_tests": [],
        "links_to_unknown_requirements": [], "tests_without_requirement": []}
