from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice
from dialogs.consultar_matricula import ConsultarMatriculaDialog
from dialogs.enturmar_aluno import EnturmarAlunoDialog
from dialogs.quadro_horario import QuadroHorarioDialog


class MainDialog(ComponentDialog):
    
    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__("MainDialog")
        
        #Guarda na memoria aonde o usuário parou no dialogo
        self.user_state = user_state
        
        #Prompt para escolher as opções de atendimento
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        
        #Area de Atendimento de Consultar Matricula
        self.add_dialog(ConsultarMatriculaDialog(self.user_state))
        
        #Area de Atendimento de Enturmar Aluno
        self.add_dialog(EnturmarAlunoDialog(self.user_state))
        
        #Area de Atendimento de Quadro de Horario
        self.add_dialog(QuadroHorarioDialog(self.user_state))
        
        
        
        #Conversação Sequencial (Steps)        
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
                    Choice("Ajuda")
                ]
            )
        )
    async def process_option_step(self, step_context: WaterfallStepContext):
        #Captura o que o usuário escolheu de opcao
        option = step_context.result.value
        
        if (option == "Consultar Matricula"):
            return await step_context.begin_dialog("ConsultarMatriculaDialog")
        elif (option == "Enturmar Aluno"):
            return await step_context.begin_dialog("EnturmarAlunoDialog")
        elif (option == "Quadro de Horario"):
            return await step_context.begin_dialog("QuadroHorarioDialog")
        elif (option == "Ajuda"):
            return await step_context.context.send_activity(
                    MessageFactory.text(
                        "Voce escolheu a opção Ajuda"
                    )
                )
        return await step_context.end_dialog()