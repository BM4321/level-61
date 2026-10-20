"""Tests that EXPOSE the defects in the flawed designs (they pass by demonstrating each problem)."""
import datetime

import pytest

from clinic import flawed_coupling as fc
from clinic import flawed_god_class as fg
from clinic import flawed_inheritance as fi


def test_god_class_defects(capsys):
    m = fg.LabManager()
    assert m.do_booking("amina", "LAB1-01", "2026-03-02 09:00", "2026-03-02 11:00")
    # Defect: the 22:00 closing rule is checked on the hour only, so 22:30 is accepted.
    assert m.do_booking("amina", "LAB1-02", "2026-03-02 20:00", "2026-03-02 22:30")
    # Defect: quota counts all bookings ever, not per week: a booking a month later is refused.
    m.do_booking("amina", "LAB1-02", "2026-03-03 09:00", "2026-03-03 13:00")      # total now 8.5 h
    assert not m.do_booking("amina", "LAB1-02", "2026-04-06 09:00", "2026-04-06 11:00")
    # Defect: SQL built from strings; a quote in the name breaks the query.
    with pytest.raises(Exception):
        m.do_booking("o'brien", "LAB1-01", "2026-03-05 09:00", "2026-03-05 10:00")
    # Defect: output mixed with logic; the only way to see results is to capture stdout.
    assert "OK amina LAB1-01" in capsys.readouterr().out


def test_lsp_violation():
    stations = [fi.Workstation("A"), fi.GpuWorkstation("G")]
    assert fi.book_whole_lab(stations[:1], "drm", 3)
    with pytest.raises(PermissionError):
        fi.book_whole_lab(stations, "drm", 3)       # substituting a subclass breaks the client
    with pytest.raises(NotImplementedError):
        fi.book_whole_lab([fi.OutOfServiceWorkstation("X")], "drm", 1)


def test_inheriting_from_list_bypasses_rules():
    bl = fi.BookingList()
    bl.add_booking("b1")
    bl.append("b1")                                 # duplicate slips in through an inherited method
    assert bl.count("b1") == 2


def test_hidden_dependencies_make_testing_hard():
    soon = {"start": datetime.datetime.now() + datetime.timedelta(minutes=30),
            "user": {"contact": {"email": "amina@example.ac.tz"}}}
    with pytest.raises(ConnectionError):
        fc.ReminderService().remind_if_soon(soon)  # cannot run without a real mail server
    assert fc.Config() is fc.Config()               # global state shared by every test
