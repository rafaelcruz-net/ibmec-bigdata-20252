from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

class ConsultarMatriculaDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ConsultarMatriculaDialog, self).__init__("ConsultarMatriculaDialog")
        
        #Guarda na memoria aonde o usuário parou no dialogo
        self.user_state = user_state
        
        #Adiciona pedido de CPF para consultar a matricula
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        #Conversação Sequencial (Steps)        
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
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Por favor, digite o cpf para consultar sua matricula:"))
        )
    async def process_cpf_step(self, step_context: WaterfallStepContext):
        cpf = step_context.result
        
        #TODO: CRIAR LOGICA DE CONSULTA AO BACKEND PARA O CPF
        
        return await step_context.end_dialog()
        
