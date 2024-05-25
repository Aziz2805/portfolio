#!/bin/env python3
import re
import os
import django
import psycopg2

from fct_extrait_infos import extrait_infos

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()

from monappli.models import Employe, Email, Message, Destinataire



conn = psycopg2.connect(
        dbname="aabes",
        user="aabes",
        password="aabes",
        host="data",
        port="5432")
                        
curseur = conn.cursor()

                    
path = "maildir"

print("!!!!!!!!!!!!!!!!!!!!!!!!!! DEBUT DU PROGRAMME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

for path, dirs, files in os.walk(path):
    
    compteur = 1
        
    for f in files:
        file = path+'/'+f
        
        print(f"_____________Mail n° {compteur}_____________")
        print(f"PATH = {file}")
        
        
        with open(file,"r") as fichier:
            message = ""
            
            for line in fichier:
                message += line
                
            L = message.split("-----Original Message-----")
            
            print(f"Longueur de la conversation : {len(L)}")
            
            if len(L)>1:
                
                for message in L:
                    for line in message.splitlines():
                        extrait_infos(line)
                        
            else:
                fichier.seek(0)
                for line in fichier:
                    extrait_infos(line)
        compteur += 1 

                    
         
