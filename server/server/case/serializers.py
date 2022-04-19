import json
from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from case.models import Case, Person
from case.documents import CaseDocument

class CaseDocumentSerializer(DocumentSerializer):
    tags = serializers.ListField()
    judges = serializers.ListField()
    class Meta:
        model = Case
        document = CaseDocument
        fields = '__all__'

        def get_location(self, obj):
            try:
                return obj.location.to_dict()
            except:
                return {}

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class CaseListSerializer(serializers.ModelSerializer):
    judges = serializers.SerializerMethodField('judges_get', allow_null=True, required=False)
    class Meta:
        model = Case
        fields = '__all__'


    def judges_get(self, obj):
        try: 
            return list(obj.judges.all().values())
        except Exception as e:
            return []
    


