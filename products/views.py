from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .models import *
from basket.models import *


def home(request):
    categories = ProductCategory.objects.order_by("name")
    images = ProductImage.objects.filter(is_main=True).order_by("-product__created")[:6]

    return render(request, "home.html", locals())


def category_page(request, category_id):
    category = get_object_or_404(ProductCategory, pk=category_id)
    images = ProductImage.objects.filter(product__category=category, is_main=True).order_by('product__name')
    return render(request, "category.html", locals())


def product_filters(request, category_id):
    category = get_object_or_404(ProductCategory, pk=category_id)

    sort = request.POST.get('sort', 'nothing')
    price_from = request.POST.get('price_from', 'nothing')
    price_to = request.POST.get('price_to', 'nothing')
    pf_check = price_from.isdigit()
    pt_check = price_to.isdigit()

    if not pt_check and pf_check:
        images = ProductImage.objects.filter(product__category=category, is_main=True,
                                             product__price__gte=int(price_from))
    elif pt_check and not pf_check:
        images = ProductImage.objects.filter(product__category=category, is_main=True,
                                             product__price__lte=int(price_to))
    elif pt_check and pf_check:
        images = ProductImage.objects.filter(product__category=category, is_main=True,
                                             product__price__range=(int(price_from), int(price_to)))
    else:
        images = ProductImage.objects.filter(product__category=category, is_main=True)

    if sort == 'name':
        images = images.order_by('product__name')
    elif sort == 'cheap':
        images = images.order_by('product__price')
    elif sort == 'expensive':
        images = images.order_by('-product__price')
    elif sort == 'rating':
        images = images.order_by('-product__average_rating')
    elif sort == 'created':
        images = images.order_by('-product__created')

    list = render_to_string('product_list.html', {'images': images})

    return JsonResponse({'list': list})


def product_page(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = Comment.objects.filter(product=product)
    ratings = Rating.objects.all()
    user = request.user

    if user.is_authenticated():
        contains = not ProductInBasket.objects.filter(user=user, product=product).exists()
        contains_comment = not Comment.objects.filter(user=user, product=product).exists()
    else:
        contains_comment = False

    return render(request, "product.html", locals())


@login_required
@require_POST
def add_comment(request):
    text = request.POST['text']

    stars = request.POST['rating']
    product_id = request.POST['product_id']

    user = request.user
    rating = Rating.objects.get(stars=stars)
    product = Product.objects.get(pk=product_id)

    if not Comment.objects.filter(user=user, product=product).exists():
        Comment.objects.create(user=user, rating=rating, product=product, text=text)

    return JsonResponse({})
