#!/bin/env python3
import os
import django
import xml.etree.ElementTree as ET

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()

from monappli.models import Personne,Email

tree = ET.parse('/users/2024/ds1/192014034/affaire_Enron/employes_enron.xml')
root = tree.getroot()

for employee in root.findall('employee'):
  
    new_personne = Personne()
    
    new_personne.nom = employee.find('lastname').text
    new_personne.prenom = employee.find('firstname').text
    new_personne.categorie = employee.get('category') if employee.get('category') else "N/A"
    new_personne.boite_mail = employee.find('mailbox').text

    new_personne.save()
    
    email_addresses = [email.attrib['address'] for email in employee.findall('email')]
    
    for email_address in email_addresses:
        
        email = Email()
        email.adresse_mail = email_address
        email.est_interne = "Y"
        email.personne = new_personne
        email.save()
personne_nodata = Personne()
personne_nodata.nom,personne_nodata.prenom,personne_nodata.categorie,personne_nodata.boite_mail = "N/A","N/A","N/A","N/A"
personne_nodata.save()