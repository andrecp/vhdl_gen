#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import vhdl_parser
 
src_file_path = sys.argv[1]

src_file_path = os.path.abspath(src_file_path)
print "Path to the VHDL File: ",src_file_path
src_file_dir = os.path.dirname(src_file_path)

src_file_fd = open(src_file_path, 'r')
text = src_file_fd.read()
src_file_fd.close()

vhdl_path = os.path.splitext(src_file_path)[0] + '.vhd'

dest_file_fd = open(vhdl_path, 'w')

generated_vhdl = vhdl_parser.parse_vhdl(text)

dest_file_fd.write(generated_vhdl)
dest_file_fd.close()

print 'VHDL file created in the ' + src_file_dir + '/ folder with sucess'
