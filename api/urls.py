from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('<str:klass_prdt>-list/', views.product_list, name='api-list'),
    path('<klass_prdt>/<int:pk>/', views.product_detail, name='api-Product-Details')

]
