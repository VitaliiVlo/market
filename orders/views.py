from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from basket.models import ProductInBasket
from .models import *


@login_required
def myorders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created')
    contains = orders.exists()
    return render(request, "order.html", locals())


@login_required
@require_POST
def addorder(request):
    name = request.POST['name']
    phone = request.POST['phone']
    address = request.POST['address']
    comment = request.POST['comment']

    email = request.POST['email']
    email_check = False
    try:
        validate_email(email)
    except forms.ValidationError:
        email_check = True

    fails = ""

    if email_check:
        fails += "Неправильный Email \n"
    if len(name) < 5:
        fails += "Имя и фамилия минимум - 5 символов \n"
    if len(address) < 5:
        fails += "Адрес минимум - 5 символов \n"
    if not phone.replace("+", "").isdigit() or len(phone) < 10:
        fails += "Номер неправильный \n"

    if fails == "":
        user = request.user
        status = Status.objects.get(id=1)
        order = Order.objects.create(user=user, status=status, customer_name=name, customer_email=email,
                                     customer_phone=phone, customer_address=address, comments=comment)

        products_in_basket = user.productinbasket_set.all()

        for el in products_in_basket:
            ProductInOrder.objects.create(order=order, product=el.product, nmb=el.nmb)

        products_in_basket.delete()

        fails = True

    return JsonResponse({'check': fails})


@login_required
@require_POST
def cancelorder(request):
    id = request.POST['id']
    user = request.user
    status = Status.objects.get(id=4)
    order = Order.objects.get(user=user, id=id)
    order.status = status
    order.save(force_update=True)
    return JsonResponse({'status': order.status.name})
