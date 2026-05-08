from textnode import *
from functions import *
from htmlnode import *
import os
import shutil

#print("hello world")

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_files_over("static","public")
    generate_page("content/index.md","template.html","public/index.html")
    


main()

