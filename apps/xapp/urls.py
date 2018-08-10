from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.indexlogin), #start as login
    url(r'^register$', views.register),#register page
    url(r'^create$', views.createuser), #registers the user
    url(r'^dashboard/$', views.dashboard),#main page
    url(r'^dashboard/(?P<user_id>\d+)$', views.dashboard), #dashboard redirect with user.
    
    url(r'^add/(?P<user_id>\d+)$', views.add),# page for add the product
    url(r'^showproduct/(?P<x>\d+)$', views.showproduct),# show a product 
    url(r'^addtowish/(?P<x>\d+)$', views.addtowish),# add a product  to wishlist 
    url(r'^remove/(?P<x>\d+)$', views.remove),# removes a product 
    url(r'^delete/(?P<x>\d+)$', views.delete),# Deletes a product 
    
    url(r'^loginprocess$', views.loginprocess), #logs in the user
    url(r'^addproduct$', views.addproduct),# add the trip process
    url(r'^logout$', views.logout),#log out
]
