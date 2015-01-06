#!/usr/bin/python3

"""A simple script to be able to use latexmk through pipes. Inspired from rubber-pipe."""

import glob
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
    initial_dir = os.getcwd()

    logging.basicConfig(level=logging.INFO)

    # create temporary file
    filename = make_name()
    src = filename + ".tex"

    with open(src, 'w') as src_file:
        logging.info("temporary file is " + src)
        dump_file(sys.stdin, src_file)

    # call latexmk with options
    options = ' '.join(sys.argv[1:])

    try:
        subprocess.check_call("latexmk " + options + " " + src,
                              stdin=None,
                              stdout=sys.stderr.buffer,
                              shell=True)
    except subprocess.CalledProcessError:
        logging.critical("problem with latexmk!")
        sys.exit(1)

    # dump output file on standard output
    with  open(filename + ".log", 'r') as log_file:
        print(log_file)
        log_text = log_file.read()

    output_file_pattern = re.compile(r"Output written on (\w+\.\w+).*")

    with open(output_file_pattern.search(log_text).group(1), 'rb') as output_file:
        for byte in output_file:
            sys.stdout.buffer.write(byte)

    # clean temporary files
    for temp_file in glob.glob(filename + "*"):
        os.remove(temp_file)
