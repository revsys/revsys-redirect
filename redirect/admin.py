from django.contrib import admin

from .models import Domain, Redirect, Ignore404, Seen404


class DomainAdmin(admin.ModelAdmin):
    model = Domain
    list_display = ('name', 'wildcard')

admin.site.register(Domain, DomainAdmin)


class RedirectAdmin(admin.ModelAdmin):
    model = Redirect
    list_display = ('old_domain', 'old', 'new_domain', 'new')

admin.site.register(Redirect, RedirectAdmin)


class Ignore404Admin(admin.ModelAdmin):
    model = Ignore404
    list_display = ('domain', 'name')

admin.site.register(Ignore404, Ignore404Admin)


class Seen404Admin(admin.ModelAdmin):
    model = Seen404
    list_display = ('domain', 'path', 'count', 'first_seen', 'last_seen')

admin.site.register(Seen404, Seen404Admin)
