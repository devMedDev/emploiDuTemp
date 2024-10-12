import random
from datetime import time, timedelta,datetime
from emploi.models import Enseignant, Classe, Creneau, Matiere

def generate_random_solution():
    jours = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi']
    horaires = [time(h, 0) for h in range(8, 17)]  # Créneaux horaires de 8h à 16h (1h chacun)
    enseignants = Enseignant.objects.all()
    classes = Classe.objects.all()

    solution = []

    for enseignant in enseignants:
        for jour in jours:
            if jour == enseignant.jour_de_repos:
                continue  # Pas de cours le jour de repos

            for horaire in horaires:
                classe = random.choice(classes)
                matiere = random.choice(list(enseignant.matieres.all()))
                solution.append({
                    'enseignant': enseignant,
                    'jour': jour,
                    'horaire_debut': horaire,
                    'classe': classe,
                    'matiere': matiere,
                })
    
    return solution

def evaluate_fitness(solution):
    score = 0
    for creneau in solution:
        # Respect des préférences d'enseignant (par exemple, éviter les creux)
        enseignant = creneau['enseignant']
        if enseignant.preferences.get("creux", False):
            # Pénalité si un enseignant a des créneaux non consécutifs
            previous_hour = (datetime.combine(datetime.today(), creneau['horaire_debut']) - timedelta(hours=1)).time()
            if not any(sol['horaire_debut'] == previous_hour for sol in solution if sol['enseignant'] == enseignant):
                score -= 1

        # Respect des types de matières (par exemple, matières scientifiques le matin)
        if creneau['matiere'].type == 'scientifique' and creneau['horaire_debut'].hour > 12:
            score -= 1  # Pénalité si une matière scientifique est assignée l'après-midi

    return score

def mutate(solution):
    # Mutation d'un créneau aléatoire
    random_creneau = random.choice(solution)
    random_creneau['classe'] = Classe.objects.order_by('?').first()
    random_creneau['matiere'] = Matiere.objects.order_by('?').first()
    return solution

def crossover(solution1, solution2):
    # Croisement entre deux solutions
    new_solution = []
    for creneau1, creneau2 in zip(solution1, solution2):
        new_solution.append(creneau1 if random.random() > 0.5 else creneau2)
    return new_solution

def genetic_algorithm():
    population_size = 10
    generations = 100
    mutation_rate = 0.1

    # Initialisation de la population
    population = [generate_random_solution() for _ in range(population_size)]

    for generation in range(generations):
        # Évaluation de la population
        population = sorted(population, key=lambda sol: evaluate_fitness(sol), reverse=True)
        
        # Sélection des meilleures solutions
        top_population = population[:population_size // 2]
        
        # Génération d'enfants
        offspring = [crossover(random.choice(top_population), random.choice(top_population)) for _ in range(population_size // 2)]
        
        # Application des mutations
        for individual in offspring:
            if random.random() < mutation_rate:
                mutate(individual)
        
        # Mise à jour de la population
        population = top_population + offspring

    best_solution = max(population, key=lambda sol: evaluate_fitness(sol))
    return best_solution
