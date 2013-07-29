#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
import getpass

now = datetime.datetime.now()

def parse_vhdl(text):
    if '#' in text:
        splitted_text = text.split('#')
        temp = splitted_text[0]
        temp = temp[:-1]
        splitted_text[0] = temp
        lines = splitted_text[0].split("\n")
        splitted_text[1] = splitted_text[1].split("\n")
        vhdl_text = entity_header()
        vhdl_text = entity_declaration(vhdl_text,lines[0])
        vhdl_text = ports_declaration(vhdl_text,lines[1:],lines[0])
        vhdl_text = add_minus(vhdl_text)
        vhdl_text = insert_architecture(vhdl_text,lines[0],lines[1],lines[2],splitted_text[1])
    else:
        vhdl_text = "the % symbol wasnt found in the .txt file"
    return vhdl_text 

def parse_tb(text):
    return text

def entity_header():
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

def entity_declaration(text,entity_name):
    text = text + "\n\
entity "+entity_name+" is\n\
  port (\n"
    return text

def ports_declaration(text,lines_ports,entity_name):
    for i in lines_ports:
        i = i.replace("\r","")
        splitted_line = i.split("-");
        for j in splitted_line:
            if j == "in":
                temp = temp + "  : in"
            elif j == "out":
                temp = temp + "  : out"
            elif j=="1":
                temp = temp + " std_logic;"
            elif j.isdigit():
                adjust_bits = int(j)-1
                temp = temp + " std_logic_vector(" + str(adjust_bits) +" downto 0);"
            else:
                temp = "    "+j
        text=text+temp+"\n"
    text = text[:-2] + "\n"
    text = text + "    );\n"
    text = text + "end " + entity_name + ";"
    return text;

def add_minus(text):
    text = text + "\n\n------------------------------------------------------\n\n"
    return text

def insert_architecture(text, entity_name,clk,rst,regs):
    clk = clk.split("-")
    clk = clk[0]
    rst = rst.split("-")
    rst = rst[0]
    regs = regs[1:-1]
    regs_dictionary = {}
    text = text +"\
architecture rtl of "+ entity_name + " is\n\
  type STATE_MACHINE_TYPE is (S0,S1,S2,S3);\n\n\
  attribute SYN_ENCODING : string;\n\
  attribute SYN_ENCODING of STATE_MACHINE_TYPE : type is \"safe\";\n\
\n\
  signal state      : STATE_MACHINE_TYPE;\n\
  signal state_next : STATE_MACHINE_TYPE;\n\
\n"
    for i in regs:
        i = i.replace("\r","")
        splitted_line = i.split("-")
        for j in splitted_line:
            if j == "1":
                temp = temp + " : std_logic;"
                temp2 = temp2 + " : std_logic;"
            elif j.isdigit():
                adjust_bits = int(j)-1
                temp = temp + " : std_logic_vector(" + str(adjust_bits) + " downto 0);"
                temp2 = temp2 + " : std_logic_vector(" + str(adjust_bits) + " downto 0);"
            else:
                temp = "  signal " + j + "_reg"
                temp2 = "  signal " + j + "_next"
                dic_key = j + "_reg"
                dic_value = j + "_next"
                regs_dictionary[dic_key] = dic_value
        text = text + temp + "\n" + temp2 + "\n"
        temp = ""
        temp2 = ""
    text = text + temp + "\n" + temp2 + "\
begin\n\
\n\
-- Sequential process \n\
  process("+clk+", "+rst+") is\n\
  begin\n\
    if ("+rst+" = \'0\') then\n\
      state <= S0;\n\
    elsif rising_edge("+clk+") then\n"
    for key, value in regs_dictionary.items():
        text = text + "      " + key + " <= " + value + ";"+"\n"
    text = text+"\
      state <= state_next;\n\
    end if;\n\
  end process;\n\
\n\
-- Combinational process \n\
  process(state"
    temp = ""
    for key in regs_dictionary.keys():
        temp = temp + ", " + str(key)  
    text = text + temp + ") is\n\
  begin\n"
    for key, value in regs_dictionary.items():
        text = text + "    " + value + " <= " + key + ";"+"\n"
    text = text + "    state_next <= state;\n\
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
    return text
