# Generated by Django 2.2.28 on 2023-10-11 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0016_participant_attending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='arrival_date',
        ),
        migrations.AddField(
            model_name='guide',
            name='help_frequency',
            field=models.CharField(choices=[('ZERO', 'Not at this time'), ('ONE', 'This IETF (only)'), ('ALWAYS', 'At every IETF I attend')], default='ZERO', max_length=32, verbose_name='How frequently are you willing to be a guide?'),
        ),
    ]