import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
    ConversationState,
    MemoryStorage,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from bot.main_bot import TravelBot
from dialogs.main_dialog import MainDialog
from config import DefaultConfig

CONFIG = DefaultConfig()

# Criar configurações do adaptador com ID e senha do app
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)

# Criar adaptador
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Criar armazenamento
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
USER_STATE = UserState(MEMORY)

# Criar diálogo principal
DIALOG = MainDialog(USER_STATE)

# Criar o bot
BOT = TravelBot(CONVERSATION_STATE, USER_STATE, DIALOG)

# Interceptador de erros do adaptador
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] Ocorreu um erro: {error}", file=sys.stderr)
    traceback.print_exc()

    # Enviar mensagem de erro para o usuário
    await context.send_activity("Desculpe, ocorreu um erro.")
    await context.send_activity("Para recomeçar, digite 'olá'.")
    
    # Limpar o estado da conversa
    await CONVERSATION_STATE.delete(context)

ADAPTER.on_turn_error = on_error

# Função para processar as requisições do adaptador
async def messages(req: Request) -> Response:
    # Transformar o corpo da requisição em um objeto Activity
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    # Processar a atividade através do adaptador
    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

# Configurar rotas web
APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error