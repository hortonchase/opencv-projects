# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 15:27:04 2020

@author: Chase
"""
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n","--name", required = True, help = "name of user")
args = vars(ap.parse_args())

print("Hi there {}, it's nice to meet you!".format(args["name"]))
