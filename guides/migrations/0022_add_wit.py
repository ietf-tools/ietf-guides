# Copyright The IETF Trust 2024, All Rights Reserved

from django.db import migrations

def forward(apps, schema_editor):
    Area = apps.get_model("guides","Area")
    Participant = apps.get_model("guides","Participant")
    Guide = apps.get_model("guides","Guide")
    wit = Area.objects.create(area="WIT: Web and Intenet Transport", short="wit")
    for p in Participant.objects.all():
        if p.areas.filter(short="tsv").exists():
            p.areas.add(wit)
    for g in Guide.objects.all():
        if g.areas.filter(short="tsv").exists():
            g.areas.add(wit)    

def reverse(apps, schema_editor):
    Area = apps.get_model("guides","Area")
    Participant = apps.get_model("guides","Participant")
    Guide = apps.get_model("guides","Guide")
    for g in Guide.objects.all():
        g.areas.filter(short="wit").delete()
    for p in Participant.objects.all():
        p.areas.filter(short="wit").delete()
    Area.objects.filter(short="wit").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0021_guide_gender_pref'),
    ]

    operations = [
            migrations.RunPython(forward,reverse),
    ]