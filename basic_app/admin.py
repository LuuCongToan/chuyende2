from django.contrib import admin
from basic_app.models import Post,Comment,Like,Group,UserProfileInfo,User,Story,PostGroup,ImageGroup
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = 'Delete selected items'
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = 'Delete selected items'
# Register your models here.
admin.site.register(Post,ImageAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Group)
admin.site.register(UserProfileInfo)
admin.site.register(Story)
admin.site.register(PostGroup)
admin.site.register(ImageGroup)



# admin.site.register(FriendRequest)









