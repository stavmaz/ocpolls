# Create your views here.
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import FormView
from polls.forms import CreatePollForm
from polls.models import Poll, Vote
import json


class HomeView(FormView):
    form_class = CreatePollForm

    def form_valid(self, form):
        o = Poll()
        o.proposals = form.cleaned_data['text'].splitlines()
        o.save()


class VoteView(View):
    form_class = CreatePollForm

    def post(self, request, *args, **kwargs):
        o = Vote()
        o.data = json.loads(request.POST['vote'])
        o.save()
        return HttpResponse("OK")
