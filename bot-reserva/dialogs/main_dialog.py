from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice
from dialogs.consultar_matricula import ConsultarMatriculaDialog
from dialogs.quadro_horario import QuadroHorarioDialog
from dialogs.enturmar_aluno import EnturmarAlunoDialog

class MainDialog(ComponentDialog):
    
    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__("MainDialog")
        
        #Grava na memoria aonde o usuário está no fluxo de conversa
        self.user_state = user_state
        
        #Registro do Prompt de escolha
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        
        #Area de atendimento de consultar matricula
        self.add_dialog(ConsultarMatriculaDialog(self.user_state))
        
        #Area de atendimento de quadro de horario
        self.add_dialog(QuadroHorarioDialog(self.user_state))
        
        #Area de atendimento de enturmar aluno
        self.add_dialog(EnturmarAlunoDialog(self.user_state))
                
        #Registro de Funções de Conversação Sequencial
        self.add_dialog(
            WaterfallDialog(
                "MainDialog",
                [
                    self.prompt_option_step,
                    self.process_option_step
                ]
            )
        )
                
        self.initial_dialog_id = "MainDialog"
        
    async def prompt_option_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Consultar Matricula"),
                    Choice("Enturmar Aluno"),
                    Choice("Quadro de Horario"),
                    Choice("Ajuda"),
                ]
            )
        )
    async def process_option_step(self, step_context: WaterfallStepContext):
        option = step_context.result.value
        
        if (option == "Consultar Matricula"):
            return await step_context.begin_dialog("ConsultarMatriculaDialog")
        elif (option == "Enturmar Aluno"):
            return await step_context.begin_dialog("EnturmarAlunoDialog")
        elif (option == "Quadro de Horario"):
            return await step_context.begin_dialog("QuadroHorarioDialog")
        elif (option == "Ajuda"):
            return await step_context.context.send_activity(
                MessageFactory.text(f"Voce escolheu a opção Ajuda")
            )           


