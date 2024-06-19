from django.contrib import admin

from sca import models
from sca.models import Alocacacaodisciplinasemdepartamento, Aluno, Curso, \
    Departamento, Disciplina, Historicoescolar, Inscricao, Notafinal, \
    Professor, Turma, Users, Versaocurso

# Register your models here.

admin.site.register(models.Alocacacaodisciplinasemdepartamento)
admin.site.register(models.Aluno)
admin.site.register(models.Curso)
admin.site.register(models.Departamento)
admin.site.register(models.Disciplina)
admin.site.register(models.Historicoescolar)
admin.site.register(models.Inscricao)
admin.site.register(models.Notafinal)
admin.site.register(models.Professor)
admin.site.register(models.Turma)
admin.site.register(models.Users)
admin.site.register(models.Versaocurso)
