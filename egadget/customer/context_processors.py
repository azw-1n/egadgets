#context proccessors are simple functions defined to populate templates with a context
from account.models import cart

def cart_count(request):
    if request.user.is_authenticated:
        cnt=cart.objects.filter(user=request.user).count()
        return {'count':cnt}
    else:
        return{"count":0}
