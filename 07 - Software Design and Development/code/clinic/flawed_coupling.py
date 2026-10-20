"""FLAWED DESIGN, for critique only (SD Flawed Design Clinic, case F3): tight coupling and hidden dependencies."""
import datetime


class Config:
    _instance = None
    max_hours = 10

    def __new__(cls):                     # global singleton: hidden dependency everywhere
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class SmtpMailer:
    def send(self, to, body):
        raise ConnectionError("no mail server in this environment")


class ReminderService:
    def __init__(self):
        self.mailer = SmtpMailer()        # concrete class created inside: cannot substitute in tests

    def remind_if_soon(self, booking):
        now = datetime.datetime.now()     # hidden dependency on the clock
        if 0 < (booking["start"] - now).total_seconds() < 3600 and Config().max_hours > 0:
            self.mailer.send(booking["user"]["contact"]["email"], "Your lab session starts soon")  # train wreck
            return True
        return False
