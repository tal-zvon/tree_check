#!/usr/bin/python
__author__ = 'tal'
__version__ = '2.0'

import argparse
import os
import sys
import subprocess
import time
import signal


# noinspection PyUnusedLocal,PyUnusedLocal
def signal_handler(kill_signal, frame):
    print   # Newline for formatting
    sys.exit(0)

#Handle Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 usage=("\t%s (-f OUT_DIR SRC_DIR... | -t OUT_FILE SRC_DIR...)\n" %
                                        os.path.basename(__file__) +
                                        "\t\t      [-g GIT_ROOT_DIR] [-i]\n" +
                                        "\t%s -h | --help\n" % os.path.basename(__file__) +
                                        "\t%s -e | --examples\n" % os.path.basename(__file__) +
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
parser.add_argument("-f", "--folder", metavar=("OUT_DIR", "SRC_DIR"), nargs="*", action="append",
                    help=("specify output folder. Can be specified multiple times. The last folder in the OUT_DIR"
                          " path will get created if it does not exist"))
parser.add_argument("-g", "--git", metavar="GIT_ROOT_DIR",
                    help=("enable git. Uses git to version control output after generating it. GIT_ROOT_DIR is the "
                          "root of the git repo"))
parser.add_argument("-i", "--ignore", action="store_true",
                    help="ignore empty and non-existent input directories. Useful when dealing with mounted filesystems"
                         " that may be unmounted once in a while when %s is running." % os.path.basename(__file__))
parser.add_argument("-t", "--total", metavar=("OUT_FILE", "SRC_DIR"), nargs="*", action="append",
                    help="create OUT_FILE with data about the total sizes of SRC_DIRs. Can be specified multiple times")
parser.add_argument('-v', '--version', action='version', version=('%(prog)s ' + __version__))
args = parser.parse_args()

#If examples arg passed, show help with examples and exit
if args.examples:
    print subprocess.check_output([sys.argv[0], '-h']),
    print "\nExamples:"
    print "\tRun tree on /etc, and put the output into the current folder:"
    print "\t\t$ %s -f . /etc\n" % os.path.basename(__file__)
    print "\tRun tree on /etc, and put the output into a folder called PC1:"
    print "\tNote: Folder 'PC1' is created automatically"
    print "\t\t$ %s -f PC1 /etc\n" % os.path.basename(__file__)
    print "\tRun tree on /etc, and put the output into the current folder."
    print "\tAlso run tree on '/SOME FOLDER' and put the output into the folder"
    print "\tcalled 'Machine 2':"
    print "\tNote: Folder 'Machine 2' is created automatically"
    print "\t\t$ %s -f . /etc -f Machine\ 2 /SOME\ FOLDER" % os.path.basename(__file__)
    print "\t\tOR"
    print "\t\t$ %s -f . /etc -f 'Machine 2' '/SOME FOLDER'\n" % os.path.basename(__file__)
    print "\tRun tree on /etc, and put the output into the current folder."
    print "\tThen run tree on /var and /usr, and put the output of both into"
    print "\ta folder called PC1."
    print "\tFinally run tree on /home, and put the output into the current"
    print "\tfolder too:"
    print "\tNote: Folder 'PC1' is created automatically"
    print "\t\t$ %s -f . /etc -f PC1 /var /usr -f . /home\n" % os.path.basename(__file__)
    print "\tRun tree on /etc, and make the output folder"
    print "\t'/home/user/test folder/Machine 1'."
    print "\tRun tree on /var, and make the output folder"
    print "\t'/home/user/test folder/Machine 2'."
    print "\tSet the git repo root folder to '/home/user/test folder/',"
    print "\tand make a git snapshot."
    print "\tNote: In this case, the '/home/user/test folder/'"
    print "\t  dir must already exist, while the 'Machine 1' and 'Machine 2' "
    print "\t  folders are created automatically"
    print "\t\t$ %s -f '/home/user/test folder/Machine 1' \\" % os.path.basename(__file__)
    print "\t\t    /etc -f '/home/user/test folder/Machine 2' /var \\"
    print "\t\t    -g '/home/user/test folder'\n"
    print "\tRun 'du -hcs' on /etc and /var, and put the output in a "
    print "\tfile called 'etc_var_totals'."
    print "\tAlso run 'du -hcs' on /home and /usr and put the output "
    print "\tin a file called 'home_usr_totals'."
    print "\tThen make a git snapshot of the output folder:"
    print "\t\t$ %s -t etc_var_totals /etc /var \\" % os.path.basename(__file__)
    print "\t\t    -t home_usr_totals /home /usr -g .\n"
    print "\tRun tree on '/etc', and run 'du -hcs' on /var before taking a "
    print "\tsnapshot of the output folder with git:"
    print "\t\t$ %s -f . /etc -t totals /var -g ." % os.path.basename(__file__)
    exit(0)

