#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
import getpass

now = datetime.datetime.now()

def parse_vhdl(texto):
    if '#' in texto:
        entrada = texto.split('#')
        temp = entrada[0]
        temp = temp[:-1]
        entrada[0] = temp
        linhas = entrada[0].split("\n")
        entrada[1] = entrada[1].split("\n")
        s = cabecario_entidade()
        s = declaracao_entidade(s,linhas[0])
        s = declaracao_portas(s,linhas[1:],linhas[0])
        s = adiciona_menos(s)
        s = adiciona_arquitetura(s,linhas[0],linhas[1],linhas[2],entrada[1])
    else:
        s = "Nao foi encontrado um # com os registradores no arquivo de entrada"
    return s

def parse_tb(texto):
    return texto

def cabecario_entidade():
    string = "------------------------------------------------------\n\
-- Nome : "+getpass.getuser()+"\n\
-- Criado em : " + now.strftime("%d-%m-%Y %H:%M") + "\n\
------------------------------------------------------\n\
\n\
--Libraries and use clauses\n \
\n\
library ieee;\n\
use ieee.std_logic_1164.all;\n\
use ieee.numeric_std.all;\n"
    return string

def declaracao_entidade(texto,nome_entidade):
    texto = texto + "\n\
entity "+nome_entidade+" is\n\
  port (\n"
    return texto

def declaracao_portas(texto,linhas_portas,nome_entidade):
    for i in linhas_portas:
        i = i.replace("\r","")
        partes_linha = i.split("-");
        for j in partes_linha:
            if j == "entrada":
                temp = temp + "  : in"
            elif j == "saida":
                temp = temp + "  : out"
            elif j=="1":
                temp = temp + " std_logic;"
            elif j.isdigit():
                ajusta_bits = int(j)-1
                temp = temp + " std_logic_vector(" + str(ajusta_bits) +" downto 0);"
            else:
                temp = "    "+j
        texto=texto+temp+"\n"
    texto = texto[:-2] + "\n"
    texto = texto + "    );\n"
    texto = texto + "end " + nome_entidade + ";"
    return texto;

def adiciona_menos(texto):
    texto = texto + "\n\n------------------------------------------------------\n\n"
    return texto

def adiciona_arquitetura(texto, nome_entidade,clk,rst,regs):
    clk = clk.split("-")
    clk = clk[0]
    rst = rst.split("-")
    rst = rst[0]
    regs = regs[1:-1]
    dicionario_regs = {}
    texto = texto +"\
architecture rtl of "+ nome_entidade + " is\n\
  type STATE_MACHINE_TYPE is (S0,S1,S2,S3);\n\n\
  attribute SYN_ENCODING : string;\n\
  attribute SYN_ENCODING of STATE_MACHINE_TYPE : type is \"safe\";\n\
\n\
  signal state      : STATE_MACHINE_TYPE;\n\
  signal state_next : STATE_MACHINE_TYPE;\n\
\n"
    for i in regs:
        i = i.replace("\r","")
        partes_linha = i.split("-")
        for j in partes_linha:
            if j == "1":
                temp = temp + " : std_logic;"
                temp2 = temp2 + " : std_logic;"
            elif j.isdigit():
                ajusta_bits = int(j)-1
                temp = temp + " : std_logic_vector(" + str(ajusta_bits) + " downto 0);"
                temp2 = temp2 + " : std_logic_vector(" + str(ajusta_bits) + " downto 0);"
            else:
                temp = "  signal " + j + "_reg"
                temp2 = "  signal " + j + "_next"
                dic_key = j + "_reg"
                dic_value = j + "_next"
                dicionario_regs[dic_key] = dic_value
        texto = texto + temp + "\n" + temp2 + "\n"
        temp = ""
        temp2 = ""
    texto = texto + temp + "\n" + temp2 + "\
begin\n\
\n\
-- Sequential process \n\
  process("+clk+", "+rst+") is\n\
  begin\n\
    if ("+rst+" = \'0\') then\n\
      state <= S0;\n\
    elsif rising_edge("+clk+") then\n"
    for key, value in dicionario_regs.items():
        texto = texto + "      " + key + " <= " + value + ";"+"\n"
    texto = texto+"\
      state <= state_next;\n\
    end if;\n\
  end process;\n\
\n\
-- Combinational process \n\
  process(state"
    temp = ""
    for key in dicionario_regs.keys():
        temp = temp + ", " + str(key)  
    texto = texto + temp + ") is\n\
  begin\n"
    for key, value in dicionario_regs.items():
        texto = texto + "    " + value + " <= " + key + ";"+"\n"
    texto = texto + "    state_next <= state;\n\
  \n\
    case state is\n\
\n\
      when S0 =>\n\
          null;\n\
      when S1 =>\n\
          null;\n\
      when S2 =>\n\
          null;\n\
      when S3 =>\n\
          null;\n\
      when OTHERS =>\n\
          null;\n\
    end case;\n\
  end process;\n\
\n\
\n\
end rtl;"
    return texto
