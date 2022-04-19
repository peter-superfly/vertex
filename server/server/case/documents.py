from django_elasticsearch_dsl import (
    Document, fields, Index
)
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl.registries import registry
from .models import Case


@registry.register_document
class CaseDocument(Document):
    class Index:
        name = 'case'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1
        }
    tags = fields.ListField(StringField(
        fields={
            'raw': KeywordField(),
        }
    ))
    judges = fields.ListField(StringField(
        fields={
            'raw': KeywordField(),
        }
    ))

    court_name = StringField(
        fields={
            'raw': KeywordField(),
        }
    )

    case_class = StringField(
        fields={
            'raw': KeywordField(),
        }
    )

    case_action = StringField(
        fields={
            'raw': KeywordField(),
        }
    )

    updated_at = fields.DateField()
    

    class Django:
        model = Case
      
        fields = [
            'id',
            'kenyalaw_id',
            'title',
            'case_number',
            'case_name',
            'citation',
            'parties',
            'description',
            'delivery_date',
            'file_id'
        ]
