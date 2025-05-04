from django.urls import path
from chat.views import update_company, chat_view

urlpatterns = [
    path('update-company/<int:company_id>/', update_company, name='update_company'),
    path('chat/<str:group_name>/', chat_view, name='chat'),
]
