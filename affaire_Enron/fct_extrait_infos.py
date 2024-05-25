#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import django
import psycopg2
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

Dict_mois_sent = {'January':1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,
"October":10,"November":11,"December":12}

Dict_mois = {'Jan':1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,
             "Oct":10,"Nov":11,"Dec":12}

def extrait_infos(message):
    
        pattern_date_heure = re.compile(r"^Date: ..., (..) (...) (....) (........) (.....)")
        pattern_expediteur = re.compile(r"^From: (.+)")
        pattern_objet = re.compile(r"^Subject: (.+)")
        pattern_destinataires = re.compile(r"^To: (.+)")
        pattern_cc = re.compile(r"Cc: (.+)")
        pattern_bcc = re.compile(r"Bcc: (.+)")
        pattern_date_heure_sent = re.compile(r"^Sent(?:=09)?:\s*(.+), (.+?) (\d{1,2}), (\d{4}) (\d{1,2}:\d{2}) (AM|PM)")


        found_date_heure = pattern_date_heure.search(message.strip())
        found_expediteur = pattern_expediteur.match(message.strip())
        found_objet = pattern_objet.search(message.strip())
        found_destinataires = pattern_destinataires.search(message.strip())
        found_cc = pattern_cc.search(message.strip())
        found_bcc = pattern_bcc.search(message.strip())
        found_date_heure_sent = pattern_date_heure_sent.search(message.strip())
        
        new_message= Message()
        
        if found_date_heure:
            #Bon format : 2001-04-25 10:55:12-0700
            annee = found_date_heure.groups()[2]
            mois = Dict_mois[found_date_heure.groups()[1]]
            jour = found_date_heure.groups()[0]
            heure = found_date_heure.groups()[3]
            fuseau = found_date_heure.groups()[4]

            s = f"{annee}-{mois}-{jour} {heure}{fuseau}"
    
            print(f"DateTime : {s}")
        
        
        if found_date_heure_sent:
            
            jour_sem = found_date_heure_sent.groups()[0]
            mois = Dict_mois_sent[found_date_heure_sent.groups()[1]]
            jour = found_date_heure_sent.groups()[2]
            annee = found_date_heure_sent.groups()[3]
            heure,minute = found_date_heure_sent.groups()[4].split(":")
            apm = found_date_heure_sent.groups()[5]


            if apm == "PM":
                heure = int(heure)
                heure += 12

            s = f"{annee}-{mois}-{jour} {heure}:{minute}:00-0700"

            print(f"Sent: {s}")

        
        if found_expediteur:
            
            adresse_mail = found_expediteur.groups()[0]
            
            print(f"Expediteur_email = {adresse_mail}")
    
            curseur.execute(f"SELECT id from monappli_email WHERE adresse_mail = '{adresse_mail}'")
            resultat = curseur.fetchone()
            
            if not resultat:
                print("PAS DANS LA BASE")
            else:
                print(f"DANS LA BASE : ID = {resultat}")
                
                
        if found_objet:
            print(f"Objet: {found_objet.groups()}")
        
        if found_destinataires:
            print(f"Destinataires: {found_destinataires.groups()}")
        
        if found_cc:
            print(f"Cc : {found_cc.groups()}")
            
        if found_bcc:
            print(f"Bcc : {found_bcc.groups()}")