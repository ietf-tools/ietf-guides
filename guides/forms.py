from django import forms

from .models import Guide, Participant, Match, YNM_YES
from django.template.loader import render_to_string
from django.db.models import Q


class EmailForm(forms.Form):
    email = forms.EmailField(label=u'Email address', required=True)

GuideForm = forms.modelform_factory(Guide,exclude=['email',], widgets={'language':forms.CheckboxSelectMultiple(),'areas':forms.CheckboxSelectMultiple(),})

ParticipantForm = forms.modelform_factory(Participant,exclude=['email',], widgets={'areas':forms.CheckboxSelectMultiple(),})

class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = \
            Participant.objects.filter(Q(match__isnull=True,
                                         match__attending=YNM_NO))

    class Meta:
        model = Match
        exclude = ['by','time',]

class MatchEmailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.match = kwargs.pop('match')
        super(MatchEmailForm, self).__init__(*args, **kwargs)
        self.fields['message'].initial = render_to_string('guides/match_email.txt',dict(match=self.match))

    message = forms.CharField(widget=forms.Textarea(attrs={"rows":22}), help_text="Make any changes needed to the message body before sending.")
