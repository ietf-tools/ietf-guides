import factory
import factory.fuzzy

import random

from itertools import combinations

from guides.models import Guide, Participant, Match, Language, \
    GEND_NOPREF, GEND_MALE, GEND_FEMALE, \
    ATTEND_NONE, ATTEND_ONE, ATTEND_FEW, \
    YEARS_LESSTHANFIVE, YEARS_FIVETOTEN, YEARS_MORETHANTEN



class ParticipantFactory(factory.DjangoModelFactory):
    class Meta:
        model = Participant

    email = factory.Sequence(lambda n: 'guide{0}@example.com'.format(n))
    given_name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    affiliation = factory.Faker('company')
    country = factory.Faker('country')
    language = factory.fuzzy.FuzzyChoice(Language.objects.all())
    attend = factory.fuzzy.FuzzyChoice([ATTEND_NONE,ATTEND_ONE, ATTEND_FEW])
    topics = factory.Faker('bs')
    areas = factory.fuzzy.FuzzyChoice(["ART", "INT", "OPS", "RTG", "SEC", "TSG", "I don't know yet"])
    groups = factory.fuzzy.FuzzyChoice(['stir', 'saag', 'iotrg',])
    gender_pref = factory.fuzzy.FuzzyChoice([GEND_NOPREF,GEND_MALE,GEND_FEMALE])
    additional_info = factory.Faker('bs')


class GuideFactory(factory.DjangoModelFactory):
    class Meta:
        model = Guide

    email = factory.Sequence(lambda n: 'guide{0}@example.com'.format(n))
    given_name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    affiliation = factory.Faker('company')
    country = factory.Faker('country')
    ietf_years = factory.fuzzy.FuzzyChoice([YEARS_LESSTHANFIVE, YEARS_FIVETOTEN, YEARS_MORETHANTEN])
    arrival_date = factory.Faker('date')
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


class MatchFactory(factory.DjangoModelFactory):
    class Meta:
        model = Match

    participant = factory.SubFactory('guides.factories.ParticipantFactory')
    guide = factory.SubFactory('guides.factories.GuideFactory')

class LanguageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Language

    language = factory.Faker('word')