#If no arguments are given, give warning and exit
if len(sys.argv) == 1:
    parser.print_usage(file=sys.stderr)
    print >> sys.stderr, "%s: error:" % os.path.basename(__file__) + " need at least a '-f' or '-t' argument to run"
    exit(1)

#Check number of git, ignore, and folder args
git_args = 0
ignore_args = 0
folder_args = 0
total_args = 0
#Note: The [:2] catches tricky arg combinations like -gfi
for i in range(1, len(sys.argv)):
    if sys.argv[i][:2] == "-g" or sys.argv[i] == "--git":
        git_args += 1
    if sys.argv[i][:2] == "-i" or sys.argv[i] == "--ignore":
        ignore_args += 1
    if sys.argv[i][:2] == "-f" or sys.argv[i] == "--folder":
        folder_args += 1
    if sys.argv[i][:2] == "-t" or sys.argv[i] == "--total":
        total_args += 1
if git_args > 1:
    parser.print_usage(file=sys.stderr)
    print >> sys.stderr, "%s: error:" % os.path.basename(__file__) + " only one '--git' argument allowed"
    exit(1)
if git_args == 1:
    #If git is enabled, either -f or -t must be as well
    if folder_args == 0 and total_args == 0:
        parser.print_usage(file=sys.stderr)
        print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                             " '--git' can not be enabled without either '-f' or '-t'"
        exit(1)
if ignore_args > 1:
    parser.print_usage(file=sys.stderr)
    print >> sys.stderr, "%s: error:" % os.path.basename(__file__) + " only one '--ignore' argument allowed"
    exit(1)

#Make sure the '-f' option always has at least 2 arguments (1 output folder and 1 source folder)
if args.folder:
    for i in range(0, len(args.folder)):
        if len(args.folder[i]) < 2:
            parser.print_usage(file=sys.stderr)
            print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                 " '--folder' must have at least 2 arguments"
            exit(1)

#Make sure the '-t' option always has at least 2 arguments (1 output file and 1 source folder)
if args.total:
    for i in range(0, len(args.total)):
        if len(args.total[i]) < 2:
            parser.print_usage(file=sys.stderr)
            print >> sys.stderr, "%s: error:" % os.path.basename(__file__) + " '--total' must have at least 2 arguments"
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
                        parser.print_usage(file=sys.stderr)
                        print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                             (" '%s' is not a valid path " %
                                              os.path.dirname(args.folder[i][x].rstrip("/")) +
                                              "for an output folder")
                        exit(1)
            else:
                if not args.ignore:     # Make sure we weren't specifically told to ignore non-existent source folders
                    #Check if the source folder exists
                    if not os.path.isdir(os.path.expanduser(args.folder[i][x])):
                        parser.print_usage(file=sys.stderr)
                        print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                             (" '%s' is not a valid path for a "
                                              "source folder" % args.folder[i][x])
                        exit(1)

#Check if all -t options are valid
if args.total:
    for i in range(0, len(args.total)):     # For every list in args.total
        for x in range(0, len(args.total[i])):   # For every item in the current list
            if x == 0:  # args.total[i][0] is always the output file (ex: -t total /etc /var OR -t ~/total /etc /var)
                #Make sure that the user is giving us a file instead of a dir
                if args.total[i][x][-1] == "/" or args.total[i][x][-1] == ".":
                    parser.print_usage(file=sys.stderr)
                    print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                         " '%s' is a dir, when we are expecting a filename or file path" %\
                                         args.total[i][x]
                    exit(1)

                #Make sure that the user is not giving us an existing directory
                if os.path.isdir(os.path.expanduser(args.total[i][x])):
                    parser.print_usage(file=sys.stderr)
                    print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                         " '%s' is an existing dir, when we are expecting a filename or file path" %\
                                         args.total[i][x]
                    exit(1)

                #The dirname does not need to exist if it doesn't start with / or ~
                if args.total[i][x][0] == "/" or args.total[i][x][0] == "~":
                    #Check if the dirname of the output folder exists - we will create the file
                    if not os.path.isdir(os.path.expanduser(os.path.dirname(args.total[i][x].rstrip("/")))):
                        parser.print_usage(file=sys.stderr)
                        print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                             (" '%s' is not a valid path "
                                              % os.path.dirname(args.total[i][x].rstrip("/")) +
                                              "for an output folder for --total")
                        exit(1)
            else:
                if not args.ignore:     # Make sure we weren't specifically told to ignore non-existent folders
                    #Check if the source folder exists
                    if not os.path.isdir(os.path.expanduser(args.total[i][x])):
                        parser.print_usage(file=sys.stderr)
                        print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                             (" '%s' is not a valid path " % args.total[i][x] +
                                              "for a source folder for --total")
                        exit(1)

