from django.contrib import admin

from cadd import models
from sca.models import Aluno, Professor, Curso, Departamento, Disciplina, Turma

# Register your models here.

class ComissaoAdmin(admin.ModelAdmin):
    """
    Classe para CRUD da tabela comissao
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Comissao.curso":
            kwargs["queryset"] = Curso.objects.using('sca').all()
        return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)


class MembroAdmin(admin.ModelAdmin):
    """
    Classe para CRUD da tabela membro
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Membro.professor":
            kwargs["queryset"] = Professor.objects.using('sca').all()
            return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)


class DocumentoAdmin(admin.ModelAdmin):
    """
    Classe para CRUD da tabela documento
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Documento.aluno":
            kwargs["queryset"] = Aluno.objects.using('sca').all()
            return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)


class HorarioAdmin(admin.ModelAdmin):
    """
    Classe para CRUD da tabela horario
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Horario.curso":
            kwargs["queryset"] = Curso.objects.using('sca').all()
            return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)


class ItemHorarioAdmin(admin.ModelAdmin):
    """
    Classe para CRUD da tabela item_horario
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ItemHorario.departamento":
            kwargs["queryset"] = Departamento.objects.using('sca').all()
            return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)

        if db_field.name == "ItemHorario.disciplina":
            kwargs["queryset"] = Disciplina.objects.using('sca').all()
            return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)

        if db_field.name == "ItemHorario.professor":
            kwargs["queryset"] = Professor.objects.using('sca').all()
            return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)

        if db_field.name == "ItemHorario.turma":
            kwargs["queryset"] = Turma.objects.using('sca').all()
            return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)


class PlanoAdmin(admin.ModelAdmin):
    """
    Classe para CRUD da tabela plano
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Plano.aluno":
            kwargs["queryset"] = Aluno.objects.using('sca').all()
            return super().formfield_for_foreignkey(db_field, request, using='sca', **kwargs)


admin.site.register(models.Comissao, ComissaoAdmin)
admin.site.register(models.Membro, MembroAdmin)
admin.site.register(models.Reuniao)
admin.site.register(models.Documento, DocumentoAdmin)
admin.site.register(models.Horario, HorarioAdmin)
admin.site.register(models.ItemHorario, ItemHorarioAdmin)
admin.site.register(models.Plano, PlanoAdmin)
admin.site.register(models.PlanoFuturo)

admin.site.empty_value_display = '(None)'
