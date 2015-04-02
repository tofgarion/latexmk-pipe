#!/usr/bin/python3

"""A simple script to be able to use latexmk through pipes. Inspired
by rubber-pipe."""

import glob
import logging
import os
import re
import subprocess
import sys

RE_LATEXMKTMP = re.compile("latexmktmp(?P<num>[0-9]+)\\.")
RE_OUTDIR = re.compile("-outdir=(.*)")

def make_name(output):
    """Return a base name suitable for a new compilation in the output
    directory. The name will have the form "latexmktmp" plus a number,
    such that no file of this prefix exists."""

    num = 0
    for my_file in os.listdir(output):
        my_match = RE_LATEXMKTMP.match(my_file)
        if my_match:
            num = max(num, int(my_match.group("num")) + 1)
    return "latexmktmp%d" % num

def dump_file(f_in, f_out):
    """Dump the contents of a file object into another."""

    for line in f_in.readlines():
        f_out.write(line)

def call_latexmk():
    """Create temporary LaTeX file, call latexmk and clean temporary
    files."""

    logging.basicConfig(level=logging.INFO)
    output = "." + os.sep

    # find options, particularly -output=DIR option
    for option in sys.argv[1:]:
        match = RE_OUTDIR.match(option)
        if match:
            output = match.group(1) + os.sep
            logging.info("output dir is " + output)

    options = ' '.join(sys.argv[1:])

    # create temporary file
    filename = make_name(output)
    src = output + filename + ".tex"

    with open(src, 'w') as src_file:
        logging.info("temporary file is " + src)
        dump_file(sys.stdin, src_file)

    # call latexmk with options
    try:
        subprocess.check_call("latexmk " + options + " " + src,
                              stdin=None,
                              stdout=sys.stderr.buffer,
                              shell=True)
    except subprocess.CalledProcessError:
        logging.critical("problem with latexmk!")
        sys.exit(1)

    # dump output file on standard output
    with open(output + filename + ".log", 'r', encoding='latin1') as log_file:
        log_text = log_file.read()

    output_file_pattern = re.compile(r"Output written on (" + output +
                                     "*\w+\.\w+).*")

    with open(output_file_pattern.search(log_text).group(1),
              'rb') as output_file:
        for byte in output_file:
            sys.stdout.buffer.write(byte)

    # clean temporary files
    for temp_file in glob.glob(output + filename + "*"):
        os.remove(temp_file)

if __name__ == '__main__':

    call_latexmk()
