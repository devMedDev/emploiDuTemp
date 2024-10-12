import random
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import time
from emploi.models import Niveau, Matiere, Classe, Enseignant, Creneau

class Command(BaseCommand):
    help = "Populates the database with test data for niveaux, matieres, classes, enseignants, and creneaux."

    def handle(self, *args, **kwargs):
        # Clear existing data
        Creneau.objects.all().delete()
        Enseignant.objects.all().delete()
        Classe.objects.all().delete()
        Matiere.objects.all().delete()
        Niveau.objects.all().delete()

        # Create Niveaux
        niveaux = [
            Niveau.objects.create(nom='4ème année moyenne', description='Classe moyenne 4ème année'),
            Niveau.objects.create(nom='5ème année moyenne', description='Classe moyenne 5ème année'),
        ]

        # Create Matieres
        matieres = []
        for niveau in niveaux:
            matieres.extend([
                Matiere.objects.create(nom='Mathématiques', niveau=niveau, type='scientifique'),
                Matiere.objects.create(nom='Physique', niveau=niveau, type='scientifique'),
                Matiere.objects.create(nom='Français', niveau=niveau, type='littéraire'),
                Matiere.objects.create(nom='Histoire', niveau=niveau, type='littéraire'),
            ])

        # Create Classes
        classes = [
            Classe.objects.create(nom='4ème A', niveau=niveaux[0], nombre_etudiants=random.randint(25, 35)),
            Classe.objects.create(nom='4ème B', niveau=niveaux[0], nombre_etudiants=random.randint(25, 35)),
            Classe.objects.create(nom='5ème A', niveau=niveaux[1], nombre_etudiants=random.randint(25, 35)),
            Classe.objects.create(nom='5ème B', niveau=niveaux[1], nombre_etudiants=random.randint(25, 35)),
        ]

        # Create Enseignants
        enseignants = [
            Enseignant.objects.create(nom='Mr. Dupont', nombre_heures_par_semaine=18, jour_de_repos='lundi', preferences={'creux': False, 'debut_8h': True}),
            Enseignant.objects.create(nom='Mme. Martin', nombre_heures_par_semaine=16, jour_de_repos='dimanche', preferences={'creux': True, 'debut_8h': False}),
            Enseignant.objects.create(nom='Mr. Durand', nombre_heures_par_semaine=20, jour_de_repos='mardi', preferences={'creux': False, 'debut_8h': True}),
            Enseignant.objects.create(nom='Mme. Moreau', nombre_heures_par_semaine=15, jour_de_repos='jeudi', preferences={'creux': True, 'debut_8h': False}),
        ]

        # Assign Matieres to Enseignants
        enseignants[0].matieres.add(matieres[0], matieres[2])  # Mr. Dupont teaches Math and French
        enseignants[1].matieres.add(matieres[1], matieres[3])  # Mme. Martin teaches Physics and History
        enseignants[2].matieres.add(matieres[0], matieres[1])  # Mr. Durand teaches Math and Physics
        enseignants[3].matieres.add(matieres[2], matieres[3])  # Mme. Moreau teaches French and History

        # Create Creneaux
        creneaux = []
        heures = [(8, 0), (9, 0), (10, 0), (11, 0), (13, 0), (14, 0), (15, 0)]
        jours = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']
        
        for jour in jours:
            for classe in classes:
                for heure_debut, heure_fin in zip(heures, heures[1:]):  # Successive sessions of 1 hour
                    enseignant = random.choice(enseignants)
                    matiere = random.choice(list(enseignant.matieres.all()))
                    creneaux.append(
                        Creneau.objects.create(
                            jour=jour,
                            horaire_debut=time(heure_debut[0], heure_debut[1]),
                            horaire_fin=time(heure_fin[0], heure_fin[1]),
                            enseignant=enseignant,
                            classe=classe,
                            matiere=matiere
                        )
                    )

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
