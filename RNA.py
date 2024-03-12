import sys
import os
with open(f"{sys.argv[1]}","r") as f:
    print(f"RNA:{f.readlines()}")