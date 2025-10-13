#!/usr/bin/env python3

from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus
from botbuilder.dialogs.prompts import ChoicePrompt
from botbuilder.dialogs.choices import ListStyle

class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        """Executa um diálogo usando o contexto e acessor de estado."""
        dialog_set = DialogSet(accessor)
        
        # Configurar choice prompts para usar botões por padrão
        for dialog_id, dialog_obj in dialog_set._dialogs.items():
            if isinstance(dialog_obj, ChoicePrompt):
                dialog_obj.style = ListStyle.suggested_action
                
        dialog_set.add(dialog)
        
        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)