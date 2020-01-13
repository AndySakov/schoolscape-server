import sys, os, time, string


def equalRep(filename = 'server.py'):
    file = open(filename, "r")
    cont = file.read()
    cont = cont.replace(" -> ", " = ")
    cont = cont.replace("->", "=")
    cont = cont.replace(" -. ", " + ")
    cont = cont.replace("-.", "+")
    file.close()
    file = open(filename, "w")
    file.write(cont)
    file.close()

for x in os.listdir():
    try:
        if ("comp.py" == x):
            continue
        if ("." in x):
            equalRep(x)
            print("yes")
    except PermissionError:
        continue