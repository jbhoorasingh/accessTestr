from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from .models import UrlCheck, Test
from .serializers import UrlCheckSerializer, CreateUrlCheckSerializer
from .tasks import add, create_tests
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from .forms import UrlCheckForm


class ViewListUrlCheck(APIView):
    """View to list all Url Checks"""
    serializer_class = UrlCheckSerializer

    def get(self, request):
        checks = UrlCheck.objects.all()
        serializer = UrlCheckSerializer(checks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = UrlCheckSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            # create_tests.delay(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewSpecficUrlCheck(APIView):
    """View to a single Url Checks and it's tests"""
    serializer_class = UrlCheckSerializer

    def get(self, request, pk):
        checks = UrlCheck.objects.get(pk=pk)
        serializer = UrlCheckSerializer(checks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def home(request):
    if request.method == 'POST':
        form = UrlCheckForm(request.POST)
        if form.is_valid():
            url_check_obj = form.save()
            return redirect(reverse('url_check_test_result', args=[url_check_obj.pk]))
    else:
        form = UrlCheckForm()
    return render(request, 'index.html', {'form': form})


def url_check_test_result(request, pk):
    url_check_obj = get_object_or_404(UrlCheck, pk=pk)
    return render(request, 'url_check_test_result.html', {'url_check_obj': url_check_obj})