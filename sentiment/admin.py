from django.contrib import admin
from .models import fileupload, overall_rating, individual_rating, individual
# Register your models here.

admin.site.register(fileupload)
admin.site.register(overall_rating)
admin.site.register(individual)
admin.site.register(individual_rating)
