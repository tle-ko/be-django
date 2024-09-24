from django.db import models


class TextGenerationDAO(models.Model):
    request = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    requested_at = models.DateTimeField(blank=True, null=True)
    responsed_at = models.DateTimeField(blank=True, null=True)
    foundation_model = models.CharField(blank=True, null=True, max_length=50)

    class field_name:
        PK = 'pk'
        REQUEST = 'request'
        RESPONSE = 'response'
        CREATED_AT = 'created_at'
        REQUESTED_AT = 'requested_at'
        RESPONSDED_AT = 'responsed_at'
        FOUNDATION_MODEL = 'foundation_model'
