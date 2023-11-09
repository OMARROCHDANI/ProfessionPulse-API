from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.
@api_view(['GET'])
def api_home(request, *args, **kwargs):
    """
    DRF API VIEW
    """
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance:
         # data = model_to_dict(instance, fields=['id', 'title', 'price', 'sale_price'])
        data = ProductSerializer(instance).data
    return Response(data)