
    
from django.db import models

class Acteur(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    email = models.EmailField()
    mission=models.CharField(max_length=200)
    def __str__(self):
       return (self.nom)+"  "+(self.prenom)

class PV(models.Model):
    titre = models.CharField(max_length=200)
    date = models.DateTimeField('date du PV')
    ordreDuJour = models.TextField('Ordre du jour')
    pointAborde = models.TextField('Points abordées',null=True, blank=True)
    contenu = models.TextField(null=True, blank=True)
    Decisions = models.TextField('Décisions finales',null=True, blank=True)
    presents= models.ManyToManyField(Acteur)

    class Meta:
        verbose_name='PV'
        verbose_name_plural='PVs'
    def __str__(self):
        return self.titre+'/ Ordre du jour: '+self.ordreDuJour