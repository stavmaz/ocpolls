from annoying.fields import JSONField
from django.db import models
from polls.graphs import DynamicSchulze
from pyvotecore.schulze_pr import SchulzePR
import json


class Poll(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    proposals = JSONField()
    # result = models.TextField(null=True, blank=True)

    def calculate_result(self):
        valid_props = range(len(self.proposals))
        schulze = DynamicSchulze(valid_props)
        for v in self.votes.all():
            schulze.add_vote(v.data)
        schulze_res = schulze.run_schulze()
        # print schulze_res
        result = schulze_res['order']
        return [self.proposals[i] for i in result]

        # return [[self.proposals[i] for i in x] for x in result]

    @models.permalink
    def get_absolute_url(self):
        return 'poll', (str(self.id),)

    def json_proposals(self):
        return json.dumps(self.proposals)

class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()

