##ETAPE 3 : 

import sys, os
from Biblio import base_livre, LivrePDF, LivreEPUB
from Biblio import base_bibli, SimpleBibli, Bibli, Bibli_scrap


def main():
    
    if len(sys.argv) > 1:
        
        fichier_configuration = "bibli.conf.txt"
        profondeur = 1
    
        with open(fichier_configuration, 'r') as config_file:
            config = dict(line.strip().split('=') for line in config_file)
    
        bibli_path = config.get('bibliotheque')
        etats_path = config.get('etats')
        nbmax = int(config.get('nbmax'))

    
        
        if sys.argv[1] == "-c":
            
            if len(sys.argv) == 5:
                fichier_configuration = sys.argv[2]
                profondeur = sys.argv[4]
            
            
                with open(fichier_configuration, 'r') as config_file:
                    config = dict(line.strip().split('=') for line in config_file)
            
                bibli_path = config.get('bibliotheque')
                etats_path = config.get('etats')
                nbmax = int(config.get('nbmax'))
                
                bibli = Bibli_scrap(bibli_path,etats_path)
                bibli.scrap(sys.argv[3],profondeur,nbmax)
        
            
            if len(sys.argv) == 4:
                
                livres = os.listdir(bibli_path)
                bibli = SimpleBibli(etats_path)
                
                for ressource in livres:
                    
                    if ressource.endswith("pdf"):
                        livre = LivrePDF(bibli_path + "/" + ressource )
                        bibli.ajouter(livre)
         
                bibli.rapport_livres("PDF", "rapport_livres")
                bibli.rapport_auteurs("PDF", "rapport_auteurs")
            
        
        
        if sys.argv[1] != "-c":
            
            if sys.argv[1].startswith("https://") or sys.argv[1].startswith("http://"):
                bibli = Bibli_scrap(bibli_path,etats_path)
                profondeur = sys.argv[2]
                bibli.scrap(sys.argv[1],profondeur,nbmax)
                
                
            if sys.argv[1] == "rapports":
                
                livres = os.listdir(bibli_path)
                
                bibli = SimpleBibli(etats_path)
                
                for ressource in livres:
                    
                    if ressource.endswith("pdf"):
                        livre = LivrePDF(bibli_path + "/" + ressource )
                        bibli.ajouter(livre)
                        
                    if ressource.endswith("epub"):
                        livre = LivreEPUB(bibli_path + "/" + ressource )
                        bibli.ajouter(livre)
     
                bibli.rapport_livres("PDF", "rapport_livres")
                bibli.rapport_auteurs("PDF", "rapport_auteurs")


if __name__ == "__main__":
    main()
