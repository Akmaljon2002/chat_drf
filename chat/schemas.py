from drf_spectacular.utils import extend_schema
from chat.serializers import SendMessageSer, SendMessageResponse, MessagesResponseModel

send_message_schema = extend_schema(
    summary="Send message",
    request=SendMessageSer,
    responses=SendMessageResponse
)


get_message_schema = extend_schema(
    summary="Get message",
    request=None,
    responses=MessagesResponseModel
)