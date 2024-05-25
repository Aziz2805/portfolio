from django.shortcuts import render,redirect
from django.conf import settings
# Create your views here.
from django.http import HttpResponse
from monappli.models import Personne, Email, Message, Destinataire
from .forms import form_requete6, form_requete4, form_requete3, form_choix_requete1, form_requete1_mail, form_requete1_nomprenom, form_requete5, form_requete2
from psycopg2 import sql
import psycopg2
from requete3 import requete3
from requete4 import requete4
from requete1 import requete1_nomprenom, requete1_mail
from requete5 import requete5
from requete2 import requete2
from requete6 import requete6
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affaire_Enron.settings')
django.setup()



def vue_requete6(request):
    if request.method =="POST":
        form = form_requete6(request.POST)
        if form.is_valid():
            mode = form.cleaned_data.get('mode')
            mots = form.cleaned_data.get('mots').split(',')
            resultat = requete6(mots,mode)
            return render(request,'resultat_requete6.tmpl',{'resultat':resultat,'mode':mode})
    else:
        form = form_requete6()
    return render(request,'form_requete6.tmpl',{'form':form})


def page_accueil(request):
    return render(request,'accueil.tmpl')



def vue_affiche_contenu(request, message_id):
    try:
        conn = psycopg2.connect(
            dbname="achennoufi",
            user="achennoufi",
            password="achennoufi",
            host="data",
            port="5432"
        )
        curseur = conn.cursor()
        requete = f"SELECT contenu FROM monappli_message WHERE id = %s"
        curseur.execute(requete, (message_id,))
        resultat = curseur.fetchone()
        contenu = resultat[0] if resultat else "Message non trouvé"

        curseur.close()
        conn.close()

    except Exception as e:
        contenu = f"Erreur de connexion à la base de données : {str(e)}"

    return render(request, 'contenu.tmpl', {'message_id': message_id, 'contenu': contenu})


def vue_requete2(request):
    if request.method == 'POST':
        form = form_requete2(request.POST)
        if form.is_valid():
            type_message = form.cleaned_data.get('type_message')
            signe = form.cleaned_data.get('signe')
            nb_min = form.cleaned_data.get('nb_min')
            date_inf = form.cleaned_data.get('date_inf')
            date_sup = form.cleaned_data.get('date_sup')
            resultat = requete2(type_message,signe,nb_min,date_inf,date_sup)
            return render(request,'resultat_requete2.tmpl',{'resultat':resultat, 'type_message':type_message})
    else:
        form = form_requete2()
    return render(request,'form_requete2.tmpl',{'form':form})


def vue_requete4(request):
    if request.method == 'POST':
        form = form_requete4(request.POST)
        if form.is_valid():
            date_inf = form.cleaned_data.get('date_inf')
            date_sup = form.cleaned_data.get('date_sup')
            seuil = form.cleaned_data.get('seuil')
            resultat = requete4(date_inf,date_sup,seuil)
            return render(request,'resultat_requete4.tmpl',{'resultat':resultat})
    else:
        form = form_requete4()
    return render(request,'form_requete4.tmpl',{'form':form})


def vue_requete3(request):
    if request.method=='POST':
        form = form_requete3(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            prenom = form.cleaned_data.get('prenom')
            date_heure_inf = form.cleaned_data.get('date_heure_inf')
            date_heure_sup = form.cleaned_data.get('date_heure_sup')
            resultat = requete3(nom,prenom,date_heure_inf,date_heure_sup)
            return render(request,'resultat_requete3.tmpl',{'resultat':resultat})
    else:
        form = form_requete3()
        return render(request,'form_requete3.tmpl',{'form':form})

import matplotlib.pyplot as plt

def vue_requete5(request):
    if request.method == 'POST':
        form = form_requete5(request.POST)
        
        if form.is_valid():
            date_inf = form.cleaned_data.get('date_inf')
            date_sup = form.cleaned_data.get('date_sup')
            resultat = requete5(date_inf, date_sup)

            dates = [entry[0] for entry in resultat]
            mails_total = [entry[1] for entry in resultat]
            mails_internes = [entry[2] for entry in resultat]
            mails_externes = [entry[3] for entry in resultat]

            plt.bar(dates, mails_total, label='Total')
            plt.bar(dates, mails_internes, label='Internes')
            plt.bar(dates, mails_externes, label='Internes-Externes', bottom=mails_internes) 

            plt.xlabel('Date')
            plt.ylabel('Nombre de mails')
            plt.title('Histogramme des échanges de mails')
            plt.legend()
            plt.xticks(rotation=90,fontsize=8)
        
            chemin = os.path.join(settings.BASE_DIR, 'static', 'histogramme.png')
            plt.savefig(chemin,bbox_inches='tight')
            plt.clf()

            return render(request, 'resultat_requete5.tmpl', {'resultat': resultat, 'histogram_path': chemin})

    else:
        form = form_requete5()

    return render(request, 'form_requete5.tmpl', {'form': form})



def vue_requete1(request):
    if request.method == 'POST':
        form = form_choix_requete1(request.POST)
        
        if form.is_valid():
            if form.cleaned_data.get('choix') == 'nomprenom':
                return redirect('vue_requete1_nomprenom')
            
            else:
                return redirect('vue_requete1_mail')
    else:
        form = form_choix_requete1()
    return render(request,'form_choix_requete1.tmpl',{'form':form})
            

def vue_requete1_nomprenom(request):

    if request.method == 'POST':
        form = form_requete1_nomprenom(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            prenom = form.cleaned_data.get('prenom')
            resultat = requete1_nomprenom(nom, prenom)
            return render(request,'resultat_requete1_nomprenom.tmpl',{'resultat':resultat})
    else:
        form = form_requete1_nomprenom()
        return render(request, 'form_requete1_nomprenom.tmpl', {'form': form})

def vue_requete1_mail(request):

    if request.method == 'POST':
        form = form_requete1_mail(request.POST)
        if form.is_valid():
            adresse_mail = form.cleaned_data.get('adresse_mail')
            resultat = requete1_mail(adresse_mail)
            return render(request,'resultat_requete1_mail.tmpl',{'resultat':resultat})
    else:
        form = form_requete1_mail()

    return render(request, 'form_requete1_mail.tmpl', {'form': form})
