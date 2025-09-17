from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

class ConsultarMatriculaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ConsultarMatriculaDialog, self).__init__("ConsultarMatriculaDialog")
        
        #Grava na memoria aonde o usuário está no fluxo de conversa
        self.user_state = user_state
        
        #Adicionar prompt de cpf
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        #Registro de Funções de Conversação Sequencial
        self.add_dialog(
            WaterfallDialog(
                "ConsultarMatriculaDialog",
                [
                    self.prompt_cpf_step,
                    self.process_cpf_step
                ]
            )
        )
        
        self.initial_dialog_id = "ConsultarMatriculaDialog"
        
    async def prompt_cpf_step(self, step_context: WaterfallStepContext):
        
        message = MessageFactory.text("Digite o cpf para consultar a matricula:")
        
        prompt_option = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text("Desculpe não entendi, digite o cpf para consultar a matricula:")
        )
        
        return await step_context.prompt(TextPrompt.__name__, prompt_option)
        
    async def process_cpf_step(self, step_context: WaterfallStepContext):
        cpf = step_context.result
        
        print(f"CPF digitado {cpf}")
        
        #TODO: PREPARAR BACKEND PARA CONSULTAR A MATRICULA
        
        return await step_context.end_dialog()
        
