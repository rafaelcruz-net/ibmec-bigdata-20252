from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt
from botbuilder.dialogs.choices import Choice

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
                    self.prompt_option_step,
                    self.process_option_step
                ]
            )
        )
        
        
        self.initial_dialog_id = "ConsultarMatriculaDialog"
