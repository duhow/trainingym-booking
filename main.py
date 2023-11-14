#!/usr/bin/env python3

import argparse
from api import Trainingym, Dias
import logging
import yaml
from datetime import datetime
from time import sleep

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


def load_yaml(filepath: str = "clases.yaml"):
    activities = dict()
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
        for dia in Dias:
            if dia.name in data.keys():
                activities[dia.value] = data[dia.name]
                activities[dia.value]["start_time"] = datetime.strptime(data[dia.name].get("desde"), "%I%p").time()
    return activities


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

    want_list = load_yaml()
    trainingym.book_activities(want_list)

if __name__ == "__main__":
    main()
