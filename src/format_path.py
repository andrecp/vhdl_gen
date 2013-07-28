# -*- coding: utf-8 -*-

import sys
import os

def format_tb(file):
    path_tb = "../sim/"
    path_tb += "tb_"
    path_tb += file
    path_tb += ".vhd"
    return path_tb

def format_top(file):
    path_vhd = "../"
    path_vhd += file
    path_vhd += ".vhd"
    return path_vhd
