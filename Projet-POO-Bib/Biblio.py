#!/usr/bin/env python3

# PROJET POO 

# PARTIE 1

from reportlab.pdfgen import canvas
from ebooklib import epub
import PyPDF2
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse,urljoin
import os

class FormatError(Exception):
    pass


class base_livre:
      def __init__(self, ressource):
        self.ressource = ressource
    
      def getTitre(self):
        return self.titre
    
      def getAuteur(self):
        return self.auteur
    
      def getLangue(self):
        return self.langue
    
      def getSujet(self):
        return self.sujet
    
      def getDate(self):
        return self.date

 

# QUESTION 1

class LivrePDF(base_livre):
    
      def __init__(self, ressource):
        super().__init__(ressource)
        
        with open(ressource, 'rb') as f:
            
          pdf = PyPDF2.PdfReader(f)
          info = pdf.metadata
          
          self.langue = ""   
          
          try:
              self.auteur = info.author
          except:
              return None
          try:
              self.sujet = info.subject
          except:
              return None
          try: 
              self.titre = info.title
          except:
              return None
          try: 
              self.date = info.creation_date
          except:
              return None
        
    
      def getType(self):
        return "PDF"

 

class LivreEPUB(base_livre):
    
      def __init__(self, ressource):
        super().__init__(ressource)
        livreEpub = epub.read_epub(self.ressource)
        
        try:
            self.titre = livreEpub.get_metadata('DC', 'title')[0][0]
        except:
            return None
        try:
            self.auteur = ', '.join(author[0] for author in livreEpub.get_metadata('DC', 'creator'))
        except:
            return None
        try:
            self.langue = livreEpub.get_metadata('DC', 'language')[0][0]
        except:
            return None
        try: 
            self.date = livreEpub.get_metadata('DC', 'date')
        except:
            return None
        try:
            self.sujet = livreEpub.get_metadata('DC', 'subject')[0]
        except:
            return None
    
      def getType(self):
        return "EPUB"

#QUESTION 2

class base_bibli:
    
    def __init__(self,path):
        self.path = path


class SimpleBibli(base_bibli):
    
    def __init__(self, path, livres=[]):
        super().__init__(path)
        self.livres = livres

    def ajouter(self, livre):
        self.livres.append(livre)


    def rapport_livres(self, Format, fichier):
        
            if Format == "PDF":
                chemin = self.path + "/" + fichier + ".pdf"
                    
                with open(chemin, 'wb') as pdf_file:
                    pdf = canvas.Canvas(pdf_file)
                    pdf.setFont("Helvetica", 8)
                    pdf.drawString(50, 800, f"Format rapport : {Format}")
                    y_position = 780
                    k=1
                    for livre in self.livres:
                        y_position -= 20 
                        pdf.drawString(50, y_position, f"{k}/ Titre: {livre.getTitre()}, Auteur : {livre.getAuteur()}, Type : {livre.getType()}, Fichier : {fichier}.pdf")
                        k+=1
                        if y_position <= 100: 
                            pdf.showPage()  
                            pdf.setFont("Helvetica", 8)
                            y_position = 780  
                    pdf.save()
                    
            elif Format == "EPUB":
                chemin_epub = self.path + "/" + fichier + ".epub"
                livre = epub.EpubBook()
                livre.set_title(f"Format rapport : {Format}")
                contenu = []
                for livre in self.livres:
                    contenu.append(epub.EpubItem(uid=f"livre_{livre.getTitre()}", file_name=f"{livre.getTitre()}.html", content=f"<h1><p>Titre: {livre.getTitre()}, Ressource: {livre.ressource}<p>"))
                for item in contenu:
                    livre.add_item(item)
                livre.spine = contenu
                epub.write_epub(chemin_epub, livre, {})

                 
            else:
                raise FormatError(f"Le format {Format} n'est pas supportÃ©")



    def rapport_auteurs(self, Format, fichier):
    
            auteurs = []
            
            for livre in self.livres:
                auteur = livre.getAuteur()
                if auteur not in auteurs:
                    auteurs.append(auteur)
                
            if Format == "PDF":
                 chemin = self.path + "/" + fichier + ".pdf"
                  
                 with open(chemin, 'wb') as pdf_file:
                    pdf = canvas.Canvas(pdf_file)
                    pdf.setFont("Helvetica", 8)    
                    pdf.drawString(50, 800, f"Format rapport : {Format}")
                    y_position = 780
                    for auteur in auteurs :
                        k=1
                        y_position -= 20
                        pdf.drawString(50, y_position, f"Auteur : {auteur}")
                        for livre in self.livres:
                            if livre.getAuteur() == auteur:
                                    y_position -= 20  
                                    pdf.drawString(50, y_position, f"{k}/ Titre: {livre.getTitre()}, Ressource: {livre.ressource},Type: {livre.getType()}")
                                    k+=1
                            if y_position <= 100: 
                                
                                pdf.showPage()
                                pdf.setFont("Helvetica", 8)
                                y_position = 780 
                    pdf.save()
                    
            elif Format == "EPUB":
                    chemin_epub = self.path + "/" + fichier + ".epub"
                    livre = epub.EpubBook()
                    livre.set_title(f"Format rapport : {Format}")
                    for auteur in auteurs:
                        contenu_auteurs = ""
                        for livre in self.livres:
                            if livre.getAuteur() == auteur:
                                contenu_auteurs += f"<p>Titre: {livre.getTitre()}, Ressource: {livre.ressource}, Type: {livre.getType()}</p>"
                        item = epub.EpubItem(uid=f"author_{auteur}", file_name=f"author_{auteur}.html", content=contenu_auteurs)
                        livre.add_item(item)
                    livre.spine = [item for item in livre.items]
                    epub.write_epub(chemin_epub, livre, {})

            else:
                
                raise FormatError(f"Le format {Format} n'est pas supporté")
            
