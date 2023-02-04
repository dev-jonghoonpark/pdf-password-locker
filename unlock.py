#!/usr/bin/env python
# Encoding: utf8

# Author: Hannes Ovrén (hannes@ovren.se)
# Licensed under the GPL version 2

import getpass
import os
import sys

from PyPDF2 import PdfFileWriter, PdfFileReader

import easygui

def unlock(ifname, ofname, password):
    with open(ifname, "rb") as ifile, open(ofname, "wb") as ofile:
        reader = PdfFileReader(ifile)
        reader.decrypt(password)

        writer = PdfFileWriter()
        for i in range(reader.getNumPages()):
            writer.addPage(reader.getPage(i))
        writer.write(ofile)
        
def get_password():
    while True:
        try:
            password = getpass.getpass("Set password for PDF file: ")
            repeated = getpass.getpass("Repeat password: ")
        except KeyboardInterrupt:
            print # End the password query line
            return None
        if password == repeated:
            return password
        else:
            print("Passwords did not match")

if __name__ == "__main__":
    _input = easygui.fileopenbox()
    _output = "{}_unlocked.pdf".format(_input[:-4])

    if not os.path.exists(_input):
        print("Input file {} does not exist.".format(_input))
        sys.exit(-1)
    if os.path.exists(_output):
        print("Output file {} already exists.".format(_output))
        sys.exit(-2) 

    print("Password: ")
    _password = input()
    
    if _password is not None:
        unlock(_input, _output, _password)
        print("Created {}".format(_output))
