from account.models import Account
from .models import QuizAttempt


def current_user_score(request):
    if request.user.is_authenticated:
        try:
            user = Account.objects.get(pk=request.user.pk)
            latest_attempt = QuizAttempt.objects.filter(user=user).order_by('-completed').first()
            score = latest_attempt.score if latest_attempt else user.score
            return {"current_user_score": score}
        except Account.DoesNotExist:
            return {"current_user_score": 0}

    return {"current_user_score": 0}

