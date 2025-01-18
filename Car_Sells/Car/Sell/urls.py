from django.contrib import admin
from django.urls import path
from Sell import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),
    path('testing',views.testing),
    path('home',views.home),
   # path('product',views.Product_details),
    path('cart',views.cart),
    path('contact',views.contact),
    path('pdetails/<pid>',views.pdetails),
    path('about',views.about),
    path('register',views.register),
    path('user_login',views.user_login),
    path('user_logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('viewcart',views.viewcart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    #path('makepayment',views.makepayment),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



