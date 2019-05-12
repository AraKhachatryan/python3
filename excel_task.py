#!/usr/bin/python3

import sys, getopt
import re
import time


#print script usage
def script_usage():
    print ("%s -i <inputfile> -o <outputfile>" % (sys.argv[0]))
    print("Example: %s -i 10000_Sales_Records.csv -o data.xlsx" % (sys.argv[0]))


def script_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "ifile=", "ofile="])
    except getopt.GetoptError as GetoptErrorMSG:
        print("%s: %s" % (sys.argv[0], GetoptErrorMSG))
        print("Try '%s -h or --help'" % (sys.argv[0]))
        sys.exit(2)
    #check if any options were passed
    if len(opts) > 0:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                script_usage()
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg
    else:
        #no options were passed
        script_usage()
        sys.exit(2)
    return inputfile, outputfile


def formatting_styles( workbook ):
    # Add a format. Blue fill
    bg_blue = workbook.add_format({'bg_color': '#33B2FF'})
    # Add a format. Yellow fill
    bg_yellow = workbook.add_format({'bg_color': '#FFF933'})
    # Add a format. Green fill
    bg_green = workbook.add_format({'bg_color': '#C6EFCE'})
    # Add a format. Red fill
    bg_red = workbook.add_format({'bg_color': '#FFC7CE'})
    return bg_blue, bg_yellow, bg_green, bg_red



def post_insert_formatting( worksheet, bg_red, bg_green ):
    # setting columns widths
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 29)
    worksheet.set_column('C:C', 13)
    worksheet.set_column('D:D', 12)
    worksheet.set_column('E:E', 12)
    worksheet.set_column('F:F', 11)
    worksheet.set_column('G:G', 12)
    worksheet.set_column('H:H', 11)
    worksheet.set_column('I:I', 9)
    worksheet.set_column('J:J', 9)
    worksheet.set_column('K:K', 9)
    worksheet.set_column('L:L', 13)
    worksheet.set_column('M:M', 11)
    # Write a conditional format over a range. Format background to red if "Item Type" is "Baby Food"
    worksheet.conditional_format('C2:C10000', {'type': 'text',
                                             'criteria': 'containing',
                                             'value': 'Baby Food',
                                             'format': bg_red})
    # Write a conditional format over a range. Format background to green if "Units Sold" greater than 5000
    worksheet.conditional_format('I2:I10000', {'type': 'cell',
                                             'criteria': '>',
                                             'value': '5000',
                                             'format': bg_green})


def main(argv):

    inputfile = ''
    outputfile = ''

    inputfile, outputfile = script_options()


    print ("Input file is ", inputfile)
    print ("Output file is ", outputfile),


    try:
        import xlsxwriter
    except ImportError as ImportErrorMSG:
        print(ImportErrorMSG)
        print("Installing xlsxwriter via pip3 ...")
        import os
        myCmd = os.popen('pip3 install xlsxwriter').read()
        print(myCmd)


    workbook = xlsxwriter.Workbook( outputfile )
    worksheet = workbook.add_worksheet( "sales" )

    # formatting styles
    bg_blue, bg_yellow, bg_green, bg_red = formatting_styles( workbook )

    num_rows = 0

    with open(inputfile, 'r', encoding='utf-8') as infile:
        start_timer = time.time()
        for line in infile:
            num_rows += 1
            regex = r"^([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+)$"
            matchObj = re.search( regex, line )
            if matchObj:
                if num_rows == 1:
                    # format background to blue for first row
                    worksheet.write_row( 'A'+str(num_rows) , matchObj.groups(), bg_blue )
                    continue
                # type cast to int() or float()
                row_list = [ matchObj.group(1), matchObj.group(2), matchObj.group(3), matchObj.group(4), matchObj.group(5),
                             matchObj.group(6), int(matchObj.group(7)), matchObj.group(8), int(matchObj.group(9)),
                             float(matchObj.group(10)), float(matchObj.group(11)), float(matchObj.group(12)), float(matchObj.group(13)) ]

                if row_list[0] == "Europe" and row_list[4] == "H":
                    # format background to yellow if "Region" is "Europe" and "Order Priority" is "H"
                    worksheet.write_row( 'A'+str(num_rows) , row_list, bg_yellow )
                else:
                    worksheet.write_row( 'A'+str(num_rows) , row_list )
                #break


    end_timer = time.time()
    read_and_insert_time = end_timer - start_timer
    print("Inserted into %s file %s rows, time: %.5f sec" % (outputfile, num_rows, read_and_insert_time))
    print("Saving and closing the %s file..." % outputfile, end =" ", flush=True )

    start_timer = time.time()

    # formatting the worksheet after inserting
    post_insert_formatting( worksheet, bg_red, bg_green )

    # closing the file
    workbook.close()
    end_timer = time.time()
    file_closing_time = end_timer - start_timer
    print("time: %.5f sec" % (file_closing_time) )


if __name__ == "__main__":
    main(sys.argv[1:])

