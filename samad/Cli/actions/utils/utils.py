import sys
from termcolor import colored, cprint

war = lambda x: cprint(str(x) + "\n", "red", attrs=["bold"])
ok = lambda x: cprint(str(x) + "\n", "green", attrs=["bold"])
detail = lambda x,y: {cprint(x, "yellow", end = " "), cprint(y, "cyan")}

studentDetails = ["National ID:","Student ID:","Major:","Birth Date:","First name:","Last name:","Balance:"]