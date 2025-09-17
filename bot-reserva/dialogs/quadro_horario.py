from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

class QuadroHorarioDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(QuadroHorarioDialog, self).__init__("QuadroHorarioDialog")
        
        #Grava na memoria aonde o usuário está no fluxo de conversa
        self.user_state = user_state
        
        #Adicionar prompt de matricula
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        #Registro de Funções de Conversação Sequencial
        self.add_dialog(
            WaterfallDialog(
                "QuadroHorarioDialog",
                [
                    self.prompt_matricula_step,
                    self.process_matricula_step
                ]
            )
        )
        
        self.initial_dialog_id = "QuadroHorarioDialog"
        
    async def prompt_matricula_step(self, step_context: WaterfallStepContext):
        
        message = MessageFactory.text("Digite a matricula para consultar seu quadro de horario:")
        
        prompt_option = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text("Desculpe não entendi, digite a matricula para consultar o quadro de horario:")
        )
        
        return await step_context.prompt(TextPrompt.__name__, prompt_option)
        
    async def process_matricula_step(self, step_context: WaterfallStepContext):
        matricula = step_context.result
        
        print(f"matricula digitada {matricula}")
        
        #TODO: PREPARAR BACKEND PARA CONSULTAR QUADRO DE HORARIO
        
        return await step_context.end_dialog()
        
