from django.db import models

class Niveau(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.nom

class Matiere(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)  # 'scientifique' ou 'littéraire'

    def __str__(self):
        return self.nom

class Classe(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    nombre_etudiants = models.IntegerField()

    def __str__(self):
        return self.nom

class Enseignant(models.Model):
    nom = models.CharField(max_length=100)
    nombre_heures_par_semaine = models.IntegerField()
    jour_de_repos = models.CharField(max_length=50)  # 'dimanche', 'lundi', etc.
    matieres = models.ManyToManyField(Matiere)
    preferences = models.JSONField()  # { 'creux': False, 'debut_8h': True }

    def __str__(self):
        return self.nom

class Creneau(models.Model):
    jour = models.CharField(max_length=50)  # 'dimanche', 'lundi', etc.
    horaire_debut = models.TimeField()
    horaire_fin = models.TimeField()
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.jour} | {self.horaire_debut} - {self.horaire_fin} | {self.enseignant.nom}'
