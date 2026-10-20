"""LabBook: a teaching case study for Software Design and Development (CST06101).

A fictional university computer-lab booking system. Students book workstations, lecturers
reserve whole labs for practical sessions, and technicians manage equipment. The package is
small on purpose: each module illustrates a design idea discussed in the SD lessons.

Layers (dependencies point inwards):
    cli  ->  service  ->  domain, rules, events
                 |
                 v
           repository (interface in domain terms; in-memory and SQLite implementations)
"""
__version__ = "1.0.0"
