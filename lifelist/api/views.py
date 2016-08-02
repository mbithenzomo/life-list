from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import Bucketlist
from api.serializers import BucketlistSerializer


class IndexView(TemplateView):
    """
    Handles the index URL
    """
    def get(self, request):
        return render(request, 'index.html')


class HomeView(TemplateView):
    """
    Handles the dashboard homepage
    """
    def get(self, request):
        return render(request, 'dashboard.html')


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def bucketlist_list(request):
    """
    List all bucket lists, or create a new bucket list.
    """
    if request.method == 'GET':
        bucketlists = Bucketlist.objects.all()
        serializer = BucketlistSerializer(bucketlists, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BucketlistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def bucketlist_detail(request, pk):
    """
    Retrieve, update or delete a bucket list.
    """
    try:
        bucketlist = Bucketlist.objects.get(pk=pk)
    except Bucketlist.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BucketlistSerializer(bucketlist)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BucketlistSerializer(bucketlist, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        bucketlist.delete()
        return HttpResponse(status=204)
