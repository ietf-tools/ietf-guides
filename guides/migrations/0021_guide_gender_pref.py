# Generated by Django 5.1.2 on 2024-10-14 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guides", "0020_guide_admin_notes_participant_admin_notes"),
    ]

    operations = [
        migrations.AddField(
            model_name="guide",
            name="gender_pref",
            field=models.CharField(
                choices=[
                    ("NoPref", "I don't have a preference"),
                    ("Male", "I would prefer to work with a male participant"),
                    ("Female", "I would prefer to work with a female participant"),
                    (
                        "Non-Binary",
                        "I would prefer to work with a non-binary participant",
                    ),
                ],
                default="NoPref",
                max_length=32,
                verbose_name="Participant gender preference",
            ),
        ),
    ]
