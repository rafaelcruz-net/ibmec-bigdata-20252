from botbuilder.dialogs import ComponentDialog
from botbuilder.core import UserState, MessageFactory
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, TextPrompt
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.choices import Choice

class EnturmarAlunoDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(EnturmarAlunoDialog, self).__init__("EnturmarAlunoDialog")
        
        #Grava na memoria aonde o usuário está no fluxo de conversa
        self.user_state = user_state
        
        #Adicionar prompt de matricula
        self.add_dialog(TextPrompt("matriculaPrompt"))
        #Adicionar prompt de disciplina
        self.add_dialog(TextPrompt("disciplinaPrompt"))
        #Adicionar prompt de horario
        self.add_dialog(ChoicePrompt("horarioPrompt"))
                
        
        #Registro de Funções de Conversação Sequencial
        self.add_dialog(
            WaterfallDialog(
                "EnturmarAlunoDialog",
                [
                    self.prompt_matricula_step,
                    self.prompt_disciplina_step,
                    self.prompt_horario_step,
                    self.process_enturmar_step
                ]
            )
        )
        
        self.initial_dialog_id = "EnturmarAlunoDialog"
        
    async def prompt_matricula_step(self, step_context: WaterfallStepContext):
        
        message = MessageFactory.text("Digite a matricula:")
        
        prompt_option = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text("Desculpe não entendi, digite a matricula:")
        )
        
        return await step_context.prompt("matriculaPrompt", prompt_option)
        
    async def prompt_disciplina_step(self, step_context: WaterfallStepContext):
        matricula = step_context.result
        
        #Gravar a matricula na memoria do bot
        step_context.values["matricula"] = matricula
        
        message = MessageFactory.text("Digite a disciplina:")
        
        prompt_option = PromptOptions(
            prompt=message,
            retry_prompt=MessageFactory.text("Desculpe não entendi, digite a disciplina:")
        )
        
        return await step_context.prompt("disciplinaPrompt", prompt_option)
    
    async def prompt_horario_step(self, step_context: WaterfallStepContext):
        disciplina = step_context.result
        
        #Gravar a disciplina na memoria do bot
        step_context.values["disciplina"] = disciplina
        
        return await step_context.prompt(
            "horarioPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Escolha o horário:"),
                choices=[
                    Choice("Manhã"),
                    Choice("Tarde"),
                    Choice("Noite"),
                ]
            )
        )
        
    async def process_enturmar_step(self, step_context: WaterfallStepContext):        
        matricula = step_context.values["matricula"]
        disciplina = step_context.values["disciplina"]
        horario = step_context.result.value
        
        print(f"Matricula:{matricula}, disciplina: {disciplina}, horario: {horario}")
        
        #TODO: PREPARAR BACKEND PARA RECEBER O ENTURMAR ALUNO
        
        return await step_context.end_dialog()


        
        
