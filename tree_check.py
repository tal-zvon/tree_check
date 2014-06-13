#!/usr/bin/python
__author__ = 'tal'

import sys
import os
import textwrap
import signal

GIT = False
#The root of the git repo
GIT_ROOT = '.'
#True if git root must be specified explicitly
GIT_REQ = False
DIR = '.'


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def signal_handler(signal, frame):
    print Color.END
    exit(0)


def usage():
    print Color.BOLD + "NAME" + Color.END
    print '\t%s - do a tree of specified folders' % os.path.basename(sys.argv[0])
    print ''
    print Color.BOLD + "DESCRIPTION" + Color.END
    print '\tRun the "tree" command in a way that:'
    print '\t    * Uses the ANSII standard to make it easily grepable'
    print '\t    * Shows dir and file sizes in a human readable way'
    print '\ton any folders passed to %s as arguments, and' % os.path.basename(sys.argv[0])
    print '\twrites the output to a file with the same name in the CWD.'
    print '\tNOTE: %s does NOT write anything to stdout!' % os.path.basename(sys.argv[0])
    print
    print '\t%s can also create folders to store the output' % os.path.basename(sys.argv[0])
    print '\tin any way you like.'
    print
    print '\t' + Color.BOLD + '-f OUTPUT_FOLDER' + Color.END
    print '\t\t' + '\n\t\t'.join(textwrap.wrap(
        'Output folder name. Can be used more than once. All output is stored in the folder specified by the last -f statement used. If -f is omitted, output is stored in the current directory. To specify the current directory explicitly, use "-f ." See examples for details.',
        60))
    print
    print '\t' + Color.BOLD + '-g' + Color.END + '[=GIT_ROOT_DIR]'
    print '\t\t' + '\n\t\t'.join(textwrap.wrap(
        'Enable git. After generating output, runs "git add ." and "git commit -m $(date)" on the output folder. The GIT_ROOT_FOLDER specifies where the root of the git repo will be. When using relative paths for -f options, the GIT_ROOT_FOLDER is assumed to be the CWD if the =GIT_ROOT_FOLDER is omitted. When using absolute paths for -f, the GIT_ROOT_FOLDER MUST be specified.', 60))
    print
    print '\t' + Color.BOLD + '-h, --help' + Color.END
    print '\t\t' + '\n\t\t'.join(textwrap.wrap('Display this help and exit', 60))
    print
    print '\t' + Color.BOLD + "Exit status:" + Color.END
    print '\t    0  if OK'
    print '\t    1  if Errors caused an early exit'
    print
    print Color.BOLD + "EXAMPLES" + Color.END
    print '\tRun tree on /etc, and put the output into the current folder:'
    print '\t    $ %s /etc' % os.path.basename(sys.argv[0])
    print
    print '\tRun tree on /etc, and put the output into a folder called PC1:'
    print '\t    $ %s -f PC1 /etc' % os.path.basename(sys.argv[0])
    print
    print '\tRun tree on /etc, and put the output into the current folder.'
    print '\tAlso run tree on "/SOME FOLDER" and put the output into the folder'
    print '\tcalled "Machine 2":'
    print '\t    $ %s /etc -f Machine\ 2 /SOME\ FOLDER' % os.path.basename(sys.argv[0])
    print '\tOR'
    print '\t    $ %s /etc -f "Machine 2" "/SOME FOLDER"' % os.path.basename(sys.argv[0])
    print
    print '\tRun tree on /etc, and put the output into the current folder.'
    print '\tThen run tree on /var and /usr, and put the output of both into'
    print '\ta folder called PC1.'
    print '\tFinally run tree on /home, and put the output into the current'
    print '\tfolder too.'
    print '\t    $ %s /etc -f PC1 /var /usr -f . /home' % os.path.basename(sys.argv[0])
    print
    print '\tRun tree on /etc, and make the output folder\n\t"/home/user/Documents/test folder/Machine 1".'
    print '\tRun tree on /var, and make the output folder\n\t"/home/user/Documents/test folder/Machine 2".'
    print '\tSet the git repo root folder to "/home/user/Documents/test folder/",\n\tand make a git snapshot.'
    print '\tNote: In this case, the "/home/user/Documents/test folder/"\n\tdir must already exist'
    print '\t    $ %s -f "/home/user/Documents/test folder/Machine 1" \\\n\t\t/etc -f "/home/user/Documents/test folder/Machine 2" /var \\\n\t\t"-g=/home/user/Documents/test folder"' % os.path.basename(sys.argv[0])
    print
    print Color.BOLD + "AUTHOR" + Color.END
    print '\tWritten by Tal.'
    print
    print Color.BOLD + "REPORTING BUGS" + Color.END
    print '\tReport %s bugs to Tal\'s GitHub repo.' % os.path.basename(sys.argv[0])
    print
    print Color.BOLD + "LICENSE" + Color.END
    print '\tGPLv2 - http://www.gnu.org/licenses/gpl-2.0.html'
    print

