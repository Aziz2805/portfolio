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


requete = f"""
SELECT date(date_heure), COUNT(*) AS nombre_mails 
FROM (
    SELECT date_heure 
    FROM monappli_message 
    WHERE date(date_heure) > '2002-01-01' 
        AND date(date_heure) < '2002-06-01'
) AS subquery 
GROUP BY date(date_heure);
"""