#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import format_path
import vhdl_parser
 
src_file_path = sys.argv[1]
print "Path to the VHDL File: ",src_file_path

src_file = open(src_file_path, 'r')
src_file_path = src_file_path.replace(".txt","")
src_file_path = src_file_path.replace("../","")
text = src_file.read()

vhdl_path = format_path.format_top(src_file_path)

dest_file = open(vhdl_path, 'w')

generated_vhdl = vhdl_parser.parse_vhdl(text)

dest_file.write(generated_vhdl)
dest_file.close()
src_file.close()

print "VHDL file created in the .txt file folder with sucess"
