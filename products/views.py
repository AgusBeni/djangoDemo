from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson.objectid import ObjectId
from bson import json_util
import json

from django.http import JsonResponse
from pymongo import MongoClient
from django.conf import settings

mongo_client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
db = mongo_client[settings.MONGODB_NAME]
collection = db['product']

@api_view(['GET'])
def product_list(request):

    if request.method == 'GET':
        product_list = collection.find()

        doc_list = json_util.dumps(product_list)

        return JsonResponse(doc_list, safe=False)

@api_view(['GET'])
def product_detail(id, format=None):
    try:
        product = collection.find_one({'_id': ObjectId(id)})
        product['_id'] = str(product['_id'])
        return Response(product)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    
@api_view(['POST'])
def product_detail_add(request, format=None):

    if request.method == 'POST':

        serializer = ProductSerializers(data=request.data)

        if serializer.is_valid():

            data_insert = serializer.validated_data
            data_insert['price'] = float(data_insert['price'])
            result = collection.insert_one(data_insert)

            if result.inserted_id:
                data_insert['_id'] = str(result.inserted_id)

                return Response(data_insert, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','DELETE'])
def product_delete(id, format=None):
    try:
        collection.delete_one({'_id': ObjectId(id)})

        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)