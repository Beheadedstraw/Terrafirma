#!/usr/bin/python

import oyaml as yaml

#with open(sys.argv[1], "r") as file:
with open("main.yaml", "r") as file:
    y = yaml.safe_load(file)

for t in y:
    print(t)

#if y['START']:
#    START(y)


 