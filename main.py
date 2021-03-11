from config import CONFIG
import os
import subprocess

path = os.path.dirname(os.path.realpath(__file__))


for i in range(len(CONFIG)):
    subprocess.Popen(f'python {path}/bot.py "{CONFIG[i][0]}" "{CONFIG[i][1]}" "{CONFIG[i][2]}" "{CONFIG[i][3]}" "{CONFIG[i][4]}"')

