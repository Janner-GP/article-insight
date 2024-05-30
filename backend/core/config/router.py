from fastapi import APIRouter

from apis.article_api import get_summary
from apis.chat_api import conversation, get_chats, get_chat, get_messages

router = APIRouter()
router.prefix = "/api/v1"

router.add_api_route("/chat/{chat_id}/messages", conversation, methods=["POST"])
router.add_api_route("/summary", get_summary, methods=["POST"])
router.add_api_route("/chats", get_chats, methods=["GET"])
router.add_api_route("/chat/{chat_id}", get_chat, methods=["GET"])
router.add_api_route("/chat/{chat_id}/messages", get_messages, methods=["GET"])