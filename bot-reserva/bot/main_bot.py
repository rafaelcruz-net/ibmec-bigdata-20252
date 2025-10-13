from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.dialogs import Dialog
from helpers.DialogHelper import DialogHelper

from dialogs.main_dialog import MainDialog

class TravelBot(ActivityHandler):
    """Bot principal para o sistema de reservas de viagens."""

    def __init__(self, conversation_state: ConversationState, user_state: UserState, dialog: MainDialog):
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog
        self.dialog_state_property = self.conversation_state.create_property("DialogState")
        
    async def on_turn(self, turn_context: TurnContext):
        """Executa o processamento da mensagem."""
        await super().on_turn(turn_context)
        
        # Salva o estado da conversa e do usuário
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)
    
    async def on_message_activity(self, turn_context: TurnContext):
        """Processa mensagens recebidas."""
        # Encaminhar para o sistema de diálogos
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.dialog_state_property
        )