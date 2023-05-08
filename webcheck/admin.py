from django.contrib import admin
from .models import UrlCheck, Test


class UrlCheckAdmin(admin.ModelAdmin):
    list_display = ("url", "created_at")
    # list_filter = ("edl_type",)

    # def edl_entries_count(self, obj):
    #     # from django.db.models import Count
    #     result = EdlEntry.objects.filter(edl_id=obj.id).all()
    #     return len(result)


class TestAdmin(admin.ModelAdmin):
    list_display = ("test_type", "url_check", "status", "created_at", "result", "details", "proof_image")
    # list_filter = ("edl",)



admin.site.register(UrlCheck, UrlCheckAdmin)
admin.site.register(Test, TestAdmin)
