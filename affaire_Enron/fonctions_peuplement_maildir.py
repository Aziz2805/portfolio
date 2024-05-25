#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()

import re
from monappli.models import Personne, Email, Message, Destinataire
import psycopg2
from extrait_infos_maildir import extrait_infos, extrait_body

conn = psycopg2.connect(
        dbname="aabes",
        user="aabes",
        password="aabes",
        host="data.stud.mua",
        port="5432")
                        
curseur = conn.cursor()


def ajoute_email(email):
    try:
        curseur.execute("SELECT id FROM monappli_email WHERE adresse_mail = %s", (email,))
        personne_id = curseur.fetchone()

    except psycopg2.Error:
        personne_id = None
    
    if personne_id:
        email_obj = Email.objects.get(adresse_mail=email)

    else:
        personne_nodata = Personne.objects.get(id=150)
        email_obj = Email.objects.create(adresse_mail=email, personne=personne_nodata, est_interne="Y" if "@enron" in email else "N")

    return email_obj

def nettoie_email(email):
    if "<" not in email and "[" not in email:
        return email.strip()

    else:
        match = re.search(r"[<\[]?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})[>\]]?", email)
        if match:
            return match.group(1).strip()


def Peuplement_message(message):

    new_message = Message()
    metadonnees = extrait_infos(message)
    
    new_message.objet = metadonnees["Objet"]
    new_message.date_heure = metadonnees["DateTime"].strip()
    new_message.contenu = extrait_body(message)
    
    expediteur = metadonnees["Expediteur"]
    expediteur = nettoie_email(expediteur)

    new_message.expediteur = ajoute_email(expediteur)

    destinataires = metadonnees["Destinataires"]

    new_message.save()

    if destinataires == []:

        curseur.execute("SELECT adresse_mail FROM monappli_email WHERE personne_id = (SELECT id FROM monappli_personne WHERE monappli_personne.boite_mail = %s)", (metadonnees["Mailbox"],))
        
        email_obj = Email.objects.get(adresse_mail=curseur.fetchone()[0])
        
        destinataire = Destinataire.objects.create(emails=email_obj,messages=new_message)
    
    for dest in destinataires:
        dest = nettoie_email(dest)
        destinataire = Destinataire.objects.create(emails=ajoute_email(dest), messages=new_message)

