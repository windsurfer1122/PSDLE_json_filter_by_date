#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: nil; py-indent-offset: 4 -*-
### ^^^ see https://www.python.org/dev/peps/pep-0263/

###
### PSDLE_json_filter_by_date.py (c) 2019 by "windsurfer1122"
### Filter PSDLE JSON exports on purchase date or release date.
###
### For options execute: PSDLE_json_filter_by_date.py -h and read the README.md
###
### git master repository at https://github.com/windsurfer1122
### Read README.md for more information including Python requirements and more
###
### Python 2 backward-compatible workarounds:
### - handle prefix in kwargs manually
### - set system default encoding to UTF-8
### - define unicode() for Python 3 like in Python 2 (ugly)
###
### Adopted PEP8 Coding Style: (see https://www.python.org/dev/peps/pep-0008/)
### * (differs to PEP8) Studly_Caps_With_Underscores for global variables
### * (differs to PEP8) mixedCase for functions, methods
### * lower_case_with_underscores for attributes, variables
### * UPPER_CASE_WITH_UNDERSCORES for constants
### * StudlyCaps for classes
###

###
### This program is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <https://www.gnu.org/licenses/>.
###

### Python 2 future-compatible workarounds: (see: http://python-future.org/compatible_idioms.html)
## a) prevent interpreting print(a,b) as a tuple plus support print(a, file=sys.stderr)
from __future__ import print_function
## b) interpret all literals as unicode
from __future__ import unicode_literals


## Version definition
## see https://www.python.org/dev/peps/pep-0440/
__version__ = "2019.08.10"
__author__ = "https://github.com/windsurfer1122/PSDLE_json_filter_by_date"
__license__ = "GPL"
__copyright__ = "Copyright 2019, windsurfer1122"


## Imports
import sys
import io
import locale
import os
import argparse
import traceback
import json
import datetime


## Debug level for Python initializations (will be reset in "main" code)
Debug_Level = 0


## Error and Debug print to stderr
## https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):  ## error print
    ## Python 2 workaround: handle prefix in kwargs manually
    #def eprint(*args, prefix="[ERROR] ", **kwargs):  ## Python 3 only
    if "prefix" in kwargs:
        prefix = kwargs["prefix"]
        del kwargs["prefix"]
    else:
        prefix="[ERROR] "
    #
    if not prefix is None \
    and prefix != "":
        print(prefix, file=sys.stderr, end="")
    print(*args, file=sys.stderr, **kwargs)

def dprint(*args, **kwargs):  ## debug print
    if Debug_Level:
        ## Python 2 workaround: handle prefix in kwargs manually
        #def dprint(*args, prefix="[debug] ", **kwargs):  ## Python 3 only
        if "prefix" in kwargs:
            prefix = kwargs["prefix"]
            del kwargs["prefix"]
        else:
            prefix="[debug] "
        #
        if not prefix is None \
        and prefix != "":
            print(prefix, file=sys.stderr, end="")
        print(*args, file=sys.stderr, **kwargs)


