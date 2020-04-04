from django.contrib import admin
from .models import Article, AdvertImages, Comment, Profile # Images,  AdvertImages
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')




class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')


#class ImagesAdmin(admin.ModelAdmin):
    #list_display = ('post', 'image')

class AdvertImagesAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'amount', 'duration')



admin.site.register(Comment)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Profile, ProfileAdmin)
#admin.site.register(Images, ImagesAdmin)
admin.site.register(AdvertImages)
