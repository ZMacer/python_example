#! /usr/bin/env python
# -*- coding:utf8 -*-

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', action = "store", dest = "username")
parser.add_argument('-p', action = "store", dest = "password")
args = parser.parse_args()

print args.username,args.password