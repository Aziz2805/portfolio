from django.db import models

# Create your models here.

class Personne(models.Model):
    
    #employe_id = models.IntegerField(unique=True)
    nom =  models.CharField(max_length=30)
    prenom =  models.CharField(max_length=50)
    categorie =  models.CharField(max_length=30)
    boite_mail = models.CharField(max_length=50)
  
    
class Email(models.Model):
    
    #email_id = models.IntegerField(unique=True)
    adresse_mail = models.EmailField()
    est_interne = models.CharField(max_length=1)
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    
class Message(models.Model):
    
    #message_id = models.IntegerField(unique=True)
    date_heure = models.DateTimeField()
    objet = models.TextField(null=True)
    contenu = models.TextField(null=True)
    expediteur = models.OneToOneField(Email,on_delete = models.CASCADE)
    
class Destinataire(models.Model):
    #destinataire_id = models.IntegerField(unique=True)
    emails = models.OneToOneField(Email,on_delete=models.CASCADE)
    messages = models.ForeignKey(Message,on_delete= models.CASCADE)
    
    
    
    