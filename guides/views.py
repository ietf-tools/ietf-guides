# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import Guide, Participant, Match, RegistrationState
from .models import REGISTRATION_OPEN, REGISTRATION_FULL, REGISTRATION_CLOSED
from .utils import encode_email, decode_hash
from .forms import EmailForm, GuideForm, ParticipantForm, MatchForm, MatchEmailForm


def set_registration(to_what):
    if RegistrationState.objects.count() == 0:
        registration_state = RegistrationState()
        registration_state.save()

    inst = RegistrationState.objects.first()
    inst.system_state = to_what
    inst.save()
    return inst.system_state


def get_registration_state():
    if RegistrationState.objects.count() == 0:
        return set_registration(REGISTRATION_OPEN)
    return RegistrationState.objects.first().system_state


def index(request):
    registration_state = get_registration_state()

    if request.user.is_authenticated:
        return redirect('guides.views.matcher_index')
    elif registration_state == REGISTRATION_OPEN:
        return render(request, 'guides/index.html', {})
    elif registration_state == REGISTRATION_FULL:
        return render(request, 'guides/registration_full.html', {})
    else:  # default closed
        return render(request, 'guides/registration_closed.html', {})


@login_required
def close_registration(request):
    set_registration(REGISTRATION_CLOSED)
    return redirect('guides.views.index')


@login_required
def open_registration(request):
    set_registration(REGISTRATION_OPEN)
    return redirect('guides.views.index')


@login_required
def full_registration(request):
    set_registration(REGISTRATION_FULL)
    return redirect('guides.views.index')


@login_required
def matcher_index(request):
    stats = dict()
    stats['participants'] = Participant.objects.count()
    stats['guides'] = Guide.objects.count()
    stats['matches'] = Match.objects.count()
    stats['unmatched'] = Participant.objects.exclude(match__isnull=False).count()
    stats['guides_unused'] = Guide.objects.exclude(match__isnull=False).count()
    stats['guides_matched_but_willing'] = Guide.objects.filter(match__isnull=False,multiple_guided=True).count()
    return render(request, 'guides/matcher_index.html',dict(stats=stats))

def become_guide(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            hash = encode_email(email,'guide')
            url = request.build_absolute_uri(reverse('guides.views.edit_info',kwargs=dict(hash=hash)))
            message = render_to_string('guides/guide_nextsteps.txt', dict(url=url))
            send_mail(subject='Guide volunteer next steps', message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email,])
            return render(request, 'guides/thanks_becoming.html',dict(email=email))
    else:
        form = EmailForm()
    context = dict(form=form,)
    return render(request, 'guides/become_a_guide.html', context)


def request_guide(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            hash = encode_email(email,'participant')
            url = request.build_absolute_uri(reverse('guides.views.edit_info',kwargs=dict(hash=hash)))
            message = render_to_string('guides/participant_nextsteps.txt', dict(url=url))
            send_mail(subject='IETF Guide Program next steps', message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email,])
            return render(request, 'guides/thanks_becoming.html',dict(email=email))
    else:
        form = EmailForm()
    context = dict(form=form,)
    return render(request, 'guides/request_a_guide.html', context)


def edit_info(request, hash):
    decode = decode_hash(hash)
    if not decode:
        raise Http404 
    (request_type, email) = decode
    form = None
    modelclass = Guide if request_type=='guide' else Participant
    formclass = GuideForm if request_type=='guide' else ParticipantForm
    instance = modelclass.objects.filter(email=email).first()

    # handle submissions
    if request.method == 'POST':
        form = formclass(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.email = email
            obj.save()
            form.save_m2m()
            message='IETF {} {} {} <{}> has {} their information'.format(request_type, obj.given_name, obj.surname, obj.email, 'updated' if instance else 'created')
            send_mail(
                subject=message,
                message=message,
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list = [settings.DEFAULT_FROM_EMAIL],
            )
            return render(request,'guides/saved.html', dict(obj=obj))

    template = 'guides/edit_info_guide.html' if request_type=='guide' else 'guides/edit_info_participant.html'
    if not form:
        form = formclass(instance=instance) if instance else formclass()
    return render(request, template, dict(email=email, form=form))

@login_required
def make_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.by = request.user
            obj.save()
            return redirect(reverse('guides.views.send_match_email', kwargs=dict(match_id=obj.pk)))
    else:
       form = MatchForm()
    return render(request,'guides/makematch.html', dict(form=form))

@login_required
def send_match_email(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.method=='POST':
        if request.POST.get("send"):
            form = MatchEmailForm(request.POST, match=match)
            if form.is_valid():
               message = form.cleaned_data['message'] 
               send_mail(subject='IETF Guide Program Match', message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[match.participant.email, match.guide.email, match.by.email])
               return redirect(reverse('guides.views.matcher_index'))
        elif request.POST.get("cancel"):
            match.delete()
            return redirect(reverse('guides.views.matcher_index'))
        else:
            pass

    form = MatchEmailForm(match = match) 
    return render(request,'guides/send_match_email.html',dict(match=match, form=form))

