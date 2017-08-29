from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import *


@login_required
def basket_page(request):
    products_in_basket = ProductInBasket.objects.filter(user=request.user).order_by("-created")
    sum = products_in_basket.aggregate(Sum("total_price"))
    contains = products_in_basket.exists()
    return render(request, "basket.html", locals())


@login_required
@require_POST
def basket_remove(request):
    id = request.POST['id']
    ProductInBasket.objects.get(user=request.user, id=id).delete()
    return JsonResponse({})


@login_required
@require_POST
def basket_number(request):
    id = request.POST['id']
    nmb = request.POST['nmb']
    user = request.user
    fail = False

    if nmb.isdigit and int(nmb) > 0:
        product = ProductInBasket.objects.get(user=user, id=id)
        product.nmb = nmb
        product.save(force_update=True)
    else:
        fail = True

    return JsonResponse({'fails': fail})


@login_required
@require_POST
def basket_add(request):
    id = request.POST['id']
    user = request.user
    product = Product.objects.get(id=id)
    ProductInBasket.objects.get_or_create(product=product, user=user)

    return JsonResponse({})
