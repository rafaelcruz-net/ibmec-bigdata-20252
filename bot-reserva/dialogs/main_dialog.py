from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, DialogTurnResult
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import ChoicePrompt, TextPrompt, PromptOptions
from botbuilder.dialogs.choices import Choice, ListStyle

from dialogs.ajuda_dialog import AjudaDialog
from dialogs.reservar_hotel import ReservarHotelDialog
from dialogs.reservar_voo import ReservarVooDialog
from dialogs.consultar_reservas import ConsultarReservasDialog

class MainDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__(MainDialog.__name__)
        
        self.user_state = user_state
        
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        # Configurando o ChoicePrompt para usar botões por padrão
        choice_prompt = ChoicePrompt(ChoicePrompt.__name__)
        choice_prompt.style = ListStyle.suggested_action
        self.add_dialog(choice_prompt)
        
        # Adicionar diálogos
        self.add_dialog(ReservarHotelDialog(user_state))
        self.add_dialog(ReservarVooDialog(user_state))
        self.add_dialog(ConsultarReservasDialog(user_state))
        self.add_dialog(AjudaDialog(user_state))
        
        self.add_dialog(
            WaterfallDialog(
                "WaterfallDialog",
                [
                    self.mostrar_menu_step,
                    self.processar_escolha_step,
                    self.final_step
                ],
            )
        )

        self.initial_dialog_id = "WaterfallDialog"

    async def mostrar_menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Mostrar mensagem de boas-vindas para iniciar
        await step_context.context.send_activity(
            MessageFactory.text("Bem-vindo ao TravelBot! 🌴✈️\n\nO que você gostaria de fazer hoje?")
        )
        
        # Exibir as opções do menu principal com estilo de botão explícito
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha uma opção:"),
                choices=[
                    Choice("Reservar Hotel"), 
                    Choice("Reservar Voo"), 
                    Choice("Consultar Minhas Reservas"),
                    Choice("Ajuda")
                ],
                style=ListStyle.suggested_action
            ),
        )

    async def processar_escolha_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Obter a escolha do usuário
        escolha = step_context.result.value
        
        if escolha == "Reservar Hotel":
            return await step_context.begin_dialog("ReservarHotelDialog")
        elif escolha == "Reservar Voo":
            return await step_context.begin_dialog("ReservarVooDialog")
        elif escolha == "Consultar Minhas Reservas":
            return await step_context.begin_dialog("ConsultarReservasDialog")
        elif escolha == "Ajuda":
            return await step_context.begin_dialog("AjudaDialog")
        
        return await step_context.next(None)
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Perguntar se o usuário deseja fazer mais alguma coisa
        return await step_context.replace_dialog(self.id)