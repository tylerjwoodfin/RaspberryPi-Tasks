# remindmail

- turns reminders written in terminal into emails; integrates with Google Assistant; supports scheduled reminders

## features

- easily manage your To Do list from anywhere in the terminal
- schedule one-time or recurring reminders
- automatically sync scheduled reminders as a plaintext file with Dropbox, Google Drive, Nextcloud, or any other Cloud Storage provider using [rclone](https://rclone.org/install/)

# dependencies

- Linux (Raspberry Pis work great!)
- [securedata](https://github.com/tylerjwoodfin/securedata)
- a unique, non-Gmail address specifically for this project
  - do not use an email address that you use in other areas of your life
  - do not re-use a password you've used anywhere else; use a unique password.
- Python3

# setup

- install Python3
- install [securedata](https://github.com/tylerjwoodfin/securedata)

  - initialize using `securedata config`; see securedata's README for complete setup instructions
  - in securedata's `settings.json`, set the full directory path of your `remind.md` file using `path -> remindmail -> local`
  - in securedata's `settings.json`, set the email information using the example below
    - note that Gmail will _not_ work due to their security restrictions.
    - it's very bad practice to store your password in plaintext; for this reason, never sync this file.
    - always use a unique email address specifically for this, and _especially_ use a unique password.
    - an example working client id and secret can be found [here](https://github.com/jonahar/google-reminders-cli/blob/master/app_keys.json)
  - Your `settings.json` should be similar to this:

  ```
  {
    "path": {
      "remindmail": {
        "local": "/home/pi/remindmail"
      }
    },
    "email": {
        "from": "YourUniqueAndNonGmailEmailAddress",
        "from_pw": "YourPassword",
        "from_name": "Your Name",
        "to": "RemindersSentToThisEmailAddress",
        "smtp_server": "your domain's smtp server",
        "imap_server": "your domain's imap server",
        "port": 465
    },
    "tasks": {
      "client_id": "Your client ID",
      "client_secret": "Your client secret"
    }
  }
  ```

- follow the `remind.md` section below

# usage

- natural language, e.g. `remindmail take the trash out on thursday`
  - I recommend aliasing `remindmail` to `remind`; then, something like `remind me to take the trash out on Thursday` should parse properly.
- scheduling `remindmail pull` to automatically pull reminders from Google through crontab (see below)
- scheduling `remindmail generate` to automatically send emails based on date match from `remind.md` (see below)

# generate

- generates reminders from `remind.md` (see below)

# pull

- generates reminders from Google

## syncing with rclone (optional)

- complete the steps above in "Setup"
- install [rclone](https://rclone.org/install/).
- run `rclone config` to set up a cloud storage provider of your choice
- set the full directory path of your cloud using `securedata`; set `path -> remindmail -> cloud` (see `Setup` for an example)

## scheduling reminder checks:

- type "crontab -e" in the terminal

- add the line below (without the >, without the #, replacing the path with your real path):
  - `0 * * * * python3 path/to/main.py generate` (every hour, generate based on remind.md)
  - `*/5 * * * * python3 path/to/main.py pull` (every 5 minutes, query Google for new reminders)

# logging

- by defualt, remindmail's log path is set to `securedata`'s default log
- otherwise, you can set `path -> remindmail -> log` in `securedata` (see Setup above) for a custom directory.

# scheduling reminders with remind.md

- this file is the heart of this tool, used for scheduling one-time or recurring reminders.
- place the "good" example in the `remind.md example` section below in a file named `remind.md`.
- reminders from the `remind.md` file will be emailed once the conditions are met.

## using colons to edit email body

- any text after a colon (`:`) will be placed in the body of the email.

## using natural language to add to remind.md

- `remindmail take out the trash` will immediately send an email upon confirmation
- `remindmail take out the trash tomorrow` will add `[YYYY-MM-DD]d take out the trash` upon confirmation (where `YYYY-MM-DD` is tomorrow's date)
- `remindmail take out the trash on Thursday` will add `[thu]d take out the trash` upon confirmation
- `remindmail take out the trash on the 13th` will add `[YYYY-MM-13]d take out the trash` upon confirmation (where `YYYY-MM-13` is the next `13th`)
- `remindmail take out the trash every 2 weeks` will add `[W%2] take out the trash` upon confirmation (TODO!)
- try other combinations, and feel free to contribute to the codebase for other scenarios!

## manually editing remind.md to schedule reminders

### days

```
[D%1]         This reminder is sent every day.
[D%4]         This reminder is sent every 4 days.

[mon]         This reminder is sent if today is Monday.
[Monday]      This reminder is sent if today is Monday.
[thu]         This reminder is sent if today is Thursday.
[Thursday]d   This reminder is sent, then deleted, if today is Thursday.
[D01]         This reminder is sent if today is the 1st of the month.
[D31]d        This reminder is sent, then deleted, if today is the 31st of the month.

[3-5]         This reminder is sent if today is March 5.
[3/5]d        This reminder is sent if today is March 5.
[2022-3-5]d   This reminder is sent, then deleted, if today is March 5.
```

### weeks

```
[W%3]         This reminder is sent if today is a Sunday of every third week, based on Epoch Time. See below...
[thu%2]       This reminder is sent every other Thursday.
[thu%2+1]     This reminder is sent every other Thursday (between the weeks of the line above).
[W%3+1]       This reminder is sent if today is a Sunday of every third week, _with an offset of 1_, meaning if [W%3] would normally be sent last week, it will be sent this week instead.
```

### months

```
[M%5]         This reminder is sent every 5 months (_not necessarily May and October! pay attention to offsets_)
[M%2]d        This reminder is sent at the next even-numbered month, then deleted.
```

### examples that won't work

```
[D50]         Months only have up to 31 days.
[D%3] d       The 'd' operator must be immediately next to the ] symbol.
[Y%5]         Year is unsupported.
(thu)         You must use brackets.
{thu}         You must use brackets.
   [W%3]      You must start reminders on the first column.
[W%3-1]       This is invalid. To add an offset, you MUST use +.
[W%3+4]       An offset of 4 makes no sense and won't be triggered because [W%3+3] is the same thing as [W%3+0]. Use [W%3+1] instead.

```

## calculating and scheduling "every n weeks", "every n days", "every n months"

- `remindmail offset <type> <date (YYYY-MM-DD, optional)> <n>`
- (`type` is day, week, month)
- (`n` is 'every `n` days')

- Take the results of this function and use it to add an offset.

  - If you want something to happen every 3 days starting tomorrow, use:
  - remindmail offset day <tomorrow's date YYYY-MM-DD> 3

  - If the answer is 2, then you can add this to remind.md:
  - [D%3+2] Description here

### how this is calculated

- The Epoch time is the number of seconds since January 1, 1970, UTC.
- For example, if the current time is 1619394350, then today is Sunday, April 25, 2021 at 11:45:50PM UTC.
- The "week number" is calculated by {epochTime}/60/60/24/7.
  - 1619394350 /60/60/24/7 ~= 2677
  - 2677 % 3 == 1, meaning scheduling a reminder for [W%3] would be sent last week, but not this week (or next week or the week after).

## offset examples

- e.g. `remindmail offset day 2022-12-31 12`
- (find offset for every 12 days intersecting 2022-12-31)

- e.g. `remindmail offset week 2022-12-31 3`
- (every 3 weeks intersecting 2022-12-31)

- e.g. `remindmail offset month 2022-12-31 4`
- (every 4 months intersecting 2022-12-31)

- e.g. `remindmail offset day 5`

  - (every 5 days intersecting today)

- e.g. `remindmail offset week 6`

  - (every 6 weeks intersecting today)

- e.g. `remindmail offset month 7`
  - (every 7 months intersecting today)"""

## using "d" to set one-time reminders:

- an item with `]d`, such as `[D%5]d`, will add the reminder and remove it from remind.md, meaning it will only generate once until you add it again.
  - this is useful for scheduling a reminder in the future that you don't need to repeat.

# credit

- Google polling forked from [https://github.com/jonahar/google-reminders-cli](https://github.com/jonahar/google-reminders-cli)