#If user hits Ctrl+C, make sure the terminal colors are back to normal
signal.signal(signal.SIGINT, signal_handler)

#If there are no arguments, show usage and exit
if len(sys.argv) == 1:
    usage()
    exit(0)

#Check for invalid arguments
for i in range(1, len(sys.argv)):

    #If one of the arguments is '-g', enable git
    if sys.argv[i][:2] == "-g":
        if len(sys.argv[i]) > 2:
            #Make sure the extended version of -g (-g=) is formatted correctly
            if len(sys.argv[i]) == 3:
                print "Invalid formatting: '%s'" % sys.argv[i]
                exit(1)
            elif len(sys.argv[i]) > 3:
                if sys.argv[i][2] != "=":
                    print "Invalid formatting: '%s'" % sys.argv[i]
                    exit(1)

            #Assign root directory for git to GIT_ROOT
            GIT_ROOT = sys.argv[i][3:]

        GIT = True
        continue

    #If one of the arguments is '-h' or '--help', show help and exit
    if sys.argv[i] == "-h" or sys.argv[i] == "--help":
        usage()
        exit(0)

    #If one of the arguments is '-f', make sure it's not the last argument
    if sys.argv[i] == "-f":
        #Check if this is the last argument
        if i == (len(sys.argv) - 1):
            print "'-f' cannot be the last argument!\n"
            usage()
            exit(1)

        #Check if this is the second last argument
        if i == (len(sys.argv) - 2):
            print "'-f %s' cannot be the last argument!\n" % sys.argv[i + 1]
            usage()
            exit(1)

        #Check if next argument starts with a /
        if sys.argv[i + 1][:1] == "/":
            GIT_REQ = True
            #Check if dirname of the following argument exists
            if not os.path.isdir(os.path.dirname(sys.argv[i + 1])):
                print "You are using an absolute path. '%s' must exist!" % os.path.dirname(sys.argv[i + 1])
                exit(1)

        #Skip to the next arg
        continue

    #Check if the folder exists
    if not os.path.isdir(sys.argv[i]):
        #Check if '-f' was the previous argument
        if sys.argv[i - 1] != '-f':
            print "'%s' is not a valid folder!" % sys.argv[i]
            exit(1)

#Check if git is required, and if it was specified
if GIT_REQ and GIT_ROOT == '.':
    print "You are using absolute paths for your output"
    print "You must specify the root of your git repo explicitly with '-g=/some_folder'"
    exit(1)

#For every argument, run tree on it and send the output where it needs to go
for i in range(1, len(sys.argv)):
    #If argument is '-f', skip it
    if sys.argv[i] == "-f":
        continue

    #If argument is '-g', skip it
    if sys.argv[i][:2] == "-g":
        continue

    #If the previous argument was '-f', make a folder
    if sys.argv[i - 1] == "-f":
        if not os.path.exists(sys.argv[i]):
            os.makedirs(sys.argv[i])
        DIR = sys.argv[i]
        continue

    exit_code = os.system("tree --du -h --charset=ANSII -F '%s' > '%s/%s'" % (
                sys.argv[i], DIR, os.path.basename(sys.argv[i].rstrip("/"))))
    if exit_code > 0:
        print "Something went wrong!"
        exit(1)

#Check if git is enabled
if GIT:
    #Check if GIT_ROOT is an actual folder
    if not os.path.isdir(GIT_ROOT):
        print "'%s' does not exist! Check your -g= option" % GIT_ROOT
        exit(1)
    #Check if current dir is a git repo
    if os.system("cd '%s'; git status >/dev/null 2>&1" % GIT_ROOT) != 0:
        #Create a git repo in the current folder
        exit_code = os.system("cd '%s'; git init" % GIT_ROOT)

        #If it failed to create, exit
        if exit_code > 0:
            print "Something went wrong when creating a git repo."
            exit(1)

    os.system('cd "%s"; git add .' % GIT_ROOT)
    os.system('cd "%s"; git commit -m "$(date)"' % GIT_ROOT)

