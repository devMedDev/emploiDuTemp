from django.shortcuts import render
from .genetic_algorithm import genetic_algorithm
from .models import Enseignant, Classe
from django.shortcuts import render, get_object_or_404
from .models import Enseignant, Classe, Creneau

def list_enseignants(request):
    enseignants = Enseignant.objects.all()
    return render(request, 'emploi/enseignants_list.html', {'enseignants': enseignants})

def enseignant_timetable(request, enseignant_id):
    enseignant = Enseignant.objects.get(id=enseignant_id)
    
    # Liste des jours et horaires
    jours = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']
    horaires = [
        {'index': 0, 'horaire': '08:00'},
        {'index': 1, 'horaire': '09:00'},
        {'index': 2, 'horaire': '10:00'},
        {'index': 3, 'horaire': '11:00'},
        {'index': 4, 'horaire': '12:00'},
        {'index': 5, 'horaire': '13:00'},
        {'index': 6, 'horaire': '14:00'},
        {'index': 7, 'horaire': '15:00'},
    ]

    # Préparer l'emploi du temps sous forme de liste de créneaux
    emploi_du_temps = genetic_algorithm()  # Ceci doit être une liste de dictionnaires

    # Structure pour organiser les créneaux par jour et par horaire
    emploi_structure = {jour: {horaire['horaire']: None for horaire in horaires} for jour in jours}

    # Remplir l'emploi du temps structuré avec les créneaux
    for creneau in emploi_du_temps:
        jour = creneau.get('jour')  # Obtenez le jour
        horaire = creneau.get('horaire_debut').strftime("%H:%M")  # Format de l'horaire en chaîne
        if jour in emploi_structure and horaire in emploi_structure[jour]:
            emploi_structure[jour][horaire] = creneau  # Ajoutez le créneau

    context = {
        'enseignant': enseignant,
        'emploi_du_temps': emploi_structure,
        'jours': jours,
        'horaires': horaires,
    }
    return render(request, 'emploi/enseignant_timetable.html', context)

def list_classes(request):
    classes = Classe.objects.all()
    return render(request, 'emploi/classes_list.html', {'classes': classes})

def classe_timetable(request, classe_id):
    classe = Classe.objects.get(id=classe_id)
    emploi_du_temps = genetic_algorithm()
    return render(request, 'emploi/classe_emploi.html', {'emploi_du_temps': emploi_du_temps, 'classe': classe})
