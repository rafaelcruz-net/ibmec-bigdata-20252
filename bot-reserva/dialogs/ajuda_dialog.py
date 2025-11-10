import json
import requests
from datetime import datetime
from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice, ListStyle
from config import DefaultConfig
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential
from config import DefaultConfig
from dialogs.consultar_reservas import ConsultarReservasDialog
from dialogs.reservar_hotel import ReservarHotelDialog
from dialogs.reservar_voo import ReservarVooDialog

CONFIG = DefaultConfig()

class AjudaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(AjudaDialog, self).__init__("AjudaDialog")
        
        # Guarda na memória onde o usuário parou no diálogo
        self.user_state = user_state
        
        # Adiciona prompts necessários
        self.add_dialog(TextPrompt(TextPrompt.__name__))

        # Adicionar diálogos
        self.add_dialog(ReservarHotelDialog(user_state))
        self.add_dialog(ReservarVooDialog(user_state))
        self.add_dialog(ConsultarReservasDialog(user_state))

       
        # Conversação Sequencial (Steps)        
        self.add_dialog(
            WaterfallDialog(
                "AjudaDialog",
                [
                    self.prompt_ajuda_step,
                    self.final_step
                ]
            )
        )
                
        self.initial_dialog_id = "AjudaDialog"

        #Configuracao do modelo de IA
        self.client = ConversationAnalysisClient(
            endpoint=DefaultConfig.CLU_ENDPOINT,
            credential=AzureKeyCredential(DefaultConfig.CLU_KEY)
        )
        
    async def prompt_ajuda_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Como posso te ajudar?"))
        )
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        text_ajuda = step_context.result

        request_payload = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                        "id": "1",
                        "participantId": "user1",
                        "modality": "text",
                        "language": "pt-BR",
                        "text": text_ajuda
                }
            },
            "parameters": {
                "projectName": "HotelReservation",
                "deploymentName": "HotelReservation",
                "verbose": True
            }
        }

        result = self.client.analyze_conversation(request_payload)

        top_intent = result["result"]["prediction"]["topIntent"]

        if (top_intent == "ReservarHotel"):
            await step_context.begin_dialog("ReservarHotelDialog")
        elif (top_intent == "ConsultarReserva"):
            await step_context.begin_dialog("ConsultarReservasDialog")
        elif (top_intent == "CancelarReserva"):
            await step_context.context.send_activity(f"Cancelando a reserva...")
        else:
            await step_context.end_dialog()
        