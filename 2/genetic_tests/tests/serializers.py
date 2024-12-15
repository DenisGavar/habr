from rest_framework import serializers
from .models import GeneticTest

class GeneticTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneticTest
        fields = '__all__'
