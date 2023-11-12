from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse
from pymongo import MongoClient
from django.conf import settings

mongo_client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
db = mongo_client[settings.MONGODB_NAME]
collection = db['order']

@api_view(['GET'])
def product_list(request):

    if request.method == 'GET':
        order_list = collection.find()

        document_list = [doc for doc in order_list]

        return JsonResponse(document_list, safe=False)

# @api_view(['GET', 'POST'])
# def product_list(request, format=None):

#     if request.method == 'GET':
#         #get all the products
#         products = Product.objects.all()
#         #serialize them
#         serializer = ProductSerializers(products, many=True)
#         #return json
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = ProductSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id, format=None):

    try:
        product = collection.find_one({'_id': id})
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    