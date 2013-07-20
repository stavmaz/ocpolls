from django.db import models
import json
from annoying.fields import JSONField


class Poll(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    proposals = JSONField()
    # result = models.TextField(null=True, blank=True)

    def calculate_result(self):
        votes = [v.data for v in self.votes.all()]

        # TODO do the magic
        result = [[1], [2, 0]]

        return [[self.proposals[i] for i in x] for x in result]


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()
