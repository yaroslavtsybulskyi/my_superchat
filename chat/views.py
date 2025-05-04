from typing import Union

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat.models import Company


@csrf_exempt
def update_company(request: HttpRequest, company_id: int) -> JsonResponse:
    """
    Handles POST request to update a company's name and broadcasts a message
    to all users in the company's group via WebSocket.

    :param request: The incoming HTTP request.
    :param company_id: ID of the company to update.
    :return: A response indicating the result of the operation.
    """
    if request.method == 'POST':
        new_name = request.POST.get('name')

        try:
            company = Company.objects.get(id=company_id)
            company.name = new_name
            company.save()

            channel_layer = get_channel_layer()
            group_name = f"company_{company_id}"

            async_to_sync(channel_layer.group_send)(
                group_name,
                {"type": "chat_message",
                 "message": f"Company {new_name} updated.",
                 "user": "System"}
            )
            return JsonResponse({'status': 'updated'})

        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)


def chat_view(request: HttpRequest, group_name: str) -> HttpResponse:
    """
    Renders the chat room page with the given group name.
    :param request: The incoming HTTP request.
    :param group_name: The name of the chat group.
    :return: Rendered HTML response for the chat page.
    """
    return render(request, 'chat.html', {'group_name': group_name})
