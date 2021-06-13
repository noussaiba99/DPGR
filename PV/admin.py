import io
from pathlib import Path
from typing import List
from django import forms
from django.contrib import admin
from django.http.response import FileResponse
from django.urls.resolvers import URLPattern
from django.views.generic.base import RedirectView
from reportlab.pdfgen import canvas
from .models import PV, Acteur
from django.contrib.auth.models import Group

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, path, include
from django.utils.http import urlencode

from django_object_actions import DjangoObjectActions

from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)
admin.site.unregister(Group)


@admin.register(Acteur)
class ActeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email')
    search_fields = ('nom', 'prenom', 'email')


@admin.register(PV)
class PVAdmin(admin.ModelAdmin):

    def view_presents_link(self, obj):
        from django.utils.html import format_html

        count = obj.presents.count()
        url = (
                reverse("admin:PV_acteur_changelist")
                + "?"
                + urlencode({"presents__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} présents</a>', url, count)

    view_presents_link.short_description = "Présents"

    # fields=('','')
    list_display = ('titre', 'ordreDuJour', 'date', 'view_presents_link')
    list_filter = ('date', 'presents')
    search_fields = ('titre', 'ordreDuJour')
    # list_display_links=('ordreDuJour',)
    # list_editable=('titre',)
    # change_list_template='admin/pv/pv_change_list.html'
    change_form_template = 'admin/pv/pv_change_form.html'

    def newC(self, obj):
        return "{} - {}".format(obj.titre, obj.ordreDuJour)


admin.site.site_header = "Génération des PVs"
admin.site.site_title = "Outil de génération des PVs"
