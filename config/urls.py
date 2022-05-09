from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages import views as flatpage_views
from django.contrib.flatpages.sitemaps import FlatPageSitemap

# NOTE: This is needed to control language switcher
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from filebrowser.sites import site as filebrowser

from config.sitemaps import StaticViewSitemap

from darkcodr.core.views import switch_language, service_worker, AnonymousWebPushDeviceViewSet, send_notification

sitemaps = {
    "static": StaticViewSitemap,
}

# TODO: Add google analytics client_secret file
# class CustomIndexDashboard(Dashboard):
#     columns = 3

#     def init_with_context(self, context):
#        self.available_children.append(google_analytics_views.GoogleAnalyticsVisitorsTotals)
#        self.available_children.append(google_analytics_views.GoogleAnalyticsVisitorsChart)
#        self.available_children.append(google_analytics_views.GoogleAnalyticsPeriodVisitors)


urlpatterns = i18n_patterns(
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("sw.js", service_worker, name="service_worker"),
    path("offline/", TemplateView.as_view(template_name="pages/offline.html"), name="offline"),
    path("create-wp-subscription", AnonymousWebPushDeviceViewSet.as_view({"post": "create"}), name="create-wp-subscription"),
    path("send-notification", send_notification, name="send-notification"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
        "services/", TemplateView.as_view(template_name="pages/services.html"), name="services"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path(settings.ADMIN_FILEBROWSER_URL, filebrowser.urls),
    path('admin/', include('admin_honeypot.urls', 'admin_honeypot')),
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ADMIN_DOC_URL, include("django.contrib.admindocs.urls")),

    # User management
    # User management
    path('rosetta/', include('rosetta.urls')),
    path("users/", include("darkcodr.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),

    # Your stuff: custom urls includes go here
    path('tinymce/', include('tinymce.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

# urlpatterns += [path("sw.js", service_worker, name="service_worker")]

# flatpages
if flatpage_views:
    urlpatterns += [
        path(_("terms/"), flatpage_views.flatpage, {"url": "/terms/"}, name="terms"),
        path(_("cookies/"), flatpage_views.flatpage, {"url": "/cookies/"}, name="cookies"),
        path(_("privacy/"), flatpage_views.flatpage, {"url": "/privacy/"}, name="privacy"),
    ]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path("sitemap.xml/", sitemap, kwargs={"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += i18n_patterns(
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
        path("__reload__/", include("django_browser_reload.urls")),
    )
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = i18n_patterns(path("__debug__/", include(debug_toolbar.urls))) + urlpatterns

urlpatterns += [
        path("<str:language>/<str:url>/", view=switch_language, name="language"),
]

admin.site.site_header = _("DARKCODR CODES DASHBOARD")
admin.site.site_title = _("DARKCODR CODES DASHBOARD")
admin.site.index_title = _("DARKCODR CODES DASHBOARD")
