#!/usr/bin/env python3

#=====
# Converts a json string from standard in to 
# a json object then takes the key value to 
# extract from the json as an argument and 
# returns the associated value
#=====

import sys, json

try:
    print(json.load(sys.stdin)[sys.argv[1]])
except:
    print("Invalid " + sys.argv[1])