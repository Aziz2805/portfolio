#!/bin/env python3

import psycopg2
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()


def requete3(nom,prenom,date_heure_min,date_heure_max):
    
    conn = psycopg2.connect(
            dbname="aabes",
            user="aabes",
            password="aabes",
            host="data",
            port="5432")
                            
    curseur = conn.cursor()
    
    requete = f"""
        SELECT * FROM (
            SELECT *
            FROM monappli_personne
            WHERE monappli_personne.id IN (
                SELECT monappli_email.personne_id
                FROM monappli_email
                WHERE monappli_email.id IN (
                    SELECT monappli_destinataire.emails_id
                    FROM monappli_destinataire
                    WHERE monappli_destinataire.messages_id IN (
                        SELECT id
                        FROM monappli_message
                        WHERE expediteur_id IN (
                            SELECT id
                            FROM monappli_email
                            WHERE monappli_email.personne_id = (
                                SELECT id
                                FROM monappli_personne
                                WHERE nom = '{nom}' AND prenom = '{prenom}'
                            ))
                            AND monappli_message.date_heure >= '{date_heure_min}'
                            AND monappli_message.date_heure <= '{date_heure_max}'
                        
                    )
                    AND monappli_email.est_interne = 'Y'
                )
            )
    
           UNION
        
        SELECT * 
        FROM monappli_personne p
        WHERE p.id IN (
            SELECT personne_id 
            FROM monappli_email 
            WHERE id IN (
                SELECT expediteur_id 
                FROM monappli_message 
                WHERE (
                    monappli_message.id IN (
                        SELECT messages_id 
                        FROM monappli_destinataire 
                        WHERE emails_id IN (
                            SELECT id 
                            FROM monappli_email
                            WHERE personne_id = (
                                SELECT id 
                                FROM monappli_personne 
                                WHERE nom = '{nom}'
                                AND prenom = '{prenom}'
                            )
                        )
                    ) 
                    AND 
                    (monappli_message.date_heure > '{date_heure_min}'  
                    AND monappli_message.date_heure < '{date_heure_max}')
                )
            )
            AND est_interne = 'Y' 
        )) as personne
        INNER JOIN
        monappli_email as email ON (personne.id = email.personne_id AND email.est_interne='Y');

    """

    curseur.execute(requete)
    
    resultat = curseur.fetchall()
    conn.close()
    return resultat

print(requete3('Blair','Lynn','2002-01-01 00:00:00+01','2005-07-01 00:00:00+01'))
