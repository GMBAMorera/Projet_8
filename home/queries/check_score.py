from home.models import Aliment, Score
from django.db.models import Avg
from login.models import User
from home.constants import MEAN_VOTE, NO_VOTE


def check_user_score(aliment, user):
    try:
        score = Score.objects.get(aliment=aliment, user=user)
        return score.score
    except Score.DoesNotExist:
        return None

def check_mean_score(aliment):
    all_score = Score.objects.filter(aliment=aliment)
    if all_score.exists():
        mean_score = Score.objects.filter(aliment=aliment).aggregate(Avg('score'))
        mean_score = mean_score['score__avg']
        return MEAN_VOTE.format(mean_score)
    else:
        return NO_VOTE

def vote_for(user, aliment_id, score):
    aliment = Aliment.objects.get(id=aliment_id)

    old_vote = Score.objects.filter(user=user, aliment=aliment)
    if old_vote.exists():
        old_vote.delete()

    Score.objects.create(user=user, aliment=aliment, score=score)