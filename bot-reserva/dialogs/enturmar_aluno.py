from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice

class EnturmarAlunoDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(EnturmarAlunoDialog, self).__init__("EnturmarAlunoDialog")
        
        #Guarda na memoria aonde o usuário parou no dialogo
        self.user_state = user_state
        
        #Adiciona pedido de matricula para enturmar
        self.add_dialog(TextPrompt("matriculaPrompt"))
        self.add_dialog(TextPrompt("disciplinaPrompt"))
        self.add_dialog(ChoicePrompt("horarioPrompt"))
        
        #Conversação Sequencial (Steps)        
        self.add_dialog(
            WaterfallDialog(
                "EnturmarAlunoDialog",
                [
                    self.prompt_matricula_step,
                    self.process_matricula_step,
                    self.prompt_disciplina_step,
                    self.process_enturmar_step
                ]
            )
        )
                
        self.initial_dialog_id = "EnturmarAlunoDialog"
        
    async def prompt_matricula_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "matriculaPrompt",
            PromptOptions(prompt=MessageFactory.text("Por favor, digite sua matricula:"))
        )
    async def process_matricula_step(self, step_context: WaterfallStepContext):
        
        #Grava na memoria a matricula o que usuario digitou
        step_context.values["matricula"] = step_context.result
        
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Digite a disciplina que deseja enturmar"),
            retry_prompt=MessageFactory.text("Não entendi, digite disciplina que deseja enturmar")
        )
        
        return await step_context.prompt("disciplinaPrompt",prompt_options)
    async def prompt_disciplina_step(self, step_context: WaterfallStepContext):
        
        #Grava na memoria a disciplina o que usuario digitou
        step_context.values["disciplina"] = step_context.result
        
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Escolha o horario que deseja se matricular:"),
            choices=[
                Choice("Manhã"),
                Choice("Tarde"),
                Choice("Noite")
            ]
        )
        
        return await step_context.prompt("horarioPrompt",prompt_options)
    
    async def process_enturmar_step(self, step_context: WaterfallStepContext):

        #Grava na memoria o horario o que usuario escolheu
        step_context.values["horario"] = step_context.result.value
        
        #Pega da memoria os valores
        matricula = step_context.values["matricula"]
        disciplina = step_context.values["disciplina"]
        horario = step_context.values["horario"]
        
        print(f"Matricula:{matricula}, disciplina:{disciplina}, horario:{horario}")
        
        #TODO: CHAMAR O BACKEND PARA ENTURMAR
        
        return await step_context.end_dialog()


        
