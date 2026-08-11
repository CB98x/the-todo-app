from datetime import datetime, timedelta
from reminders import is_due_in_window, send_email, check_and_send_reminders

#due tomorrow
def test_is_due_in_window_returns_true_when_due_in_24h():
    todo = {"title":"atodo", "due_date":"2026-06-02", "done":False} 
    now = datetime(2026, 6, 1, 6,0)
    result = is_due_in_window(todo, now)
    assert result == True

# due next week → expect False (out of window)
def test_is_due_in_window_returns_false_when_due_next_week():
    todo = {"title":"atodo", "due_date":"2026-06-09", "done":False} 
    now = datetime(2026, 6, 1, 6,0)
    result = is_due_in_window(todo, now)
    assert result == False

# exactly 23 hours → boundary
def test_is_due_in_window_returns_true_when_due_in_23h():
    todo = {"title":"atodo", "due_date":"2026-06-02", "done":False} 
    now = datetime(2026, 6, 1, 7,0)
    result = is_due_in_window(todo, now)
    assert result == True

# exactly 25 hours → boundary
def test_is_due_in_window_returns_true_when_due_in_25h():
    todo = {"title":"atodo", "due_date":"2026-06-02", "done":False} 
    now = datetime(2026, 6, 1, 5,0)
    result = is_due_in_window(todo, now)
    assert result == True

def test_is_due_in_window_returns_false_when_due_in_25h_1min():
    todo = {"title":"atodo", "due_date":"2026-06-02", "done":False} 
    now = datetime(2026, 6, 1, 4,59)
    result = is_due_in_window(todo, now)
    assert result == False

# exactly 22.9 hours → boundary
def test_is_due_in_window_returns_false_when_due_in_22h_59min():
    todo = {"title":"atodo", "due_date":"2026-06-02", "done":False} 
    now = datetime(2026, 6, 1, 7, 1)
    result = is_due_in_window(todo, now)
    assert result == False

#check email sending functionality
def test_send_email_calls_smtp(monkeypatch):
    #arrange
    sent = {}
    class FakeServer:
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def login(self, user, pw): pass
        def send_message(self, msg):
            sent["msg"] = msg

    def fake_smtp(host, port):
        return FakeServer()

    monkeypatch.setattr("reminders.smtplib.SMTP_SSL", fake_smtp)

    #act
    send_email("Test subject", "Test Body")

    #assert
    assert sent["msg"]["Subject"] == "Test subject"
    assert sent["msg"].get_content().strip() == "Test Body"

def test_check_and_send_reminders_sends_when_due(monkeypatch):
    # ARRANGE
    fake_todos = [
        {"title": "pay rent", "due_date": "2026-06-02", "done": False}
    ]

    # fake get_task_list -> hand back our list, no file
    monkeypatch.setattr("reminders.get_task_list", lambda: fake_todos)

    # fake is_due_in_window -> always True, no clock
    monkeypatch.setattr("reminders.is_due_in_window", lambda todo: True)

    # fake update_task_list -> do nothing, no file write
    monkeypatch.setattr("reminders.update_task_list", lambda todos: None)

    # fake send_email -> RECORD the call
    calls = []
    def fake_send_email(subject, body):
        calls.append((subject, body))
    monkeypatch.setattr("reminders.send_email", fake_send_email)

    # ACT
    check_and_send_reminders()

    # ASSERT
    assert len(calls) == 1

def test_check_and_do_not_send_reminders_when_done(monkeypatch):
    # ARRANGE
    fake_todos = [
        {"title": "pay rent", "due_date": "2026-06-02", "done": True}
    ]

    # fake get_task_list -> hand back our list, no file
    monkeypatch.setattr("reminders.get_task_list", lambda: fake_todos)

    # fake is_due_in_window -> always True, no clock
    monkeypatch.setattr("reminders.is_due_in_window", lambda todo: True)

    # fake update_task_list -> do nothing, no file write
    monkeypatch.setattr("reminders.update_task_list", lambda todos: None)

    # fake send_email -> RECORD the call
    calls = []
    def fake_send_email(subject, body):
        calls.append((subject, body))
    monkeypatch.setattr("reminders.send_email", fake_send_email)

    # ACT
    check_and_send_reminders()

    # ASSERT
    assert len(calls) == 0

def test_check_and_do_not_send_reminders_when_not_due(monkeypatch):
    # ARRANGE
    fake_todos = [
        {"title": "pay rent", "due_date": "2026-06-02", "done": False}
    ]

    # fake get_task_list -> hand back our list, no file
    monkeypatch.setattr("reminders.get_task_list", lambda: fake_todos)

    # fake is_due_in_window -> False, no clock
    monkeypatch.setattr("reminders.is_due_in_window", lambda todo: False)

    # fake update_task_list -> do nothing, no file write
    monkeypatch.setattr("reminders.update_task_list", lambda todos: None)

    # fake send_email -> RECORD the call
    calls = []
    def fake_send_email(subject, body):
        calls.append((subject, body))
    monkeypatch.setattr("reminders.send_email", fake_send_email)

    # ACT
    check_and_send_reminders()

    # ASSERT
    assert len(calls) == 0

def test_check_and_do_not_send_reminders_sends_smtp_error(monkeypatch):
    # ARRANGE
    fake_todos = [
        {"title": "pay rent", "due_date": "2026-06-02", "done": False}
    ]

    # fake get_task_list -> hand back our list, no file
    monkeypatch.setattr("reminders.get_task_list", lambda: fake_todos)

    # fake is_due_in_window -> always True, no clock
    monkeypatch.setattr("reminders.is_due_in_window", lambda todo: True)

    # fake update_task_list -> do nothing, no file write
    monkeypatch.setattr("reminders.update_task_list", lambda todos: None)

    # fake send_email -> raise the Exception
    def fake_send_email(subject, body):
        raise Exception("smtp down")
    monkeypatch.setattr("reminders.send_email", fake_send_email)

    # ACT + ASSERT
    # send_email raises. If the except block works, this call returns normally.
    # If the except block were missing, this line would raise and fail the test.
    check_and_send_reminders()