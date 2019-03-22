from selenium import webdriver
import time
import sys
from collections import defaultdict
import logging, sys
from datetime import datetime


def gotoURL(driver, url):
  logging.debug(url)
  driver.get(url)
  logging.debug("url reached")


def elementPresent(driver, xpath):
  returnVal = "0"
  try:
    logging.debug(xpath)
    pricevalElem = driver.find_element_by_xpath(xpath)
    if pricevalElem is not None:
      returnVal = "1"
  except:
    pass
  return returnVal

def readXPATHElement(driver, xpath):
  returnVal = ""
  try:
    logging.debug(xpath)
    valElem = driver.find_element_by_xpath(xpath)
    logging.debug(valElem.text)
    returnVal = valElem.text
  except:
    pass
  return returnVal

def readXPATHElementAttribute(driver, xpath, attributename):
  returnVal = ""
  try:
    logging.debug(xpath)
    valElem = driver.find_element_by_xpath(xpath)
    logging.debug(valElem.get_attribute(attributename))
    returnVal = valElem.get_attribute(attributename).text
  except:
    pass
  return returnVal

def setValueOfXPathElement(driver, xpath, toValue):
  try:
    logging.debug("xpath:"+xpath)
    logging.debug("tovalue;"+toValue)
    pricevalElem = driver.find_element_by_xpath(xpath)
    pricevalElem.clear()
    pricevalElem.send_keys(toValue)
  except:
    pass

def clickElement(driver, xpath):
  try:
    logging.debug(xpath)
    pricevalElem = driver.find_element_by_xpath(xpath)
    pricevalElem.click()
  except:
    pass

def write2OutputFile(writer, fmt):
  logging.debug("FMT:::::" + fmt)
  outval = ""
#  get the tokens
  tks = fmt.split(",")
  for tkn in tks[:]:
#   if token starts with $ lookup and substitute
#   else print as is 
    if tkn[0] == "$":
      logging.debug("getting from dict:" + tkn[1:].strip() + ":")
      logging.debug(vardict[tkn[1:].strip()])
      val = vardict.get(tkn[1:].strip(), "NO VALUE FOUND")
    else:
      val = tkn.strip()
    outval = outval + val
    outval = outval + ","
  outval = outval[:len(outval)-1]
  outval = outval + "\n"
  writer.write(outval)
    

def containsStrXpathElem(driver, xpath, substrinelem):
  retval = "0"
  print(xpath)
  try:
    pricevalElem = driver.find_element_by_xpath(xpath)
    logging.debug(":::" + pricevalElem.text)
    logging.debug("::::::::::::::::::::::::::::::::::::::::::::::::::")
    if substrinelem in pricevalElem.text:
      retval = "1"
  except: 
    pass
#   do nothing...
  return retval 
    


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
# make sure the call format is okay
if len(sys.argv) != 2:
  logging.error("format is :::RandomScriptRunner scriptprefix")
  exit()

dt=datetime.today().strftime('%Y-%m-%d')
infile = sys.argv[1] + ".txt"
outfile = sys.argv[1] + dt + ".txt"



linenumber = 1
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument("--test-type")
options.add_argument("user-agent=Kimberly")
options.add_argument("--user-agent=Kimberly")
# options.binary_location = "/usr/bin/chromium"
driver = webdriver.Chrome(chrome_options=options)

# read input file
fin = open(infile, "r") 

# open output file (add datetimestamp yyyymmdd_24HRMMSS)
fout = open(outfile, "w") 

vardict = defaultdict(lambda : None)
vardict["rundatetime"]  = str(datetime.now())

# for each line in input file
for each_line in fin:
# remove leading and trailing spaces
  logging.info("Running line: " + str(linenumber))
  str_line = each_line.strip()
# if emptyline- skip
  if len(str_line) == 0:
    continue
# if starts with #, skip- this is a comment
  if str_line[:1] == "#":
    continue
  logging.debug(":" + str_line + ":")
# split to tokens
  tkns = str_line.split("|")
  logging.debug(tkns)







