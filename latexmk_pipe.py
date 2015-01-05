#!/usr/bin/python3

"""A simple script to be able to use latexmk through pipes. Inspired from rubber-pipe."""

import logging
import os
import re
import subprocess
import sys

re_latexmktmp = re.compile("latexmktmp(?P<num>[0-9]+)\\.")

def make_name ():
    """Return a base name suitable for a new compilation in the current
    directory. The name will have the form "latexmktmp" plus a number,
	such that no file of this prefix exists.
	"""
    num = 0
    for my_file in os.listdir("."):
        m = re_latexmktmp.match(my_file)
        if m:
            num = max(num, int(m.group("num")) + 1)
    return "latexmktmp%d" % num

def dump_file (f_in, f_out):
    """
	Dump the contents of a file object into another.
	"""
    for line in f_in.readlines():
        f_out.write(line)

if __name__ == '__main__':

    path = []
    place = "."
    initial_dir = os.getcwd()

    logging.basicConfig(level=logging.INFO)

    # create temporary file

    if place is not None and place != ".":
        path.insert(0, initial_dir)
        os.chdir(place)

    src = make_name()

    try:
        srcfile = open(src + ".tex", 'w')
    except IOError:
        logging.critical("cannot create temporary files!")
        sys.exit(1)

    logging.info("temporary file used is " + src + ".tex")
    dump_file(sys.stdin, srcfile)

    # call latexmk with options
    options = ' '.join(sys.argv[1:])

    try:
        subprocess.check_call("latexmk " + options + src + ".tex",
                              stdin=None, shell=True)
    except subprocess.CalledProcessError:
        logging.critical("problem with latexmk!")
        sys.exit(1)

    # clean
    srcfile.close()
