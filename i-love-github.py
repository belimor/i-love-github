#!/usr/bin/python3

import os
import subprocess
import pytz
from datetime import datetime, timedelta

def get_user_input():
    default_year = datetime.now().year - 1
    # Read default username and email from git config
    default_username = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True, text=True).stdout.strip()
    default_email = subprocess.run(["git", "config", "--get", "user.email"], capture_output=True, text=True).stdout.strip()
    username = input(f"Enter your GitHub username (default: {default_username}): ") or default_username
    email = input(f"Enter your GitHub email (default: {default_email}): ") or default_email
    year_input = input(f"Enter the year (default is {default_year}): ")
    year = int(year_input) if year_input.isdigit() else default_year
    return username, email, year

def setup_git_config(username, email):
    subprocess.run(["git", "config", "user.name", username])
    subprocess.run(["git", "config", "user.email", email])

def get_timezone_offset():
    tz = datetime.now().astimezone().tzinfo
    offset = tz.utcoffset(datetime.now()).total_seconds() / 3600
    return f"{int(offset):+03d}00"

def get_first_full_week_start(year):
    first_day = datetime(year, 1, 1)
    days_to_sunday = (6 - first_day.weekday()) % 7  # Days to the next Sunday
    first_sunday = first_day + timedelta(days=days_to_sunday)
    # Ensure it starts within the first 7 days of January
    return first_sunday if first_sunday.day <= 7 else first_sunday + timedelta(days=7)

def commit_on_dates(dates, timezone_offset):
    for commit_date in sorted(dates):
        date_str = commit_date.strftime("%Y-%m-%d")
        with open("dummy.txt", "a") as f:
            f.write(f"Commit for {date_str}\n")
        subprocess.run(["git", "add", "dummy.txt"])
        subprocess.run(["git", "commit", "--date", f"{date_str}  10:00:00 {timezone_offset}", "-m", f"Commit on {date_str}"])
        # Debug:
        # print("git", "commit", "--date", f"{date_str} 10:00:00 {timezone_offset}", "-m", f"Commit on {date_str}")
        # input()

def main():
    username, email, year = get_user_input()
    setup_git_config(username, email)
    timezone_offset = get_timezone_offset()
    
    start_date = get_first_full_week_start(year)
    # Debug:
    # print(start_date)
    
    matrix = [
        "###    #   #     ####  ### ##### #   # #   # ####  ",
        " #    ### ###   #    #  #    #   #   # #   # #   # ",
        " #   #########  #       #    #   #   # #   # #   # ",
        " #    #######   #  ###  #    #   ##### #   # ####  ",
        " #     #####    #    #  #    #   #   # #   # #   # ",
        " #      ###     #    #  #    #   #   # #   # #   # ",
        "###      #       ####  ###   #   #   #  ###  ####  "
    ]
    
    commit_dates = []
    for x, row in enumerate(matrix):
        for y, char in enumerate(row):
            if char == "#":
                #print(start_date + timedelta(days=x + y * 7))
                #input()
                commit_dates.append(start_date + timedelta(days=x + y * 7))
    
    commit_on_dates(commit_dates, timezone_offset)
    
    print("All commits have been created. Push your changes using 'git push origin main'.")

if __name__ == "__main__":
    main()
