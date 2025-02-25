#!/usr/bin/python3

import os
import subprocess
from datetime import datetime, timedelta

def get_user_input():
    username = input("Enter your GitHub username: ")
    email = input("Enter your GitHub email: ")
    return username, email

def setup_git_config(username, email):
    subprocess.run(["git", "config", "user.name", username])
    subprocess.run(["git", "config", "user.email", email])

def commit_on_dates(dates):
    for commit_date in sorted(dates):
        date_str = commit_date.strftime("%Y-%m-%d")
        with open("dummy.txt", "a") as f:
            f.write(f"Commit for {date_str}\n")
        subprocess.run(["git", "add", "dummy.txt"])
        subprocess.run(["git", "commit", "--date", f"{date_str}  10:00:00 -0700", "-m", f"Commit on {date_str}"])
        # debug mode:
        #print("git", "commit", "--date", f"{date_str} 10:00:00 -0700", "-m", f"Commit on {date_str}")
        #input()

def main():
    username, email = get_user_input()
    setup_git_config(username, email)
    
    start_date = datetime(2024, 1, 7)  # First Sunday of full week 2024
    
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
    
    commit_on_dates(commit_dates)
    
    print("All commits have been created. Push your changes using 'git push origin main'.")

if __name__ == "__main__":
    main()