# COMMANDS
#   gotoURL <URL>
#   readXPATHElement | <xpath> | <toVar>
#   readVarString | <varstring> | <toVar>
#   setValueOfXPathElement | <xpath> | <value>
#   clickOnXpathElement | <xpath>
#   clickOnString | <string>
#   clickOnDropDownOptionXpath | <howerXpath> | <optionString>
#   write2OutputFile "format" 
#        example "$dtvar,$fn,$ln,freetext,$age"
#   containsStrXpathElem | <xpath> | <pattern> | <var>

#interpret the command
  logging.debug(tkns[0])

#   gotoURL <URL>
  if tkns[0].strip() == "gotoURL":
    if len(tkns) != 2:
      logging.error("Format is: " + "gotoURL | <url>")
      continue
    gotoURL(driver, tkns[1].strip())
#   readXPATHElement | <xpath> | <toVar>
  elif tkns[0].strip() == "readXPATHElement":
    if len(tkns) != 3:
      logging.error("Format is: " + "readXPATHElement <xpath> <varname>")
      continue
    vardict[tkns[2].strip()] = readXPATHElement(driver, tkns[1].strip())
    logging.debug("added to dictionary :" + tkns[2].strip() + ":")
    logging.debug(vardict[tkns[2].strip()])
#   readXPATHElementAttribute | <xpath> | <attributename> | <toVar>
  elif tkns[0].strip() == "readXPATHElementAttribute":
    if len(tkns) != 4:
      logging.error("Format is: " + "readXPATHElementAttribute <xpath> <attributename> <varname>")
      continue
    vardict[tkns[3].strip()] = readXPATHElement(driver, tkns[1].strip(), tkns[2].strip())
    logging.debug("added to dictionary :" + tkns[2].strip() + ":")
    logging.debug(vardict[tkns[2].strip()])
#   elementPresent | <xpath> | <toVar>
  elif tkns[0].strip() == "elementPresent":
    if len(tkns) != 3:
      logging.error("Format is: " + "elementPresent <xpath> <varname>")
      continue
    vardict[tkns[2].strip()] = elementPresent(driver, tkns[1].strip())
    logging.debug("added to dictionary :" + tkns[2].strip() + ":")
    logging.debug(vardict[tkns[2].strip()])
#   setValueOfXPathElement | <xpath> | <toValue>
  elif tkns[0].strip() == "setValueOfXPathElement":
    if len(tkns) != 3:
      logging.error("Format is: " + "setValueOfXPathElement <xpath> <toValue>")
      continue
    setValueOfXPathElement(driver, tkns[1].strip(), tkns[2].strip())
#   clickElement | <xpath> 
  elif tkns[0].strip() == "clickElement":
    if len(tkns) != 2:
      logging.error("Format is: " + "clickElement <xpath>")
      continue
    clickElement(driver, tkns[1].strip())
#   write2OutputFile "format" 
  elif tkns[0].strip() == "write2OutputFile":
    if len(tkns) != 2:
      logging.error("Format is: " + "write2OutputFile | <format>")
      continue
    write2OutputFile(fout, tkns[1].strip())
#   containsStrXpathElem | <xpath> | <string to search for> | <resultvariable>
  elif tkns[0].strip() == "containsStrXpathElem":
    logging.debug("switch containsStrXpathElem ")
    if len(tkns) != 4:
      logging.error("Format is: " + "containsStrXpathElem | <xpath> | <string to search for> | <resultvariable>")
      continue
    logging.debug("right params for containsStrXpathElem ")
    vardict[tkns[3].strip()] = containsStrXpathElem(driver, tkns[1].strip(), tkns[2].strip())
  else:
    logging.error("command :" + tkns[0].strip() + ": not supported")
  linenumber = linenumber + 1;
# 
if driver != None:
  driver.quit()


fout.close()
import os
import shutil
s = "C:/Users/U14365/Desktop/scraping/" + outfile
d = "C:/Users/U14365/Desktop/scraping/" + outfile[0:len(outfile)-14]
c = "C:/Users/U14365/Desktop/scraping/" + outfile[0:len(outfile)-14] + "/" + outfile

if os.path.exists(c):
	os.remove(c)
shutil.move(s,d)

