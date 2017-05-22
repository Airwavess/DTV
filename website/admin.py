from django.contrib import admin
from .models import Attractions

class AttractionsAdmin(admin.ModelAdmin):
	list_display = ('at_name', 'at_category', 'at_description', 'at_url', 'at_img_url')

admin.site.register(Attractions, AttractionsAdmin)