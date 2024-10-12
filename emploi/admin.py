# emploi/admin.py

from django.contrib import admin
from .models import Niveau, Classe, Matiere, Enseignant, Creneau

admin.site.register(Niveau)
admin.site.register(Classe)
admin.site.register(Matiere)
admin.site.register(Enseignant)
admin.site.register(Creneau)
