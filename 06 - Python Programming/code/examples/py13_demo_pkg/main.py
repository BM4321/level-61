"""Entry point. Run from this folder: python main.py"""
import sys

from gradebook import summary

print("module __name__ here:", __name__)
print("first sys.path entry:", sys.path[0])
print(summary({"Ali": 71, "Bea": 64, "Chen": 38}))
