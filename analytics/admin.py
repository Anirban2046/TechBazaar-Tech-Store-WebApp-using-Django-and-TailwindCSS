# analytics/admin.py
from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.auth.models import Group

# Proxy model based on a real model
class AnalyticsLink(Group):
    class Meta:
        proxy = True
        verbose_name = "Analytics"
        verbose_name_plural = "Analytics"

# Admin that redirects to your analytics page
class AnalyticsAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect("/analytics/")

admin.site.register(AnalyticsLink, AnalyticsAdmin)
