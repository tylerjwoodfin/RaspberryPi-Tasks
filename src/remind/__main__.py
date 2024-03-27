"""
The main entrypoint
"""

import argparse

from . import reminder_manager
from . import query_manager

def handle_args(manager_r: reminder_manager.ReminderManager, manager_q: query_manager.QueryManager) -> None:
    """
    Parse arguments passed to RemindMail
    """

    parser = argparse.ArgumentParser(description="A tool to schedule and organize reminders")

    parser.add_argument("-ls",
        "--list",
        action="store_true",
        help="list all reminders",
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="generate reminders.",
    )
    parser.add_argument("--later",
        action="store_true",
        help="show reminders scheduled for later"
    )
    parser.add_argument(
        "-e",
        "--edit",
        action="store_true",
        help="edits the remindmail file")
    parser.add_argument("-sw",
        "--show-week",
        action="store_true",
        help="show reminders through next 7 days",
    )

    try:
        args = parser.parse_args()

        if args.list:
            manager_r.print_reminders_file()
        elif args.generate:
            manager_r.generate()
        elif args.later:
            manager_r.show_later()
        elif args.edit:
            manager_r.edit_reminders_file()
        elif args.show_week:
            manager_r.show_week()
        else:
            manager_q.wizard_manual_reminder()

    except KeyboardInterrupt as exc:
        raise KeyboardInterrupt from exc

def main():
    """
    The main function
    """

    manager_remind = reminder_manager.ReminderManager()
    manager_query = query_manager.QueryManager(manager_remind)

    try:
        handle_args(manager_remind, manager_query)
    except KeyboardInterrupt:
        print("\n")

if __name__ == "__main__":
    main()
