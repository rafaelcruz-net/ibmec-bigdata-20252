from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

class QuadroHorarioDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(QuadroHorarioDialog, self).__init__("QuadroHorarioDialog")
        
        #Guarda na memoria aonde o usuário parou no dialogo
        self.user_state = user_state
        
        #Adiciona pedido de CPF para consultar a matricula
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        #Conversação Sequencial (Steps)        
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
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Por favor, digite a matricula para exibir o quadro de horario:"))
        )
    async def process_matricula_step(self, step_context: WaterfallStepContext):
        matricula = step_context.result
        
        #TODO: CRIAR LOGICA DE CONSULTA AO BACKEND PARA O QUADRO DE HORARIO
        
        return await step_context.end_dialog()
        
