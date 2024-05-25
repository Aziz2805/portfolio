#!/bin/env python3
# -*- coding: utf-8 -*-
import os
import django
import psycopg2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()

from fonctions_peuplement_maildir import Peuplement_message
from extrait_infos_maildir import extrait_infos

conn = psycopg2.connect(
        dbname="aabes",
        user="aabes",
        password="aabes",
        host="data.stud.mua",
        port="5432")
                        
curseur = conn.cursor()


path = "maildir"

for path, dirs, files in os.walk(path):

    for f in files:
        file = path+'/'+f
        try: 
            with open(file,"r") as fichier:
                file = path+'/'+f
                message = fichier.read()
                try:
    
                    Peuplement_message(message)
    
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


                
