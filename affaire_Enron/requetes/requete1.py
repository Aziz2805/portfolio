#!/bin/env python3

import psycopg2
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()


conn = psycopg2.connect(
        dbname="achennoufi",
        user="achennoufi",
        password="achennoufi",
        host="data",
        port="5432")
                        
curseur = conn.cursor()

reponse = input("nom ou adresse mail ?")



if reponse == "nom":

    nom = input("nom : ")

    requete = f"""
                SELECT * 
                FROM 
                    monappli_personne AS personne
                INNER JOIN 
                    (SELECT * 
                    FROM monappli_email 
                    WHERE monappli_email.personne_id IN 
                        (SELECT monappli_personne.id 
                            FROM monappli_personne 
                            WHERE monappli_personne.nom = '{nom}')) AS email
                ON personne.id = email.personne_id;
                """


if reponse == "adresse mail":

    adresse_mail = input("adresse mail : ")

    requete = f"""
                SELECT * 
                FROM 
                    (SELECT * 
                    FROM monappli_personne 
                    WHERE id = 
                        (SELECT personne_id 
                            FROM monappli_email 
                            WHERE monappli_email.adresse_mail = '{adresse_mail}')
                    ) AS personne
                INNER JOIN 
                    monappli_email AS email 
                ON 
                    personne.id = email.personne_id;
                """

curseur.execute(requete)


resultats = curseur.fetchall()

for ligne in resultats:
    print(ligne)

conn.close()