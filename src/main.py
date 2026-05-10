from textnode import *
from functions import *
from htmlnode import *
import os
import shutil
import sys

#print("hello world")



def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    print(f"Basepath: {basepath}")
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_files_over("static","docs")
    generate_pages_recursive(basepath,"content", "template.html","docs")

main()

