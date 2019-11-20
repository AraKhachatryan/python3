#!/usr/bin/python3

import os, sys, getopt
import re
import time


regex_search = r"Fingerprint: \[([^\]]+)]"
regex_replace = r"\1\n"


#print script usage
def script_usage():
    print ("Usage: %s -i <input_file> -o <output_file>" % (sys.argv[0]))


def script_options():
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "ifile=", "ofile="])
    except getopt.GetoptError as GetoptErrorMSG:
        print("%s: %s" % (sys.argv[0], GetoptErrorMSG))
        print("Try '%s -h or --help'" % (sys.argv[0]))
        sys.exit(2)
    # check if any options were passed
    if len(opts) > 0:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                script_usage()
                sys.exit()
            elif opt in ("-i", "--ifile"):
                input_file = arg
            elif opt in ("-o", "--ofile"):
                output_file = arg
    else:
        #no options were passed
        script_usage()
        sys.exit(2)
    # if input file is not specified
    if input_file == "":
        print("Error: input file is not specified.")
        script_usage()
        sys.exit(2)
    # if output file is not specified
    if output_file == "":
        print("Error: output file is not specified.")
        script_usage()
        sys.exit(2)
    return input_file, output_file


def main(argv):

    input_file = ''
    output_file = ''

    global regex_search
    global regex_replace

    input_file, output_file = script_options()

    if not os.path.isfile(input_file):
        print("Error: input file is not exist.")
        sys.exit(2)
    print ("Input file is ", os.path.abspath(input_file))
    print ("Output file is ", os.path.abspath(output_file))

    # clean the file if exist, otherwise make it
    open(output_file, 'w+').close()

    num_rows = 0
    start_timer = time.time()

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'a', encoding='utf-8') as outfile:
        for line in infile:
            searchObj = re.search( regex_search, line, flags=re.IGNORECASE|re.MULTILINE|re.UNICODE )
            if searchObj:
                num_rows += 1
                replaced_line = re.sub( regex_search, regex_replace, searchObj.group(0), flags=re.IGNORECASE|re.MULTILINE|re.UNICODE )
                outfile.write(replaced_line)

    end_timer = time.time()
    elapsed_time = end_timer - start_timer
    print("Replaced %s rows, time: %.5f sec" % (num_rows, elapsed_time))


if __name__ == "__main__":
    main(sys.argv[1:])

