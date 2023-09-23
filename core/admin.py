from django.contrib import admin

from .models import Designer, Merchant, User, Enquiry,Followers,Following,Notification

admin.site.register(User)
admin.site.register(Designer)
admin.site.register(Merchant)
#admin.site.register(Enquiry)
admin.site.register(Following)
admin.site.register(Followers)
admin.site.register(Notification)