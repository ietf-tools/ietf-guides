# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


ATTEND_NONE = 'None'
ATTEND_ONE = 'One'
ATTEND_FEW = 'Few'

ATTEND_CHOICES = (
    (ATTEND_NONE,'This is my first IETF meeting'),
    (ATTEND_ONE, 'This is my second IETF meeting'),
    (ATTEND_FEW, 'I have been to two, three, or four IETF meetings')
)

GEND_NOPREF = 'NoPref'
GEND_MALE = 'Male'
GEND_FEMALE = 'Female'

GEND_CHOICES = (
    (GEND_NOPREF, "I don't have a preference"),
    (GEND_MALE, "I would prefer to work with a male guide"),
    (GEND_FEMALE, "I would prefer to work with a female guide"),
)

YEARS_LESSTHANFIVE = "LESSTHANFIVE"
YEARS_FIVETOTEN = "FIVETOTEN"
YEARS_MORETHANTEN = "MORETHANTEN"

YEARS_CHOICES = (
    (YEARS_LESSTHANFIVE,"Less than 5 years"),
    (YEARS_FIVETOTEN,"5 to 10 years"),
    (YEARS_MORETHANTEN, "More than 10 years"),
)

YNM_YES = "YES"
YNM_NO = "NO"
YNM_MAYBE = "MAYBE"

YNM_CHOICES = (
    (YNM_YES, "Yes"),
    (YNM_NO, "No"),
    (YNM_MAYBE, "Maybe"),
)

class Language(models.Model):
    language = models.CharField(max_length=32)

    def __unicode__(self):
        return self.language


class Participant(models.Model):
    email = models.EmailField(primary_key=True)
    given_name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    affiliation = models.CharField(max_length=64)
    country = models.CharField('Country of residence',max_length=64)
    language = models.ForeignKey(Language,verbose_name='Preferred conversational language',max_length=32,default=1)
    attend = models.CharField('IETF attendance',max_length=32, choices=ATTEND_CHOICES, default=ATTEND_NONE)
    topics = models.TextField('What technical topics brought you to the IETF?')
    areas = models.CharField('What IETF area(s) most interest you',help_text="ART, INT, OPS, RTG, SEC, TSG, I don't know yet",max_length=64)
    groups = models.CharField('Which working groups are you most interested in?',help_text='see https://wwww.ietf.org/how/wgs',max_length=256)
    gender_pref = models.CharField('Guide gender preference', max_length=32, choices=GEND_CHOICES, default=GEND_NOPREF)
    additional_info = models.TextField('Is there anything else you would like to share with us?')

    def __unicode__(self):
        return "%s %s <%s>" % (self.given_name, self.surname, self.email)

    def pretty_attend(self):
        attendmap = {
            ATTEND_NONE: "0",
            ATTEND_ONE: "1",
            ATTEND_FEW: "2 to 4"
        }
        return attendmap[self.attend]

class Guide(models.Model):
    email = models.EmailField(primary_key=True)
    given_name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    affiliation = models.CharField(max_length=64)
    country = models.CharField('Country of residence',max_length=64)
    language = models.ManyToManyField(Language,verbose_name='What languages can you communicate in fluently?', max_length=32)
    ietf_years = models.CharField('How long have you been participating in the IETF?', max_length=32, choices=YEARS_CHOICES, default = YEARS_LESSTHANFIVE)
    multiple_guided = models.CharField('Are you willing to work with more than one program participant?', max_length=32, choices=YNM_CHOICES, default=YNM_YES)
    give_intro = models.CharField('Are you willing to give a general introduction of the IETF to a newcomer program participant?', max_length=32, choices=YNM_CHOICES, default=YNM_YES)
    arrival_date = models.DateField('What date are you arriving at then next IETF meeting?')
    additional_info = models.TextField('Is there anything else we should know?')

    def __unicode__(self):
        return "%s %s <%s>" % (self.given_name, self.surname, self.email)

    def pretty_ietf_years(self):
        yearmap = {
            YEARS_LESSTHANFIVE : "<5",
            YEARS_FIVETOTEN : "5-10",
            YEARS_MORETHANTEN: ">10"
        }
        return yearmap[self.ietf_years]


class Match(models.Model):
    participant = models.ForeignKey(Participant)
    guide = models.ForeignKey(Guide)
    by = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s is guiding %s (made by %s on %s)" % (self.guide, self.participant, self.by.email, self.date)
