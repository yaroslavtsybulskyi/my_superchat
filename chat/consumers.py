import json
from typing import Optional, List

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Profile


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat communication between users of the same company.
    """

    async def connect(self) -> None:
        """
        Called when a WebSocket connection is opened.
        Authenticates the user, determines their company group,
        and sends the initial list of connected usernames.
        :return: None
        """
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        profile = await self.get_user_profile()
        if not profile:
            await self.close()
            return

        self.company_id = profile.company.id
        self.group_name = f"company_{self.company_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        usernames = await self.get_company_usernames()
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'usernames': usernames,
        }))

    async def disconnect(self, close_code: int) -> None:
        """
        Called when the WebSocket connection is closed.
        Removes the user from their company group.
        :param close_code: code of the websocket close
        :return: None
        """
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data: str) -> None:
        """
        Called when a message is received over the WebSocket.
        Broadcasts the message to the rest of the group.
        :param text_data: text data of the message
        :return: None
        """
        data = json.loads(text_data)
        message = data.get('message', '')

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
            }
        )

    async def chat_message(self, event: dict) -> None:
        """
        Handles broadcast messages sent to the group.
        Sends the message back to all connected users in the group.
        :param event: Event received from the websocket
        :return: None
        """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'user': event['user'],
        }))

    @database_sync_to_async
    def get_user_profile(self) -> Optional[Profile]:
        """
        Retrieves the Profile instance of the current user.
        Returns None if not found.
        :return: Profile instance
        """
        try:
            return Profile.objects.select_related("company").get(user=self.user)
        except Profile.DoesNotExist:
            return None

    @database_sync_to_async
    def get_company_usernames(self) -> List[str]:
        """
        Retrieves a list of usernames of all users in the same company as the current user.
        Returns an empty list if the profile does not exist.
        :return: List of usernames
        """
        try:
            profile = Profile.objects.select_related("company").get(user=self.user)
            return list(
                profile.company.users.select_related("user").values_list('user__username', flat=True)
            )
        except Profile.DoesNotExist:
            return []
