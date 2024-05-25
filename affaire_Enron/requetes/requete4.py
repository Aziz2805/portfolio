#!/bin/env python3

import psycopg2
import os
import django
from psycopg2 import sql


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()


def requete4(date_inf, date_sup, seuil):
    try:
        conn = psycopg2.connect(
            dbname="aabes",
            user="aabes",
            password="aabes",
            host="data",
            port="5432"
        )

        with conn:
            with conn.cursor() as curseur:
                requete = sql.SQL("""
                    SELECT p1.nom as nom_expediteur, p1.prenom as prenom_expediteur, 
                           p2.nom as nom_destinataire, p2.prenom as prenom_destinataire, 
                           COUNT(*) as nombre_mails_echanges 
                    FROM monappli_personne p1 
                    JOIN monappli_email em1 ON p1.id = em1.personne_id 
                    JOIN monappli_message m ON em1.id = m.expediteur_id 
                    JOIN monappli_destinataire d ON m.id = d.messages_id 
                    JOIN monappli_email em2 ON d.emails_id = em2.id 
                    JOIN monappli_personne p2 ON em2.personne_id = p2.id 
                    WHERE m.date_heure >= %s AND m.date_heure <= %s 
                    AND p1.id != 150 AND p2.id != 150
                    GROUP BY p1.id, p2.id 
                    HAVING COUNT(*) >= %s
                    ORDER BY COUNT(*) DESC;
                """)

                curseur.execute(requete, (date_inf, date_sup, seuil))
                resultat = curseur.fetchall()

                return resultat

    except psycopg2.Error as e:
        print("Error:", e)

# Example usage:
print(requete4('2002-01-01', '2002-12-01', 10))

    
    