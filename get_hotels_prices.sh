#!/bin/bash

# Run Ramada Encore
/usr/bin/python3 /opt/price-scraper/ramadaencore.py
sleep 2m

# Run Royal Orchid
/usr/bin/python3 /opt/price-scraper/royalorchid.py
sleep 2m

# Run Sarovar
/usr/bin/python3 /opt/price-scraper/sarovar.py
sleep 2m

# Run Lemon Tree
/usr/bin/python3 /opt/price-scraper/lemontree.py
sleep 2m

# Run Ginger
/usr/bin/python3 /opt/price-scraper/ginger.py
