#!/usr/bin/env python3
"""
Parse a file containing ASN1 pseudo-code and prep it for C++ conversion.
Shares some similarities with asn1c, but this version focus on the latest 3GPP LTE specifications

Formats the output file with 'astyle'.
Ref: http://www.itu.int/en/ITU-T/asn1/Pages/introduction.aspx
$Id: asn1convert.py, 9ddcffa7b4df  makhtar $
"""
import sys
import os
import re

__author__ = "Adhoc ASN1 converter, by Makhtar Diouf"

infile = ''
if len(sys.argv) < 2:
    # input("Specify the ASN file to convert: ")
    infile = "asn1test.txt"
else:
    infile = sys.argv[1]

inp = open(infile)
print("Reading file ", inp.name)

# Symbols table
opts = {
    "SEQUENCE": " struct ",
    "CHOICE": " enum ", # verify
    "ENUMERATED": " enum ",
    "BOOLEAN": " bool ",
    #"BIT STRING": "std::bitset",
    "BIT": "std::bitset<1>",
    "INTE": " int ",
    "OCTE": " char ",
    "STRING": " string ",
    "OPTIONAL": '',
    "Need ON": ' ',
    "Need OP": ' ',
    "NULL": 'typedef ',
    "END": '// END',
    "r12": '_r12',
    "r13": '_r13',
    "...": "\n",
    "[[": " \n",
    "]]": " \n",
    "::=": " ",
    "--": " // ",
    "-": '',
    #",": ' ',
    "\t": ''
}

try:
    line = inp.readline()
    lnum = 0
    outp = open(inp.name + ".h", "w")
    # Foward declarations header file
    outp2 = open(inp.name + "_typedefs.h", "w")
    outp.write("\n// Note: " + __author__)
    outp.write('\n#include "' + outp2.name + '"\n')

    typedef_list = []
    inAsn = False

    def checkAsn(_line):
        global inAsn
        global line
        if "ASN1START" in _line:
            inAsn = True
            outp.write("// " + _line.strip() + "\n")
            line = inp.readline()

        elif "ASN1STOP" in _line:
            inAsn = False
        return inAsn

    while line != '':
        lnum += 1
        inAsn = checkAsn(line)
        if not inAsn:
            # Comment out non-ASN text
            outp.write("// " + line.strip() + "\n")
            line = inp.readline()
            continue

        tmp = line.split("\t")
        parts = [str(_).strip() for _ in tmp]
        del(tmp)
        line = ''

        for s in reversed(parts):
            s = s.strip()
            if s.isspace():
                continue
            elif ('(' not in s):
                line += s.strip() + " "
            else:
                try:
                    if "BIT STRING" in s:
                        # Get the size
                        tmp = [str(_) for _ in list(s) if _.isdigit()]
                        print("Line", lnum, s, tmp, ''.join(tmp))
                        line += 'std::bitset<' + ''.join(tmp) + '>'
                    else:
                    # e.g. INTEGER (0..28)
                        line += (s[:4]) + " "
                except TypeError:
                    print("Error @line", lnum, sys.exc_info()[0])

        d1 = False
        d2 = False
        d3 = False  # struct in previous line

        if "{" in line:
            d1 = True
            if 'ENUMERATE' in line:
                opts[','] = ','

            # Handle long enums, and structs
            tmp = line.split("{")
            line = tmp[0]
            tmp = tmp[1].split(',')
            if 'SEQ' in line:
                line += tmp[len(tmp)-1] + " { \n"
            else:
                line += tmp[len(tmp)-1] + " { \n\t" + tmp[0] + ", "

            line += ', '.join(tmp[1:len(tmp)-2])

        elif "}" in line:
            d2 = True
            line = "\t" + str(line)
        elif "struct" in line:
            d3 = True
            line = "\t" + str(line)


        # Replace items present in the symbols table
        for k in opts:
            if k not in line:
                continue
            line = re.sub(re.escape(k), opts[k], line.strip())

        if not line.isspace():
            if ("bool" not in line) and ("int" not in line)\
               and ("bitset" not in line):
                s = line.split(' ')
                d = d1 or d2 or d3
                i = 0
                typed = s[i]
                while typed.isspace():
                    typed = s[i]
                    i += 1

                if (not d) and not (typed == "typedef"):
                    typedef_list.append(typed)
                del(s)

        if d1:
            outp.write("\t" + line + "\n")
        else:
            outp.write("\t" + line + ";\n")
        line = inp.readline()
        # Reset d1
        opts[','] = ' '

except Exception:
    print("Error @line", lnum, sys.exc_info()[0])
    outp.write("// Error line: " + str(lnum))
    #bytes(line).decode("utf-8", "ignore"))
    print(line)
    outp.seek(lnum+100)
    # Skip over
    line = inp.readline()
    checkAsn(line)
    #raise

finally:
    inp.close()
    os.system("astyle --style=gnu " + outp.name)
    print(lnum, "lines processed. See output files: ", outp.name, outp2.name)

    outp2.write("\n\n// Forward declarations for " + outp.name)
    outp2.write("\n// Note: " + __author__)
    outp.close()

    for s in typedef_list:
        outp2.write("\ntypedef " + s + ";")

    # Remove empty typedefs
    outp2.close()
    os.system("sed -i 's/typedef ;/ /g' " + outp2.name)
    os.system("sed -i 's/     / /g' " + outp2.name)
    print(len(typedef_list), " typedefs generated. Check if any are missing, and fix invalid C++ statements")
    
