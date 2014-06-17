#!/usr/bin/python
__author__ = 'tal'
__version__ = '2.0'

import argparse
import os
import sys

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 usage=("\t%s -f OUTPUT_FOLDER SOURCE_FOLDER...\n" % os.path.basename(__file__) +
                                        "\t\t\t[-g GIT_ROOT_FOLDER] [-i]\n" +
                                        "\t%s -h | --help\n" % os.path.basename(__file__) +
                                        "\t%s -v | --version" % os.path.basename(__file__)),
                                 description=('Run the "tree"'
                                              ' command in a way that:\n'
                                              '  * Makes the output easily grepable\n'
                                              '  * Shows dir and file sizes in a human readable way\n'
                                              'and write the output to a desired location.'),
                                 epilog=("Exit Status:\n"
                                         "\t0 if OK\n"
                                         "\t1 if Errors caused an early exit\n\n"))
parser.add_argument("-e", "--examples", action="store_true", help="show usage examples")
parser.add_argument("-f", "--folder", metavar=("OUTPUT_FOLDER", "SOURCE_FOLDER"), nargs="+", action="append",
                    help=("specify output folder. Can be specified multiple times. The last folder in the OUTPUT_FOLDER"
                          " path will get created if it does not exist"))
parser.add_argument("-g", "--git", metavar="GIT_ROOT_FOLDER",
                    help=("enable git. Uses git to version control output after generating it. GIT_ROOT_FOLDER is the "
                          "root of the git repo"))
parser.add_argument("-i", "--ignore", action="store_true",
                    help="ignore empty and non-existent input directories. Useful when dealing with mounted filesystems"
                         " that may be unmounted once in a while when %s is running." % os.path.basename(__file__))
parser.add_argument('-v', '--version', action='version', version=('%(prog)s ' + __version__))
args = parser.parse_args()

#If examples arg passed, show help with examples and exit
if args.examples:
    os.system(sys.argv[0] + " -h")
    print "\nExamples:"
    print "\tRun tree on /etc, and put the output into the current folder:"
    print "\t\t$ %s -f . /etc\n" % os.path.basename(__file__)
    print "\tRun tree on /etc, and put the output into a folder called PC1:"
    print "\t\t$ %s -f PC1 /etc\n" % os.path.basename(__file__)
    print "\tRun tree on /etc, and put the output into the current folder."
    print "\tAlso run tree on '/SOME FOLDER' and put the output into the folder"
    print "\tcalled 'Machine 2':"
    print "\t\t$ %s -f . /etc -f Machine\ 2 /SOME\ FOLDER" % os.path.basename(__file__)
    print "\t\tOR"
    print "\t\t$ %s -f . /etc -f 'Machine 2' '/SOME FOLDER'\n" % os.path.basename(__file__)
    print "\tRun tree on /etc, and put the output into the current folder."
    print "\tThen run tree on /var and /usr, and put the output of both into"
    print "\ta folder called PC1."
    print "\tFinally run tree on /home, and put the output into the current"
    print "\tfolder too."
    print "\t\t$ %s -f . /etc -f PC1 /var /usr -f . /home\n" % os.path.basename(__file__)
    print "\tRun tree on /etc, and make the output folder"
    print "\t'/home/user/test folder/Machine 1'."
    print "\tRun tree on /var, and make the output folder"
    print "\t'/home/user/test folder/Machine 2'."
    print "\tSet the git repo root folder to '/home/user/test folder/',"
    print "\tand make a git snapshot."
    print "\tNote: In this case, the '/home/user/test folder/'"
    print "\tdir must already exist"
    print "\t\t$ %s -f '/home/user/test folder/Machine 1' \\" % os.path.basename(__file__)
    print "\t\t    /etc -f '/home/user/test folder/Machine 2' /var \\"
    print "\t\t    -g '/home/user/test folder'"
    exit(0)

#Check number of git and ignore args
git_args = 0
ignore_args = 0
folder_args = 0
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-g" or sys.argv[i] == "--git":
        git_args += 1
    if sys.argv[i] == "-i" or sys.argv[i] == "--ignore":
        ignore_args += 1
    if sys.argv[i] == "-f" or sys.argv[i] == "--folder":
        folder_args += 1
if git_args > 1:
    parser.print_usage()
    print "%s: error:" % os.path.basename(__file__) + " only one '--git' argument allowed"
    exit(1)
if ignore_args > 1:
    parser.print_usage()
    print "%s: error:" % os.path.basename(__file__) + " only one '--ignore' argument allowed"
    exit(1)
if folder_args == 0:
    parser.print_usage()
    print "%s: error:" % os.path.basename(__file__) + " must have at least one '--folder' argument"
    exit(1)

