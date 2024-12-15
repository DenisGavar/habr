from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GeneticTest
from .serializers import GeneticTestSerializer
from django.db.models import Avg, Max, Count, Q

class GeneticTestListView(APIView):
    def get(self, request):
        species = request.query_params.get('species')
        if species:
            tests = GeneticTest.objects.filter(species=species)
        else:
            tests = GeneticTest.objects.all()
        serializer = GeneticTestSerializer(tests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GeneticTestSerializer(data=request.data)
        if serializer.is_valid():
            test = serializer.save()
            return Response({'message': 'Данные успешно добавлены', 'id': test.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatisticsView(APIView):
    def get(self, request):
        statistics = GeneticTest.objects.values('species').annotate(
            total_tests=Count('id'),
            avg_milk_yield=Avg('milk_yield'),
            max_milk_yield=Max('milk_yield'),
            good_health_percentage=Count('id', filter=Q(health_status='good')) * 100.0 / Count('id')
        )
        return Response({'statistics': list(statistics)})
