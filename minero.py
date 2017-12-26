"""
Minero
https://github.com/mardix/minero

Minero is a simple bot that helps run crypto mining application based on profitability. 

For it to work, you must already have your mining application ready. 

All it does is pick the most profitable coin from a list that you provided,
against data from WhatToMine.com 

If you like this script and would like to donate, please do and thank you:

BTC: 1H94UsPEM315S1xrfWMZuxSHqJxyXnZGom
LTC: LNmCDfjMLAj7m3qaqCdnQ8iHhCeuzquStA
BCH: 1CQmM5ev9UR8UtETp9CKdw7kMcsDuAgebZ
ETH: 0x240a68f6ed12772cea76d0000a53983202d1861d

License MIT
----

Setup
To setup, run `minero --init`
"""
##############################################################

import os
import signal
import sys
import json
import subprocess
import argparse
import time

try:
    from urllib.request import Request, urlopen
except ImportError as _:
    from urllib2 import Request, urlopen
try:
    import configparser
except ImportError as _:
    import ConfigParser as configparser

NAME = "Minero"
VERSION = "0.1.0"
AUTHOR = "Mardix"
EMAIL = "mardix@illybee.com"
REPO = "https://github.com/mardix/Minero"

CWD = os.getcwd()
DEFAULT_CONFIG = os.path.join(CWD, "minero.conf")
API_URL = "https://whattomine.com/coins.json"
IS_WIN32 = sys.platform == "win32"

CONF_TPL = """
;--------------------------------------
; Minero config 
; https://github.com/mardix/Minero
;--------------------------------------

[general]
INTERVAL = 4 ; In hours. How often you want the script to check for new profitability coin
MULTI_PROGRAMS = False ; Set to True if you want to mine with multiple programs

[programs]
; Key Value pair of the coin name and the program to run when matched
ETH = C:\YOUR-CLAYMORE-OR-OTHER-PROGRAM-PATH\start_eth.bat
XMR = C:\YOUR-CLAYMORE-OR-OTHER-PROGRAM-PATH\start_xmr.bat
ZEC = C:\YOUR-CLAYMORE-OR-OTHER-PROGRAM-PATH\start_zec.bat
"""

def echo(s, color=None):
    END = '\033[0m'
    COLORS = {
        'blue': "\033[94m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "purple": "\033[95m"
    }
    print(COLORS.get(color) + s + END if color else s)

def run_process(cmd):
    cmd = "%s %s" % ("start /wait " if IS_WIN32 else "open ", cmd)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    return proc

def kill_process(handle):
    if IS_WIN32:
        subprocess.Popen("taskkill /F /T /PID %i" % handle.pid, shell=True)
    else:
        os.kill(handle.pid, signal.SIGKILL)

def load_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    d = dict(config._sections)
    for k in d:
        d[k] = dict(config._defaults, **d[k])
        d[k].pop('__name__', None)
    return d

def query_api():
    ua = "Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
    q = Request(API_URL)
    q.add_header('User-Agent', ua)
    resp = urlopen(q)
    if resp.getcode() == 200:
        return json.loads(resp.read())
    return None

def sort_coins(coins):
    coins.sort(key=lambda x: x[1]['profitability24'], reverse=True)
    return coins

def get_matched_profitable_coin(sorted_coins, coin_keys=[]):
    for _, coin in sorted_coins:
        if coin["tag"].lower() in coin_keys:
            return coin

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.description = "%s %s" % (NAME, VERSION)
        parser.epilog = "Visit %s for updates" % REPO
        parser.add_argument("-r", "--run", help="Run mining process", action="store_true")
        parser.add_argument("--dry", help="Perform a dry run of the mining process",action="store_true")
        parser.add_argument("-l", "--list", help="List your profitable coins only", action="store_true")
        parser.add_argument("--all", help="Show all profitable coins ", action="store_true")
        parser.add_argument("--config", help="To initiate the config file ")
        parser.add_argument("--init", help="To initiate the config file ", action="store_true")
        arg = parser.parse_args()

        echo("")
        echo("$" * 80)
        echo("===== %s %s =====" % (NAME, VERSION), "purple")
        echo("$" * 80)
        echo("")

        conf_file = arg.config or DEFAULT_CONFIG
        if not os.path.isfile(conf_file) and not arg.init:
            raise Exception("Missing config file. Run `python minero.py --init` to create one in the current directory")

        if arg.init:
            if not os.path.isfile(DEFAULT_CONFIG):
                with open(DEFAULT_CONFIG, "w") as f:
                    f.write(CONF_TPL)

            echo("Minero is setup!", "green")
            echo("Run `python minero.py --run` to start", "green")
            print("")
            exit()

        conf = load_config(conf_file)
        programs = conf.get("programs")
        general_conf = conf.get("general", {})
        programs_keys = [k.lower() for k in programs.keys()]
        interval = general_conf.get('interval', 4)  # in hours
        interval *= 3600

        if arg.run or arg.dry:
            proc = None
            coin = {}
            dry_text = "dry " if arg.dry else ""
            echo("//%s Running mining process..." % dry_text, "green")
            while True:
                if coin:
                    echo("quering WhatToMine.com...")
                data = query_api()
                if data:
                    reset = False
                    sorted_coins = sort_coins(data["coins"].items())
                    profitable_coin = get_matched_profitable_coin(sorted_coins, programs_keys)
                    if profitable_coin and coin.get("tag") != profitable_coin["tag"]:
                        reset = True
                        coin = profitable_coin
                        echo("")
                        echo("*** Found the most profitable coin from your list to mine:", "green")
                        echo("-" * 20)
                        echo(":: %s %s" % (coin["tag"], coin["profitability24"]), "green")
                        echo("-" * 20)
                    if reset is True:
                        cmd = programs[coin.get("tag").lower()]
                        if arg.dry:
                            echo("exiting...")
                            echo("")
                            exit()
                        else:
                            if proc and general_conf.get('muti_programs', False) is False:
                                echo("removing last mining program...", "blue")
                                kill_process(proc)
                                echo("...")
                                time.sleep(10)
                            echo("starting mining program for '%s'... " % coin.get("tag"), "purple")
                            run_process(cmd)
                            echo("mining '%s'..." % coin.get("tag"), "blue")
                    else:
                        echo("mining '%s'..." % coin.get("tag"), "blue")
                else:
                    echo("!!! WARNING: Could not receive data from WhatToMine.com.", "red")
                time.sleep(interval)

        elif arg.list or arg.all:
            title = "Listing all coins profitability"
            if arg.list:
                title = "Listing your coins by profitability"
            echo("// %s" % title, "purple")
            data = query_api()
            if data:
                for coin_ in sort_coins(data["coins"].items()):
                    coin = coin_[1]
                    if arg.list:
                        if coin["tag"].lower() in programs_keys:
                            echo(":: %s %s" % (coin["tag"], coin["profitability24"]))
                    else:
                        echo(":: %s %s" % (coin["tag"], coin["profitability24"]))
    except Exception as e:
        echo("!!! ERROR: %s" % e, "red")