#Make sure the '-f' option always has at least 2 arguments (1 output folder and 1 source folder)
for i in range(0, len(args.folder)):
    if len(args.folder[i]) < 2:
        parser.print_usage()
        print "%s: error:" % os.path.basename(__file__) + " '--folder' must have at least 2 arguments"
        exit(1)

#Check if all source and output folders are valid
if args.folder:     # Check if '-f' was ever passed to the script
    for i in range(0, len(args.folder)):    # For every list in args.folder
        for x in range(0, len(args.folder[i])):     # For every item in the current list
            if x == 0:  # args.folder[i][0] is always the output folder (ex: -f OUTPUT_FOLDER SRC SRC SRC)
                #The output folder does not need to exist if it doesn't start with / or ~
                if args.folder[i][x][0] == "/" or args.folder[i][x][0] == "~":
                    #Check if the dirname of the output folder exists - we can create the last folder if it doesn't
                    if not os.path.isdir(os.path.expanduser(os.path.dirname(args.folder[i][x].rstrip("/")))):
                        parser.print_usage()
                        print "%s: error:" % os.path.basename(__file__) +\
                              (" '%s' is not a valid path " % os.path.dirname(args.folder[i][x].rstrip("/")) +
                               "for an output folder")
                        exit(1)
            else:
                if not args.ignore:     # Make sure we weren't specifically told to ignore non-existent source folders
                    #Check if the source folder exists
                    if not os.path.isdir(os.path.expanduser(args.folder[i][x])):
                        parser.print_usage()
                        print "%s: error:" % os.path.basename(__file__) + (" '%s' is not a valid path for a "
                                                                           "source folder" % args.folder[i][x])
                        exit(1)

#Check if git root folder is valid
GIT_VALID = False
if args.git:
    if not os.path.isdir(os.path.expanduser(args.git)):
        #Check if it's listed as an output folder
        for i in range(0, len(args.folder)):
            if os.path.expanduser(args.folder[i][0]).rstrip("/") == os.path.expanduser(args.git).rstrip("/"):
                GIT_VALID = True
                break
        if not GIT_VALID:
            parser.print_usage()
            print "%s: error:" % os.path.basename(__file__) + " '%s' is an invalid path for a git repo" % args.git
            exit(1)

#For every argument, run tree on it and send it where it needs to go
for i in range(0, len(args.folder)):    # For every list in args.folder
    for x in range(0, len(args.folder[i])):     # For every item in the current list
        if x == 0:      # args.folder[i][0] is always the output folder (ex: -f OUTPUT_FOLDER SRC SRC SRC)
            if not os.path.isdir(os.path.expanduser(args.folder[i][x])):    # If the output folder doesn't exist
                try:
                    os.makedirs(os.path.expanduser(args.folder[i][x]))
                except OSError:
                    parser.print_usage()
                    print "%s: error:" % os.path.basename(__file__) + " unable to create '%s' output directory" %\
                                                                      args.folder[i][x]
                    print "%s: error: check your permissions" % os.path.basename(__file__)
                    exit(1)
        else:   # For every source folder
            if not os.path.isdir(os.path.expanduser(args.folder[i][x])):    # If the source folder doesn't exist
                continue    # Skip it. We're clearly using -i, or it would have been caught earlier
            if args.ignore and os.listdir(os.path.expanduser(args.folder[i][x])) == []:  # If the source folder is empty
                continue    # Skip it. Ex: NFS mounts that exist, but are not mounted

            exit_code = os.system("tree --du -h --charset -F '%s' > '%s/%s'" %
                                  (os.path.expanduser(args.folder[i][x]),
                                   os.path.expanduser(args.folder[i][0]),
                                   os.path.basename(args.folder[i][x].rstrip("/"))))

            if exit_code > 0:
                print ("Error while running:" +
                       "'tree --du -h --charset -F '%s' > '%s/%s''" %
                       (os.path.expanduser(args.folder[i][x]),
                       os.path.expanduser(args.folder[i][0]),
                       os.path.basename(args.folder[i][x].rstrip("/"))))
                exit(1)

#If git is enabled, start a new repo (if necessary), add files and commit
if args.git:
    #Check if args.git is a git repo, or if it needs to be created
    if os.system("cd '%s'; git status >/dev/null 2>&1" % os.path.expanduser(args.git)) != 0:
        #Create a git repo in the current folder
        exit_code = os.system("cd '%s'; git init >/dev/null" % os.path.expanduser(args.git))

        #If it failed to create, exit
        if exit_code > 0:
            parser.print_usage()
            print "%s: error:" % os.path.basename(__file__) + " something went wrong when creating a git repo"
            exit(1)

    os.system('cd "%s"; git add .' % os.path.expanduser(args.git))
    os.system('cd "%s"; git commit -m "$(date)" >/dev/null' % os.path.expanduser(args.git))