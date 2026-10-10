from account.models import Account



def view_all_user(request):
    if request.user.is_authenticated:
        return {"view_all_user": Account.objects.all().count()}
    return{"view_all_user": 0}
