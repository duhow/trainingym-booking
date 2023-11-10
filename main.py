#!/usr/bin/env python3

import argparse
from api import Trainingym
import logging

#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

def print_activities(activities):
    msg = list()
    for act in activities:
        date = act["date"].strftime("%a %d %H:%M")
        txt = f"{act['name']} el {date} ({act['id']})"
        msg.append(txt)
    print("\n".join(msg))


def main():
    parser = argparse.ArgumentParser(description="Login to Trainingym app")
    parser.add_argument("email", help="Email address to use for login")
    parser.add_argument("password", help="Password to use for login")

    args = parser.parse_args()

    trainingym = Trainingym()
    trainingym.login(args.email, args.password)
    print(f"Welcome {trainingym.person_fullname} !")

    print("Next activities:")
    print_activities(trainingym.next_activities())

if __name__ == "__main__":
    main()
