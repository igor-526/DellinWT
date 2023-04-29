#!/bin/bash
#Dellin HelpMeWork v1.0 beta

#Input there your database (only PostgreSQL without SSH)
export HOST=localhost
export DB=dellin
export USER=postgres
export PASSWORD=3611810700
export PORT=5432

#Start settings
export R_DB=0 #reset database (WARNING! WILL DELETE ALL)
export U_AUTO=1 #update auto database (using fixtures/auto.csv)
export U_CONTACTS=1 #update contact database (using fixtures/contacts.csv)
export U_CITY=1
export U_BASES=1

#Input there Telegram bot token
export TOKEN=

venv/bin/python main.py;
