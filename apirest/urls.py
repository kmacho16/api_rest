from django.conf.urls import url
from apirest import views

from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as awview


urlpatterns = [
	url(r'^series/$', views.serie_list),
    url(r'^series/(?P<pk>[0-9]+)/$', views.serie_detail),

    url(r'^register/$', view = views.Register.as_view()),
    url(r'^change/password/$', view = views.ChangePassword.as_view()),
    url(r'^get/profile/$', view = views.my_profile.as_view()),
    url(r'^create/group/$', view = views.create_group.as_view()),
    url(r'^get/groups/$', view = views.list_groups.as_view()),
    url(r'^create/token/$', view = views.create_token.as_view()),    
    url(r'^burn/token/$', view = views.burn_token.as_view()),

    url(r'^login/$',view=awview.obtain_auth_token),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout),

    url(r'^generar/token/$', views.generateToken)


]