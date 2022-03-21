from django.contrib import admin
from .models import Cohort, Profile, Module, Discussion


admin.site.register(Profile)
admin.site.register(Cohort)
admin.site.register(Module)
admin.site.register(Discussion)
