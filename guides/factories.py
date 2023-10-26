import factory
import factory.fuzzy

import random

from itertools import combinations

from guides.models import Guide, Participant, Match, Language, Area,\
    GEND_NOPREF, GEND_MALE, GEND_FEMALE, \
    ATTEND_NONE, ATTEND_ONE, ATTEND_TWO, ATTEND_THREE, \
    YEARS_LESSTHANFIVE, YEARS_FIVETOTEN, YEARS_MORETHANTEN, \
    YNM_NO, YNM_YES, HELP_NO, HELP_ONE, HELP_ALWAYS



class ParticipantFactory(factory.DjangoModelFactory):
    class Meta:
        model = Participant

    email = factory.Sequence(lambda n: 'participant{0}@example.com'.format(n))
    given_name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    affiliation = factory.Faker('company')
    country = factory.Faker('country')
    language = factory.SubFactory('guides.factories.LanguageFactory')
    attend = factory.fuzzy.FuzzyChoice([ATTEND_NONE,ATTEND_ONE, ATTEND_TWO, ATTEND_THREE])
    topics = factory.Faker('bs')
    groups = factory.fuzzy.FuzzyChoice(['stir', 'saag', 'iotrg',])
    gender_pref = factory.fuzzy.FuzzyChoice([GEND_NOPREF,GEND_MALE,GEND_FEMALE])
    additional_info = factory.Faker('bs')
    attending = factory.fuzzy.FuzzyChoice([YNM_NO, YNM_YES])

    @factory.post_generation
    def areas(self, create, extracted, **kwargs):
        if create:
            if extracted:
                for area in extracted:
                    self.areas.add(area)
            else:
                l = list(combinations(Area.objects.all(),2))
                choice = l[random.randint(0,len(l)-1)]
                for area in choice:
                    self.areas.add(area) 


class GuideFactory(factory.DjangoModelFactory):
    class Meta:
        model = Guide

    email = factory.Sequence(lambda n: 'guide{0}@example.com'.format(n))
    given_name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    affiliation = factory.Faker('company')
    country = factory.Faker('country')
    ietf_years = factory.fuzzy.FuzzyChoice([YEARS_LESSTHANFIVE, YEARS_FIVETOTEN, YEARS_MORETHANTEN])
    groups = factory.fuzzy.FuzzyChoice(['stir', 'saag', 'iotrg',])
    help_frequency = factory.fuzzy.FuzzyChoice([HELP_NO, HELP_ONE, HELP_ALWAYS])
    additional_info = factory.Faker('bs')

    @factory.post_generation
    def language(self, create, extracted, **kwargs):
        if create:
            if extracted:
                for language in extracted:
                    self.language.add(language)
            else:
                l = list(combinations(Language.objects.all(),2))
                choice = l[random.randint(0,len(l)-1)]
                for language in choice:
                    self.language.add(language)

    @factory.post_generation
    def areas(self, create, extracted, **kwargs):
        if create:
            if extracted:
                for area in extracted:
                    self.areas.add(area)
            else:
                l = list(combinations(Area.objects.all(),2))
                choice = l[random.randint(0,len(l)-1)]
                for area in choice:
                    self.areas.add(area)                     


class MatchFactory(factory.DjangoModelFactory):
    class Meta:
        model = Match

    participant = factory.SubFactory('guides.factories.ParticipantFactory')
    guide = factory.SubFactory('guides.factories.GuideFactory')

class LanguageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Language

    language = factory.Faker('word')

class AreaFactory(factory.DjangoModelFactory):
    class Meta:
        model = Area

    area = factory.Faker('word')


    short = factory.LazyFunction(lambda: factory.Faker('word').generate()[:12])