## Enhanced TraceBack
## http://code.activestate.com/recipes/52215-get-more-information-from-tracebacks/
## https://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of
    important variables in each frame.
    """
    tb = sys.exc_info()[2]
    stack = []

    while tb:
        stack.append(tb.tb_frame)
        tb = tb.tb_next

    for frame in stack:
        for key, value in frame.f_locals.items():
            if key != "Source":
                continue
            eprint(">>> PKG Source:", end=" ")
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:
                eprint(value, prefix=None)
            except:
                eprint("<ERROR WHILE PRINTING VALUE>", prefix=None)

    traceback.print_exc()


## General debug information related to Python
if Debug_Level >= 1:
    dprint("Python Version", sys.version)

## Python 2/Windows workaround: set system default encoding to UTF-8 like in Python 3
## All results will be Unicode and we want all output to be UTF-8
try:
    reload
except NameError:
    ## Python 3.4+
    from importlib import reload
reload(sys)
if sys.getdefaultencoding().lower() != "utf-8":
    if Debug_Level >= 1:
        dprint("Default Encoding setting from {} to UTF-8".format(sys.getdefaultencoding()))
    sys.setdefaultencoding("utf-8")
if sys.stdout.encoding \
and sys.stdout.encoding.lower() != "utf-8":
    if Debug_Level >= 1:
        dprint("STDOUT Encoding setting from {} to UTF-8".format(sys.stdout.encoding))
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding \
and sys.stderr.encoding.lower() != "utf-8":
    if Debug_Level >= 1:
        dprint("STDERR Encoding setting from {} to UTF-8".format(sys.stderr.encoding))
    sys.stderr.reconfigure(encoding="utf-8")

## General debug information related to Unicode
if Debug_Level >= 1:
    ## List encodings
    dprint("DEFAULT Encoding", sys.getdefaultencoding())
    dprint("LOCALE Encoding", locale.getpreferredencoding())
    dprint("STDOUT Encoding {} Terminal {}".format(sys.stdout.encoding, sys.stdout.isatty()))
    dprint("STDERR Encoding {} Terminal {}".format(sys.stderr.encoding, sys.stderr.isatty()))
    dprint("FILESYS Encoding", sys.getfilesystemencoding())
    value = ""
    if "PYTHONIOENCODING" in os.environ:
        value = os.environ["PYTHONIOENCODING"]
    dprint("PYTHONIOENCODING=", value, sep="")
    ## Check Unicode
    dprint("ö ☺ ☻")

## Python 2/3 workaround: define unicode for Python 3 like in Python 2
## Unfortunately a backward-compatible workaround, as I couldn't find a forward-compatible one :(
## Every string is Unicode
## https://stackoverflow.com/questions/34803467/unexpected-exception-name-basestring-is-not-defined-when-invoking-ansible2
try:
    unicode
except:
    if Debug_Level >= 1:
        dprint("Define \"unicode = str\" for Python 3 :(")
    unicode = str


## Generic Definitions
PYTHON_VERSION = ".".join((unicode(sys.version_info[0]), unicode(sys.version_info[1]), unicode(sys.version_info[2])))
#
CONST_FMT_ISO_DATE_TIME = "%Y-%m-%dT%H:%M:%S%z"  ## see https://docs.python.org/2.7/library/datetime.html#strftime-strptime-behavior


def compareDates(item):
    if Arguments.releasedate:
        if not "releasedate" in item:
            eprint("JSON data does not contain release date (property \"releasedate\"). Cannot filter.")
            sys.exit(2);
        else:
            date = datetime.datetime.strptime(item["releasedate"], CONST_FMT_ISO_DATE_TIME)
    else:
        if not "date" in item:
            eprint("JSON data does not contain purchase date (property \"date\"). Cannot filter.")
            sys.exit(2);
        else:
            date = datetime.datetime.strptime(item["date"], CONST_FMT_ISO_DATE_TIME)

    if Arguments.since:
        if date < Arguments.since:
            return False

    if Arguments.before:
        if date >= Arguments.before:
            return False

    return True


def createArgParser():
    ## argparse: https://docs.python.org/3/library/argparse.html

    ## Create help texts
    help_releasedate = "Compare against release date instead of purchase date"
    help_since = "Extract entries since the given date and time"
    help_before = "Extract entries before the given date and time"
    help_ident = "Create a pretty-printed output with that indent level"
    ## --> Debug
    choices_debug = range(1)
    help_debug = "Debug verbosity level.\n\
  0 = No debug info [default]\n\
  1 = Show debug info"

    ## Create description
    description = "%(prog)s {version}\n{copyright}\n{author}\n\
Filter PSDLE JSON exports on purchase date or release date.".format(version=__version__, copyright=__copyright__, author=__author__)

    ## Create epilog
    epilog = "All date-times have to be formatted as following <YYYY>-<MM>-<DD>T<HH>:<MM>:<SS>Z (ISO 8601), e.g 2019-08-23T15:36:12Z"

    ## Build Arg Parser
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument("file", metavar="<PSDLE JSON file>", help="Path to PSDLE JSON file")
    parser.add_argument("--releasedate", action="store_true", help=help_releasedate)
    parser.add_argument("--since", metavar="DATE-TIME", type=unicode, help=help_since)
    parser.add_argument("--before", metavar="DATE-TIME", type=unicode, help=help_before)
    parser.add_argument("--ident", metavar="LEVEL", type=int, default=-1, help=help_ident)
    parser.add_argument("--debug", "-d", metavar="LEVEL", type=int, default=0, choices=choices_debug, help=help_debug)

    return parser


## Global code
if __name__ == "__main__":
    try:
        ## Check parameters from command line
        Parser = createArgParser()
        Arguments = Parser.parse_args()
        ## Global Debug [Verbosity] Level: can be set via '--debug='/'-d'
        Debug_Level = Arguments.debug
        ## Since ISO Date Time String
        if not Arguments.since is None:
            Arguments.since = datetime.datetime.strptime(Arguments.since, CONST_FMT_ISO_DATE_TIME)
        ## Before ISO Date Time String
        if not Arguments.before is None:
            Arguments.before = datetime.datetime.strptime(Arguments.before, CONST_FMT_ISO_DATE_TIME)
        ## ISO Date Time Strings
        if Arguments.since is None \
        and Arguments.before is None:
            eprint("Please specify at least a since and/or a before date.")
            Parser.print_help()
            sys.exit(1);

        ## Read file
        Input_Stream = io.open(Arguments.file, mode="rt", buffering=-1, encoding="utf-8", errors="backslashreplace", newline=None, closefd=True)
        Json_Data = json.load(Input_Stream)
        Input_Stream.close()
        ## Filter JSON data inplace (via [:] slicing)
        Json_Data["items"][:] = [item for item in Json_Data["items"] if compareDates(item)]
        ## Export result as JSON again
        print(json.dumps(Json_Data, ensure_ascii=False, indent=Arguments.ident if Arguments.ident >= 0 else None))
    except SystemExit:
        raise  ## re-raise/throw up (let Python handle it)
    except:
        print_exc_plus()
