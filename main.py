import os
import re
import json
from pyswip import Prolog
from collections import defaultdict

prolog = Prolog()
base = defaultdict(list)

while True:
    filename = input("Enter a name of a prolog file to parse: ")
    if filename == "q":
        break
    try:
        with open(filename) as f:
            prolog.consult(filename)
            line = f.readline()
            while line:
                if re.match("^[A-Za-z0-9]+\(([A-Za-z0-9]*\,)*([A-Za-z0-9])*\).$", line.replace("\n", '').replace(" ", '')):
                    base["F"].append(line.replace("\n", '').replace(" ", ''))
                elif re.match("^[A-Za-z0-9]+\(([A-Za-z0-9]*\,)*([A-Za-z0-9])*\)\:\-((.+),)*(.)*\.$", line.replace("\n", '').replace(" ", '')):
                    base["R"].append(line.replace("\n", '').replace(" ", ''))
                line = f.readline()

        while True:
            question = input("Enter Prolog question for chosen file: ")
            if question == "q":
                print(json.dumps(base, indent=1))
                base.clear()
                break
            try:
                if not bool(list(prolog.query(question))):
                    print("No")
            except:
                print("question is incorrect")
                continue
            base["P"].append(question)
            for q in prolog.query(question):
                if not q:
                    print("Yes")
                else:
                    print(q)
    except FileNotFoundError:
        print("File {} does not exist".format(filename))
