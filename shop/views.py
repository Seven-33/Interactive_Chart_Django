import random
from datetime import datetime, timedelta

import pytz
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone

from shop.models import Purchase, Item

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

colorPalette = ["#55efc4", "#81ecec", "#74b9ff", "#a29bfe", "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8"]
colorSuccess = colorPalette[0]
colorDanger = colorSuccess[6]


def generate_color_palette(amount):
    palette = []
    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0
    return palette


def get_sales_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)

    # print(
    #     purchases
    #         .annotate(price=F('item__price'))
    #         .annotate(month=TruncMonth('time'))  # Truncate to month and add to select list
    #         .values('month')                          # Group By month
    #         .annotate(c=Count('id'))                  # Select the count of the grouping
    #         .values('month', 'c', 'item__price', 'quantity').order_by()
    # )

    return JsonResponse({
        'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'backgroundColor': ['#79AEC8'],
        'borderColor': ['#79AEC8'],
        'data': [1, 2, 3, 4, 5],
    })


def spend_per_customer_chart(request, year):
    return JsonResponse({
        'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'backgroundColor': ['#79AEC8'],
        'borderColor': ['#79AEC8'],
        'data': [1, 2, 3, 4, 5],
    })


def payment_success_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)

    return JsonResponse({
        'labels': ['Successful', 'Unsuccessful'],
        'backgroundColor': [colorSuccess, colorSuccess],
        'borderColor': [colorDanger, colorDanger],
        'data': [
            purchases.filter(successful=True).count(),
            purchases.filter(successful=False).count(),
        ],
    })


def payment_method_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)
    grouped_purchases = purchases.values('payment_method').annotate(count=Count('id'))\
        .values('payment_method', 'count').order_by('payment_method')

    payment_method_dict = dict()

    for group in grouped_purchases:
        payment_method_dict[dict(Purchase.PAYMENT_METHODS)[group['payment_method']]] = group['count']

    for payment_method in Purchase.PAYMENT_METHODS:
        if payment_method[1] not in payment_method_dict:
            payment_method_dict[payment_method[1]] = 0

    return JsonResponse({
        'labels': list(payment_method_dict.keys()),
        'backgroundColor': generate_color_palette(len(payment_method_dict)),
        'borderColor': generate_color_palette(len(payment_method_dict)),
        'data': list(payment_method_dict.values()),
    })


def generate(request):
    if Purchase.objects.count() > 50:
        return JsonResponse({'detail': 'generate() has already been run.'})

    names = ["Jack", "John", "Mike", "Chris", "Kyle"]
    surname = ["Jackson", "Smith", "Tyson", "Musk", "Gates"]
    items = [
        Item.objects.create(name="Socks", price=6.5), Item.objects.create(name="Pants", price=12),
        Item.objects.create(name="T-Shirt", price=8), Item.objects.create(name="Boots", price=9),
        Item.objects.create(name="Sweater", price=3), Item.objects.create(name="Underwear", price=9),
        Item.objects.create(name="Cap", price=5), Item.objects.create(name="Leggings", price=7),
    ]

    for i in range(0, 2500):
        dt = pytz.utc.localize(datetime.now() - timedelta(days=random.randint(0, 1825)))
        purchase = Purchase.objects.create(
            customer_full_name=names[random.randint(0, len(names)-1)] + " " + surname[random.randint(0, len(surname)-1)],
            item=items[random.randint(0, 2)],
            quantity=random.randint(1, 5),
            payment_method=Purchase.PAYMENT_METHODS[random.randint(0, 2)][0],
            time=timezone.now(),
            successful=True if random.randint(1, 2) == 1 else False,
        )
        purchase.time = dt
        purchase.save()

    return JsonResponse({'detail': 'Generated.'})
