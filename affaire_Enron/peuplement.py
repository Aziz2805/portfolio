#!/bin/env python3
import re
import os
import django
from django.core.exceptions import ObjectDoesNotExist
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
#'django_extensions'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()
from monappli.models import Employe, Email

"""
tree = ET.parse('/users/2024/ds1/192014034/affaire_Enron/employes_enron.xml')
root = tree.getroot()

for employee in root.findall('employee'):
    new_employe = Employe()
    
    new_employe.nom = employee.find('lastname').text
    new_employe.prenom = employee.find('firstname').text
    new_employe.categorie = employee.get('category') if employee.get('category') else "N/A"
    new_employe.boite_mail = employee.find('mailbox').text

    new_employe.save()

    email_addresses = [email.attrib['address'] for email in employee.findall('email')]
    
    for email_address in email_addresses:

        email = Email()
        email.adresses_mail = email_address
        email.employe = new_employe
        email.save()

"""

path = "maildir"


for path, dirs, files in os.walk(path):
    for f in files:
        file = path+'/'+f
        print(file)
        
        pattern = re.compile(r'.*To: (.+@.+) ')
        echecs=[]
        
        with open(file,"r") as fichier:
            contenu = fichier.read()
            print(contenu)

            for line in fichier:
                    found = pattern.search(line.strip())
                    
                    if not found:
                        echecs += [line]
                        continue  
                    print(fichier)
                    print(found.groups())           

                    
# (Subject:|Subject: RE:) (\S+) +.*
#From: (.+@enron.com) +
# *Date: (.*?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) .*'

                
                
 