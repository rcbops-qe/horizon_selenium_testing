#!/usr/bin/env python

import json

with open('ile', 'r') as f:
    config = json.load(f)

for k, v in config:
    print k
    print v