"""

#TEST QUESTION 2

L1 = LivrePDF("/home/aziz/POO/Projet-POO/livres/aicard_illustre_maurin.pdf")
L2 = LivreEPUB("/home/aziz/POO/Projet-POO/livres/aicard_maurin_des_maures.pdf")

T = [L1,L2]

bibliotheque = SimpleBibli("/home/aziz/POO/Projet-POO")

for livre in T:
    bibliotheque.ajouter(livre)

Tableau_formats = ["PDF","JPG","EPUB","TXT", "PNG"]

for Format in Tableau_formats:
    try:
        bibliotheque.rapport_livres(Format, "rapport_livres")
        
        bibliotheque.rapport_auteurs(Format, "rapport_auteurs")
        
    except FormatError as e:
        print(e)
"""
    
#Question 3:

class Bibli(SimpleBibli):
    
    def telecharger_livre(self, ressource, base_url):
            analyse_url = urlparse(ressource)
            if not analyse_url.scheme:
                ressource = urljoin(base_url, ressource)
            nom_fichier = os.path.basename(ressource)
            repertoire_local = os.path.join(self.path, nom_fichier)
            try:
                reponse = requests.get(ressource, verify=False)
                reponse.raise_for_status()
                
                with open(repertoire_local, 'wb') as f:
                    f.write(reponse.content)
                
                return repertoire_local
            except requests.exceptions.RequestException as e:
                import traceback
                print(f"échec de téléchargement du livre depuis {ressource}: {e}")
                traceback.print_exc()
                return None

        
        
    def alimenter(self, url):
        reponse = requests.get(url, verify=False)
        code_html = BeautifulSoup(reponse.text, 'html.parser')
        ressources = code_html.find_all('a')
        
        for ressource in ressources:
            href = ressource.get('href')
            if href.endswith(".pdf") or href.endswith(".epub"):
                livre_telecharge = self.telecharger_livre(href, base_url=url)
                if livre_telecharge:
                    if href.endswith(".pdf"):
                        livre = LivrePDF(ressource=livre_telecharge)
                    elif href.endswith(".epub"):
                        livre = LivreEPUB(ressource=livre_telecharge)
                    self.ajouter(livre)
            else:
                pass
            
"""
#Test fonction alimenter:
    
    
bibliotheque_en_ligne = Bibli("/home/aziz/POO/Projet-POO")

# URL de la page web contenant la liste des livres

url_page_web = "https://tibo.life/index3"

# Alimenter la bibliothèque à partir de la page web

bibliotheque_en_ligne.alimenter(url_page_web)

#Rédaction du rapport pour visualiser le résultat

bibliotheque_en_ligne.rapport_livres("PDF", "rapport_livres")
"""


# Question 4

class Bibli_scrap(Bibli):
    
    def __init__(self, path, etats_path):
        super().__init__(path)
        self.etats_path = etats_path
    
    def scrap(self, url, profondeur, nbmax):
        if profondeur == 0 or nbmax == 0:
            return
        
        try:
            reponse = requests.get(url, verify=False)
            reponse.raise_for_status()
            code_html = BeautifulSoup(reponse.text, 'html.parser')
            ressources = code_html.find_all('a')

            for ressource in ressources:
                href = ressource.get('href')
                if href.endswith(".pdf") or href.endswith(".epub"):
                    livre_telecharge = self.telecharger_livre(href, base_url=url)
                    if livre_telecharge:  
                        if href.endswith(".pdf"):
                            livre = LivrePDF(ressource=livre_telecharge)
                        elif href.endswith(".epub"):
                            livre = LivreEPUB(ressource=livre_telecharge)
                        self.ajouter(livre)
                        nbmax -= 1
                        if nbmax == 0:
                            break

            liens = [urljoin(url, link.get('href')) for link in code_html.find_all('a', href=True)]
            for lien in liens:
                self.scrap(lien, int(profondeur) - 1, nbmax)
                
                
        
        except requests.exceptions.RequestException as e:
            import traceback
            print(f"échec de la suppression de {url}: {e}")
            traceback.print_exc()


"""
# Example usage:
    
biblio_scrap = Bibli_scrap("/home/aziz/POO/Projet-POO","=/home/aziz/POO/Projet-POO/rapports")

url_page_web = "https://math.univ-angers.fr/~jaclin/biblio/livres"
profondeur = 1

biblio_scrap.scrap(url_page_web, profondeur, 10)


biblio_scrap.rapport_livres("PDF", "rapport_livres")
biblio_scrap.rapport_auteurs("PDF", "rapport_auteurs")
"""
