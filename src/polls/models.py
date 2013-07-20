from django.db import models
import json
from annoying.fields import JSONField

#import pyvotecore
#from pyvotecore.schulze_method import SchulzeMethod
from pyvotecore.schulze_pr import SchulzePR

###################################
#
# Single vote format:
# List of lists, ordered by priority.
# Every item in the list are numbers from 0 to N-1, inclusive. All values from 0 to N-1 must be included.
#
# Examples:
# vote = [ [0], [1,2], [3] ] # good
# vote = [ 0, [1,2], [3] ] # bad
# vote = [ (0), [1,2], [3] ] # bad
# vote = ( [0], [1,2], [3] ) # bad
# vote = [ [0], [2,1], [3] ] # good
# vote = [ [0], [1,2], [2,3] ] # bad
# vote = [ [0], [1,2], [4] ] # bad
# vote = [ [4], [1,2], [3] ] # bad
#
# To run Schulze algorimth run:
# print SchulzeMethod(get_schulze_format(votes_list), ballot_notation = "grouping").to_dict()

class DynamicSchulze:

    def __init__(self, candidates):
        self.hist = dict()
        self.schulze_format = list()
        assert type(candidates) in [list, set, tuple]
        self.candidates = set(candidates)
        self.vote_count = 0
        
    def add_vote(self, vote):
        # verify valid permutation
        perm = sum(vote, [])
        perm.sort()
        seen = set()
        for c in perm:
            if not (c in self.candidates) or (c in seen):
                raise Exception("Invalid vote", vote)
            seen.add(c)
        # sort internal-lists
        in_vote = list()
        for sub_v in vote:
            in_vote.append(tuple(sorted(sub_v)))
        self.vote_count += 1
        in_vote = tuple(in_vote)
        if in_vote in self.hist:
            self.hist[in_vote] += 1
        else:
            self.hist[in_vote] = 1
    
    def get_schulze_format(self):
        out = list()
        for vote, count in self.hist.iteritems():
            out.append({'count': count, 'ballot': list(vote)})
        return out
    
    def get_vote_count(self):
        return self.vote_count
    
    def run_schulze(self):
        #return SchulzeMethod(self.get_schulze_format(), ballot_notation = "grouping").as_dict()
        return SchulzePR(self.get_schulze_format(), ballot_notation="grouping").as_dict()
        
class Poll(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    proposals = JSONField()
    # result = models.TextField(null=True, blank=True)

    def calculate_result(self):
        #votes = [v.data for v in self.votes.all()]
        # TODO how to get valid values from the model?
        valid_props = [0, 1, 2]
        schulze = DynamicSchulze(valid_props)
        for v in self.votes.all():
            schulze.add_vote(v.data)
        schulze_res = schulze.run_schulze()
        #print schulze_res
        result = schulze_res['order']
        return [self.proposals[i] for i in result]

        #return [[self.proposals[i] for i in x] for x in result]

    @models.permalink
    def get_absolute_url(self):
        return 'poll', (str(self.id),)

    def json_proposals(self):
        return json.dumps(self.proposals)

class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()

