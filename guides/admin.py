# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Guide, Participant, Language, Match

# Register your models here.

class GuideAdmin(admin.ModelAdmin):
    model = Guide

class ParticipantAdmin(admin.ModelAdmin):
    model = Participant

class LanguageAdmin(admin.ModelAdmin):
    model = Language

class MatchAdmin(admin.ModelAdmin):
    model = Match

admin.site.register(Guide, GuideAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Match, MatchAdmin)
