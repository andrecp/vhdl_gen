#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import format_path
import vhdl_parser
 
arquivo_vhdl = sys.argv[1]
print "Caminho do arquivo VHDL de entrada: ",arquivo_vhdl

arq = open(arquivo_vhdl, 'r')
arquivo_vhdl = arquivo_vhdl.replace(".txt","")
arquivo_vhdl = arquivo_vhdl.replace("../","")
texto = arq.read()

caminho_vhd = format_path.format_top(arquivo_vhdl)

arq_vhdl = open(caminho_vhd, 'w')

generated_vhdl = vhdl_parser.parse_vhdl(texto)

arq_vhdl.write(generated_vhdl)
arq_vhdl.close()
arq.close()

print "Arquivo vhdl criado na pasta atual com sucesso"
