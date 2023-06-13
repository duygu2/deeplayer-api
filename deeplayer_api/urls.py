from django.contrib import admin
from django.urls import path
from deeplayer_controller.views import generate_animation, hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate_animation', generate_animation, name='generate_animation'),
    path("hello",hello,name="hello"),
]
