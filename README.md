# MINERO

**Minero** is a simple bot that helps run crypto mining application based on profitability.

NOTE: For it to work, you must already have your mining application ready (ie: claymore, etc)

### How does it work?

1- It gets data from WhatToMine.com.
2- Runs through the list of coins application pair you provided and match the first most
profitable application
3- Runs that application
4- Pauses with the interval
5- After the pauses, checks if there is new profitability
    - YES: Stop the last application and run the new application
    - NO: Keep mining with the old one
... keeps repeating step 1 to 5
6- Profit!

#### NOTE
All Minero does is pick the most profitable coin from the list that you provided,
against data from WhatToMine.com.
You must provide list of application to run in `minero.conf`

### Download

`Minero` is simple, you can either clone this repo to your local, or you can just
copy the content of `minero.py` and paste it in a file on your local called `minero.py`

It's a python application, therefore you will need to type

    python minero.py

for it to run.


### Config

In the directory that you are going to run Minero, you can either
set the config, or let minero do it for you

    python minero.py --init

Or you can copy the content below in `minero.conf`

```
; minero.conf

[general]
INTERVAL = 24 ; In hours. How often you want the script to check for new profitability
MULTI_PROGRAMS = False ; Set to True if you want to mine with multiple programs

[programs]
; Key Value pair of the coin name and the program to run when matched
ETH = C:\YOUR-CLAYMORE-OR-OTHER-PROGRAM-PATH\start_eth.bat
XMR = C:\YOUR-CLAYMORE-OR-OTHER-PROGRAM-PATH\start_xmr.bat
ZEC = C:\YOUR-CLAYMORE-OR-OTHER-PROGRAM-PATH\start_zec.bat
```

### Run

Once setup, just run the line below and profit!

    python minero.py --run

### Extra

You can view all the profitable coins

    python minero.py --all

Or you own profitable coins

    python minery.py --list


---

If you like this script and would like to donate, please do and thank you:

BTC: 1H94UsPEM315S1xrfWMZuxSHqJxyXnZGom

LTC: LNmCDfjMLAj7m3qaqCdnQ8iHhCeuzquStA

BCH: 1CQmM5ev9UR8UtETp9CKdw7kMcsDuAgebZ

ETH: 0x240a68f6ed12772cea76d0000a53983202d1861d

Author: Mardix

Email: mardix@illybee.com

License: MIT

Copyright: 2018 - Mardix


