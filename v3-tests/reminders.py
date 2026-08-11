import time
from datetime import datetime, timedelta
from todos import get_task_list, update_task_list

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

RECIPIENT = "chikaruki@gmail.com"

# def is_due_in_window(todo):
#     due_str = todo["due_date"]
#     due_date = datetime.strptime(due_str, "%Y-%m-%d")
#     due_moment = due_date + timedelta(hours=6)
#     now = datetime.now()
#     hours_until_due = (due_moment - now).total_seconds() / 3600
#     print(f"checking {todo['title']}: due in ", end="")
#     print(f"{hours_until_due} hours")
#     return 23 <= hours_until_due <= 25 #test value 0, 48


def is_due_in_window(todo, now = None):
    due_str = todo["due_date"]
    due_date = datetime.strptime(due_str, "%Y-%m-%d")
    due_moment = due_date + timedelta(hours=6)
    if now is None: 
        now = datetime.now()
    hours_until_due = (due_moment - now).total_seconds() / 3600
    print(f"checking {todo['title']}: due in ", end="")
    print(f"{hours_until_due} hours")
    return 23 <= hours_until_due <= 25 #test value 0, 48

def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = RECIPIENT
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)

def check_and_send_reminders():
    todos = get_task_list()
    for todo in todos:
        if todo["done"] or todo.get("reminder_sent", False):
            continue
        if is_due_in_window(todo):
            try:
                subject = f"Reminder: {todo['title']} due tomorrow"
                body = f"Your todo '{todo['title']}' is due {todo['due_date']}."
                send_email(subject, body)
                print(f"[{datetime.now()}] sent reminder for {todo['title']}")
                todo["reminder_sent"] = True
                update_task_list(todos)
            except Exception as e:
                print(f"[{datetime.now()}] FAILED to send reminder for {todo['title']}: {e}")

def main():
    while True:
        check_and_send_reminders()
        time.sleep(3600) #test value 5

if __name__ == "__main__":
    main()
    
# send_email("test from reminders", "if you see this, it works")