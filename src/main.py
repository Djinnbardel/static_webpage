from textnode import *
from functions import *
from htmlnode import *
import os
import shutil
import sys

#print("hello world")



def main():
    if sys.argv is None or sys.argv[0] == "src/main.py":
        basepath = "/"
    else:
        basepath = sys.argv[0]
    print(f"Basepath: {basepath}")
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_files_over("static","docs")
    generate_pages_recursive(basepath,"content", "template.html","docs")

main()