#Check if git root folder is valid
GIT_VALID = False
if args.git:
    if not os.path.isdir(os.path.expanduser(args.git)):
        if args.folder:
            #Check if it's listed as an output folder
            for i in range(0, len(args.folder)):
                if os.path.abspath(os.path.expanduser(args.folder[i][0]).rstrip("/")) ==\
                        os.path.abspath(os.path.expanduser(args.git).rstrip("/")):
                    GIT_VALID = True
                    break
            if not GIT_VALID:
                parser.print_usage(file=sys.stderr)
                print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                     " '%s' is an invalid path for a git repo" % args.git
                exit(1)
        else:
            parser.print_usage(file=sys.stderr)
            print >> sys.stderr, "%s: error:" % os.path.basename(__file__) + " '%s' is an invalid path for a git repo"\
                                                                             % args.git
            exit(1)

#For every argument to -f, run tree on it and send it where it needs to go
if args.folder:
    for i in range(0, len(args.folder)):    # For every list in args.folder
        for x in range(0, len(args.folder[i])):     # For every item in the current list
            if x == 0:      # args.folder[i][0] is always the output folder (ex: -f OUTPUT_FOLDER SRC SRC SRC)
                if not os.path.isdir(os.path.expanduser(args.folder[i][x])):    # If the output folder doesn't exist
                    #Make sure there isn't a file with the same name already there
                    if os.path.isfile(os.path.expanduser(args.folder[i][x])):
                        parser.print_usage(file=sys.stderr)
                        print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                             " unable to create '%s' output directory" %\
                                             args.folder[i][x]
                        print >> sys.stderr, "%s: error: a file with that name already exists" %\
                                             os.path.basename(__file__)
                        exit(1)

                    try:
                        os.makedirs(os.path.expanduser(args.folder[i][x]))
                    except OSError:
                        parser.print_usage(file=sys.stderr)
                        print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                             " unable to create '%s' output directory" %\
                                             args.folder[i][x]
                        print >> sys.stderr, "%s: error: check your permissions" % os.path.basename(__file__)
                        exit(1)
            else:   # For every source folder
                if not os.path.isdir(os.path.expanduser(args.folder[i][x])):    # If the source folder doesn't exist
                    continue    # Skip it. We're clearly using -i, or it would have been caught earlier
                if args.ignore and os.listdir(os.path.expanduser(args.folder[i][x])) == []:  # If source folder is empty
                    continue    # Skip it. Ex: NFS mounts that exist, but are not mounted

                try:
                    output = subprocess.check_output(['tree', '--du', '-h', '--charset', '-F', '%s' %
                                                     os.path.expanduser(args.folder[i][x])],
                                                     stderr=open("/dev/null", "w"))
                    open("%s/%s" % (os.path.expanduser(args.folder[i][0]),
                                    os.path.basename(args.folder[i][x].rstrip("/"))), 'w').write(output)
                except (subprocess.CalledProcessError, OSError, IOError):
                    parser.print_usage(file=sys.stderr)
                    print >> sys.stderr, "%s: error:" % os.path.basename(__file__) + " error running the tree command"
                    exit(1)

#For every argument to -t, run du on it and send it where it needs to go
if args.total:
    for i in range(0, len(args.total)):     # For every list in args.total
        f = ''  # File handle
        #Open output file for writing
        try:
            f = open(args.total[i][0], "w")     # Immediately blanks out a file and prepares it for writing
        except IOError:
            parser.print_usage(file=sys.stderr)
            print >> sys.stderr, "%s: error:" % os.path.basename(__file__) + " failed to write to '%s'" %\
                                                                             args.total[i][0]
            exit(1)

        for x in range(0, len(args.total[i])):     # For every item in the current list
            if x == 0:  # Skip the first argument to every -t (the output file)
                continue

            f.write(os.path.expanduser(args.total[i][x]) + '\n')
            f.write("=" * len(os.path.expanduser(args.total[i][x])) + '\n')

            #Check if source folder exists (it may not if -i was used)
            if os.path.isdir(os.path.expanduser(args.total[i][x])):
                f.write(subprocess.Popen("du -hcs '%s'/*" % os.path.expanduser(args.total[i][x]).rstrip("/"),
                                         shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, close_fds=True).stdout.read())
            else:
                f.write("'%s' not found" % os.path.expanduser(args.total[i][x]))

            f.write('\n\n')

        f.close()

#If git is enabled, start a new repo (if necessary), add files and commit
if args.git:
    #Change dir to git root folder
    os.chdir(os.path.expanduser(args.git))

    #Check if args.git is a git repo, or if it needs to be created
    if subprocess.call(["git", "status"], stdout=open("/dev/null", "w"), stderr=open("/dev/null", "w")) != 0:
        #Create a git repo in the current folder
        exit_code = subprocess.call(["git", "init"], stdout=open("/dev/null", "w"))

        #If it failed to create, exit
        if exit_code > 0:
            parser.print_usage(file=sys.stderr)
            print >> sys.stderr, "%s: error:" % os.path.basename(__file__) +\
                                 " something went wrong when creating a git repo"
            exit(1)

    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", time.ctime()], stdout=open("/dev/null", "w"))