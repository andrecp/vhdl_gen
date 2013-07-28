# -*- coding: utf-8 -*-

import sys
import os

def format_tb(file):
    caminho_tb = "../sim/"
    caminho_tb += "tb_"
    caminho_tb += file
    caminho_tb += ".vhd"
    return caminho_tb

def format_top(file):
    caminho_vhd = "../"
    caminho_vhd += file
    caminho_vhd += ".vhd"
    return caminho_vhd
