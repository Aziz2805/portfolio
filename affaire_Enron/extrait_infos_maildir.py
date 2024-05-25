#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()

from monappli.models import Personne, Email, Message, Destinataire
import email
from email import policy
from email.parser import BytesParser


Dict_mois = {'Jan':1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,
             "Oct":10,"Nov":11,"Dec":12}

def extrait_body(msg_str):
    msg = BytesParser(policy=policy.default).parsebytes(msg_str.encode('utf-8'))
    if msg.is_multipart():
        return extrait_body(msg.get_payload(0))
    else:
        payload = msg.get_payload(decode=True)
        if isinstance(payload, bytes):
            charset = msg.get_content_charset() or 'utf-8' 
            payload = payload.decode(charset)
        return payload
    
def extrait_header(email_str):
    msg = email.message_from_string(email_str)
    headers_string = ""
    for key, value in msg.items():
        headers_string += f"{key}: {value}\n"
    return headers_string
    
   
def extrait_infos(message):
    
        Expediteur = None
        Destinataires = None
        DateHeure = None
        Objet = None
        Cc = None
        Bcc = None
        Mailbox = None
        
        MetaDonnees = {"Expediteur":Expediteur,"Destinataires":Destinataires,"DateTime":DateHeure,"Objet":Objet,"Mailbox":Mailbox}
        
        header = extrait_header(message)

        Destinataires = re.findall(r"To:(.+)Subject", header,re.DOTALL)
        Cc = re.findall(r"Cc:(.+)Mime-Version", header,re.DOTALL)
        Bcc = re.findall(r"Bcc:(.+)X-From", header,re.DOTALL)

        for line in header.splitlines():
            
            found_expediteur = re.match(r"^From:(.+)", line.strip())

            found_objet = re.match(r"^Subject:(.+)", line.strip())
            found_cc = re.match(r"^Cc:(.+)", line.strip())
            found_bcc = re.match(r"^Bcc:(.+)", line.strip())
            found_date_heure = re.match(r"^Date: ..., (..*) (...) (....) (........) (.....)", line.strip())
            found_mailbox = re.match(r"^X-Origin:(.+)", line.strip())
            
            if found_date_heure:
                
                #Bon format : 2001-04-25 10:55:12-0700
                annee = found_date_heure.groups()[2]
                mois = Dict_mois[found_date_heure.groups()[1]]
                jour = found_date_heure.groups()[0]
                heure = found_date_heure.groups()[3]
                fuseau = found_date_heure.groups()[4]
    
                DateHeure = f"{annee}-{mois}-{jour} {heure}{fuseau}"

            if found_expediteur:
                
                adresse_mail = found_expediteur.groups()[0]
                Expediteur = adresse_mail
               
            if found_objet:
                Objet = found_objet.groups()[0]
            
            if found_mailbox:
                Mailbox = found_mailbox.groups()[0].lower().strip()


        Destinataires = [destinataire.strip().replace("\n", "").replace("\t","") for destinataire in Destinataires]

        if Destinataires != []:
            Destinataires = Destinataires[0].split(", ")

        if Cc:
            Cc = [cc.strip().replace("\n", "").replace("\t","") for cc in Cc]
            Cc = Cc[0].split(", ")
        
        if Bcc:
            Bcc = [bcc.strip().replace("\n", "").replace("\t","") for bcc in Bcc]
            Bcc = Bcc[0].split(", ")
        
        Destinataires = list(set(Destinataires + Cc + Bcc))

        MetaDonnees["Expediteur"]=Expediteur
        MetaDonnees["DateTime"]=DateHeure
        MetaDonnees["Objet"]=Objet
        MetaDonnees["Destinataires"]=Destinataires
        MetaDonnees["Mailbox"]=Mailbox

        return MetaDonnees