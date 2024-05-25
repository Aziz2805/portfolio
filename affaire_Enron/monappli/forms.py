from django import forms

class form_requete4(forms.Form):
    date_inf = forms.DateField(label='Date inférieure', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)
    date_sup = forms.DateField(label='Date supérieure', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)
    seuil = forms.IntegerField(label='Seuil minimal')

class form_requete3(forms.Form):
    nom = forms.CharField(label="Nom")
    prenom = forms.CharField(label="Prénom")
    date_heure_inf = forms.DateTimeField(label='Date/heure inférieure', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    date_heure_sup = forms.DateTimeField(label='Date/heure supérieure', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

class form_choix_requete1(forms.Form):
    CHOIX = (
        ('nomprenom', 'Nom et Prénom'),
        ('email', 'Adresse Mail'),
    )
    choix = forms.ChoiceField(choices=CHOIX, widget=forms.RadioSelect)

    
class form_requete1_mail(forms.Form):
    adresse_mail = forms.EmailField(label = 'Adresse mail', required=True)
    
class form_requete1_nomprenom(forms.Form):
    nom = forms.CharField(label="Nom",required=True)
    prenom = forms.CharField(label="Prénom",required=True)


class form_requete5(forms.Form):
    date_inf = forms.DateField(label='Date inférieure', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)
    date_sup = forms.DateField(label='Date supérieure', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)


class form_requete2(forms.Form):
    CHOICES = [
        ('Envoyés', 'Envoyés'),
        ('Reçus', 'Reçus'),
        ('Envoyés et Reçus', 'Envoyés et Reçus'),
    ]

    OPERATORS = [
        ('>', 'Plus que'),
        ('<', 'Moins que'),
    ]

    type_message = forms.ChoiceField(choices=CHOICES, label="Sélectionnez une option")
    signe = forms.ChoiceField(choices=OPERATORS, label="Choisissez un opérateur")
    nb_min = forms.IntegerField(label="Nombre minimal de mails")
    date_inf = forms.DateField(label='Date inférieure', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)
    date_sup = forms.DateField(label='Date supérieure', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)

class form_requete6(forms.Form):

    CHOICES = [
        ('Expediteur', 'Expediteur'),
        ('Destinataire', 'Destinataire'),
        ('Objet', 'Objet'),
        ('Date et heure', 'Date et heure'),
    ]

    mode = forms.ChoiceField(choices=CHOICES, label="Sélectionnez un mode")
    mots = forms.CharField(widget=forms.Textarea, label="Entrez les mots (séparés par des virgules)")