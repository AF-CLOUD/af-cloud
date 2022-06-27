from playwright.sync_api import Playwright as playwright
from playwright.sync_api import sync_playwright, expect
from termcolor import colored
from pyfiglet import Figlet
import requests
import json
import tabulate
import datetime
import termcolor
import time, os, sys
import urllib3
import time
import pytz
import dateutil.parser
import tabulate
from mega import Mega
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import os
import re
from time import sleep


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#--------------------service----------------------
SERVICES = ['', 'Google Drive', 'OneDrive', 'DropBox', 'BOX', 'MEGA']

FC_ERROR        = 0
FC_OK           = 1

# -*- coding: utf-8 -*-

BRIGHT_BLACK = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'
BRIGHT_END = '\033[0m'

class Colors:
	BLACK = '\033[30m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'
	UNDERLINE = '\033[4m'
	RESET = '\033[0m'

class Background:
	BLACK = '\033[40m'
	RED = '\033[41m'
	GREEN = '\033[42m'
	YELLOW = '\033[43m'
	BLUE = '\033[44m'
	MAGENTA = '\033[45m'
	CYAN = '\033[46m'
	WHITE = '\033[47m'

class FC_log(object):
	fp = None
	loglevel = 0
	FC_D = ["debug", "blue", 3]
	FC_I = ["info", "green", 2]
	FC_E = ["error", "red", 0]

	@staticmethod
	def set_loglevel(__loglevel):
		FC_log.loglevel = __loglevel

	@staticmethod
	def log_write(level, text, enter=1, attr=None):
		__level = []
		__loglevel = FC_log.loglevel
		if level == "FC_D":
			__level = FC_log.FC_D
		elif level == "FC_I":
			__level = FC_log.FC_I
		elif level == "FC_E":
			__level = FC_log.FC_E

		if FC_log.fp is None:
			if __level[2] <= __loglevel:
				if enter == 0:
					return print(termcolor.colored("[" + __level[0] + "] " + text, color=__level[1], attrs=attr),
								 end='', flush=True)
				else:
					return print(termcolor.colored("[" + __level[0] + "] " + text, color=__level[1], attrs=attr))
		else:
			if __level[2] <= __loglevel:
				FC_log.fp.write("[" + __level[0] + "] " + text + "\n")

	@staticmethod
	def set_log_fp(output_path, method, modulename="DA"):
		if method is True:
			d = datetime.datetime.today()
			__output_path = output_path + os.sep + modulename + "_" + d.strftime('%y%m%d_%H%M%S_') + str(
				os.getpid()) + ".log"
			FC_log.fp = open(__output_path, 'w', encoding='utf16')
		else:
			FC_log.fp = None

	@staticmethod
	def close_log_fp():
		if FC_log.fp is None:
			pass
		else:
			FC_log.fp.close()


def PRINT(message):
    if type(message) == type(str):
        FC_log.log_write("FC_D", message)
    else:
        FC_log.log_write("FC_D", str(message))


def PRINTI(message):
    if type(message) == type(str):
        FC_log.log_write("FC_I", message)
    else:
        FC_log.log_write("FC_I", str(message))


def PRINTE(message):
    if type(message) == type(str):
        FC_log.log_write("FC_E", message)
    else:
        FC_log.log_write("FC_E", str(message))

