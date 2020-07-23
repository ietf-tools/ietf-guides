# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


ATTEND_NONE = 'None'
ATTEND_ONE = 'One'
ATTEND_TWO = 'Two'
ATTEND_THREE = 'Three'

ATTEND_CHOICES = (
    (ATTEND_NONE,'This is my first IETF meeting'),
    (ATTEND_ONE, 'This is my second IETF meeting'),
    (ATTEND_TWO, 'This is my third IETF meeting'),
    (ATTEND_THREE, 'This is my fourth IETF meeting')
)

GEND_NOPREF = 'NoPref'
GEND_MALE = 'Male'
GEND_FEMALE = 'Female'
GEND_NONBINARY = 'Non-Binary'

GEND_CHOICES = (
    (GEND_NOPREF, "I don't have a preference"),
    (GEND_MALE, "I would prefer to work with a male guide"),
    (GEND_FEMALE, "I would prefer to work with a female guide"),
)

GEND_TYPE_FEMALE = "Female"
GEND_TYPE_MALE = "Male"
GEND_TYPE_NONBINARY = "Non-Binary"

GEND_TYPES = (
    (GEND_TYPE_FEMALE, "Female"),
    (GEND_TYPE_MALE, "Male"),
    (GEND_TYPE_NONBINARY, "Non Binary"),
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

YN_CHOICES = (
    (YNM_YES, "Yes"),
    (YNM_NO, "No"),
)

AREA_ART = "ART"
AREA_INT = "INT"
AREA_OPS = "OPS"
AREA_RTG = "RTG"
AREA_SEC = "SEC"
AREA_TSG = "TSG"
AREA_UNKNOWN = "UNKNOWN"

IETF_AREAS = (
    (AREA_ART, "Applications and Real-Time"),
    (AREA_INT, "Internet"),
    (AREA_OPS, "Operations and Management"),
    (AREA_RTG, "Routing"),
    (AREA_SEC, "Security"),
    (AREA_TSG, "Transport"),
    (AREA_UNKNOWN, "I don't know yet")
)

class Area(models.Model):
    area = models.CharField(max_length=64)
    short = models.CharField(max_length=12,default="")

    def __str__(self):
        return self.area

class Language(models.Model):
    language = models.CharField(max_length=32)

    def __str__(self):
        return self.language

class Participant(models.Model):
    email = models.EmailField(primary_key=True)
    given_name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    affiliation = models.CharField(max_length=64)
    country = models.CharField('Country of residence',max_length=64)
    language = models.ForeignKey(Language,verbose_name='Preferred conversational language',max_length=32,default=1)
    attend = models.CharField('Number of IETFs attended',max_length=32, choices=ATTEND_CHOICES, default=ATTEND_NONE)
    topics = models.TextField('What technical topics brought you to the IETF?')
    areas = models.ManyToManyField(Area, verbose_name='What IETF area(s) most interest you?', help_text = 'Further information about IETF areas is available <a href="https://www.ietf.org/topics/areas/">here</a>.' )
    groups = models.CharField('Which working groups are you most interested in?',help_text='see <a href="https://www.ietf.org/how/wgs">https://www.ietf.org/how/wgs</a>',max_length=256)
    gender_pref = models.CharField('Guide gender preference', max_length=32, choices=GEND_CHOICES, default=GEND_NOPREF)
    remote = models.CharField('Will you be attending remotely?', max_length=32, choices=YN_CHOICES, default=YNM_NO)
    additional_info = models.TextField('Is there anything else you would like to share with us?', blank=True)

    def __str__(self):
        return "%s %s <%s>" % (self.given_name, self.surname, self.email)

    def pretty_attend(self):
        attendmap = {
            ATTEND_NONE: "0",
            ATTEND_ONE: "1",
            ATTEND_TWO: "2",
            ATTEND_THREE: "3",
        }
        return attendmap[self.attend]

class Guide(models.Model):
    email = models.EmailField(primary_key=True)
    given_name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    affiliation = models.CharField(max_length=64)
    country = models.CharField('Country of residence',max_length=64)
    gender = models.CharField("Gender", max_length=32, default="", blank=True)
    language = models.ManyToManyField(Language,verbose_name='What languages can you communicate in fluently?')
    ietf_years = models.CharField('How long have you been participating in the IETF?', max_length=32, choices=YEARS_CHOICES, default = YEARS_LESSTHANFIVE)
    multiple_guided = models.CharField('Are you willing to work with more than one program participant?', max_length=32, choices=YNM_CHOICES, default=YNM_YES)
    give_intro = models.CharField('Are you willing to give a general introduction of the IETF to a newcomer program participant?', max_length=32, choices=YNM_CHOICES, default=YNM_YES, help_text="<em>(Sometimes it is not possible to exactly match guides with participants and their preferred technical areas)</em>")
    areas = models.ManyToManyField(Area, verbose_name='What IETF area(s) are you involved in?')
    groups = models.CharField('Which working groups are you most able to help people with?', max_length=256, default="", blank=True)
    arrival_date = models.CharField('What date are you arriving at the next IETF meeting (YYYY/MM/DD)?', max_length=64)
    accept_remote = models.CharField('Are you willing to guide remote participants?',max_length=32, choices=YNM_CHOICES, default=YNM_YES)
    additional_info = models.TextField('Is there anything else we should know?',
                                       blank=True)
    keep_for_nexttime = models.BooleanField("Should we keep your registration data around for future participation in the guides program?", default=False)

    def __str__(self):
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

    def __str__(self):
        return "%s is guiding %s (made by %s on %s)" % (self.guide, self.participant, self.by.email, self.date)
