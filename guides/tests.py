# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyquery import PyQuery

from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User

from .utils import encode_email
from .models import Guide, Participant, Match, Language, YEARS_MORETHANTEN, YNM_YES, ATTEND_TWO, ATTEND_THREE, GEND_NOPREF
from .factories import GuideFactory, ParticipantFactory, MatchFactory, LanguageFactory, AreaFactory

class GuidesTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email='tester@example.com')
        LanguageFactory.create_batch(10)
        AreaFactory.create_batch(8)

    def test_index(self):
        url = reverse('guides.views.index', kwargs=dict())
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

        logged_in = self.client.login(username='testuser',password='password')
        self.assertTrue(logged_in)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 302)
        r = self.client.get(r.url)
        self.assertEqual(r.status_code, 200)


    def test_become_guide(self):
        url = reverse('guides.views.become_guide', kwargs=dict())
        r = self.client.get(url)
        self.assertEqual(r.status_code,200)
        r = self.client.post(url,dict(email='bad@address'))
        self.assertEqual(r.status_code,200)
        q = PyQuery(r.content)
        self.assertTrue(q('form>.has-error'))
        r = self.client.post(url,dict(email='good@example.com'))
        self.assertEqual(r.status_code,200)
        q = PyQuery(r.content)
        self.assertFalse(q('form>.has-error'))
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[-1].to,['good@example.com'])
        hash = encode_email('good@example.com','guide')
        self.assertIn(hash, mail.outbox[-1].body)

    def test_request_guide(self):
        url = reverse('guides.views.request_guide', kwargs=dict())
        r = self.client.get(url)
        self.assertEqual(r.status_code,200)
        r = self.client.post(url,dict(email='bad@address'))
        self.assertEqual(r.status_code,200)
        q = PyQuery(r.content)
        self.assertTrue(q('form>.has-error'))
        r = self.client.post(url,dict(email='good@example.com'))
        self.assertEqual(r.status_code,200)
        q = PyQuery(r.content)
        self.assertFalse(q('form>.has-error'))
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[-1].to,['good@example.com'])
        hash = encode_email('good@example.com','participant')
        self.assertIn(hash, mail.outbox[-1].body)

    def test_edit_info(self):
        url = reverse('guides.views.edit_info', kwargs=dict(hash='abIEBSDHeb235Heb3sii8EEsgarbage'))
        r = self.client.get(url)
        self.assertEqual(r.status_code,404)

        hash = encode_email('test@example.com','guide')
        url = reverse('guides.views.edit_info', kwargs=dict(hash=hash))
        r = self.client.get(url)
        self.assertEqual(r.status_code,200)
        r = self.client.post(url, 
            dict(
                given_name="Random",
                surname="Guide",
                affiliation="LackOf",
                country="Old",
                language="1",
                ietf_years=YEARS_MORETHANTEN,
                multiple_guided=YNM_YES,
                give_intro=YNM_YES,
                areas=[2,5],
                groups='blarg, burgle, baz',
                arrival_date="2019-03-15",
                accept_remote="NO",
                additional_info="Nope.",               
            )
        )
        self.assertEqual(r.status_code,200)
        q = PyQuery(r.content)
        self.assertFalse(q('form>.has-error')) 
        self.assertEqual(Guide.objects.count(),1)

        hash = encode_email('test@example.com','participant')
        url = reverse('guides.views.edit_info', kwargs=dict(hash=hash))
        r = self.client.get(url)
        self.assertEqual(r.status_code,200)
        r = self.client.post(url, 
            dict(
                attending="YES",
                given_name="Random",
                surname="Participant",
                affiliation="DoNotHave",
                country="Old",
                language="1",
                attend=ATTEND_TWO,
                topics="sandwiches",
                areas=[1,3],
                groups='anything+contining+"bis"',
                gender_pref=GEND_NOPREF,
                remote="YES",
                additional_info="peace",
            )
        )
        self.assertEqual(r.status_code,200)
        q = PyQuery(r.content)
        self.assertFalse(q('form>.has-error')) 
        self.assertEqual(Participant.objects.count(),1)

    def test_make_match(self):
        guide = GuideFactory()
        participant=ParticipantFactory()
        url = reverse('guides.views.make_match')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.url.startswith(reverse('login')))
        self.client.login(username='testuser', password='password')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

        r = self.client.post(url,dict(participant=participant.pk, guide=guide.pk ))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Match.objects.exists())
        match = Match.objects.first()
        self.assertEqual(r.url, reverse('guides.views.send_match_email',kwargs=dict(match_id=match.pk)))

    def test_match_email(self):
        match = MatchFactory(by=self.user)
        url = reverse('guides.views.send_match_email', kwargs=dict(match_id=match.pk))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.url.startswith(reverse('login')))
        self.client.login(username='testuser', password='password')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        r = self.client.post(url,dict(send="send", message="Override all the messages"))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].body,"Override all the messages")

    def test_cancel_match(self):
        match = MatchFactory(by=self.user)
        url = reverse('guides.views.send_match_email', kwargs=dict(match_id=match.pk))
        self.client.login(username='testuser', password='password')
        r = self.client.post(url,dict(cancel="cancel", message="Override all the messages"))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(len(mail.outbox),0)
        self.assertFalse(Match.objects.filter(pk=match.pk).exists())
