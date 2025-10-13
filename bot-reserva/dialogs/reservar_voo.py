import json
import requests
from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, DateTimePrompt
from botbuilder.dialogs.choices import Choice, ListStyle
from config import DefaultConfig

CONFIG = DefaultConfig()

class ReservarVooDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ReservarVooDialog, self).__init__("ReservarVooDialog")
        
        # Guarda na memória onde o usuário parou no diálogo
        self.user_state = user_state
        
        # Adiciona prompts necessários
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        # Configurando o ChoicePrompt para usar botões por padrão
        choice_prompt = ChoicePrompt(ChoicePrompt.__name__)
        choice_prompt.style = ListStyle.suggested_action
        self.add_dialog(choice_prompt)
        
        self.add_dialog(DateTimePrompt(DateTimePrompt.__name__))
        
        # Conversação Sequencial (Steps)        
        self.add_dialog(
            WaterfallDialog(
                "ReservarVooDialog",
                [
                    self.prompt_nome_step,
                    self.prompt_email_step,
                    self.prompt_celular_step,
                    self.prompt_cpf_step,
                    self.prompt_origem_step,
                    self.prompt_destino_step,
                    self.prompt_data_step,
                    self.prompt_horario_step,
                    self.confirmar_reserva_step,
                    self.processar_reserva_step,
                    self.final_step
                ]
            )
        )
                
        self.initial_dialog_id = "ReservarVooDialog"
    
    async def prompt_nome_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        await step_context.context.send_activity(MessageFactory.text("Vamos realizar sua reserva de voo!"))
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Por favor, informe seu nome completo:"))
        )
    
    async def prompt_email_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["nome"] = step_context.result
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Informe seu email para contato:"))
        )
    
    async def prompt_celular_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["email"] = step_context.result
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Informe seu número de celular (ex: 21999998888):"))
        )
    
    async def prompt_cpf_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["celular"] = step_context.result
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Informe seu CPF (apenas números):"))
        )
    
    async def prompt_origem_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["cpf"] = step_context.result
        
        # Buscar cidades disponíveis da API
        try:
            response = requests.get(f"{CONFIG.API_BASE_URL}/opcoes/cidades")
            cidades = response.json()
        except:
            # Se falhar, usar algumas opções padrão
            cidades = ["Rio de Janeiro", "São Paulo", "Brasília", "Recife", "Salvador"]
        
        options = [Choice(value=cidade) for cidade in cidades]
        
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Qual é a cidade de origem do seu voo?"),
                choices=options,
                style=ListStyle.suggested_action
            )
        )
    
    async def prompt_destino_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["origem"] = step_context.result.value
        
        # Buscar cidades disponíveis da API
        try:
            response = requests.get(f"{CONFIG.API_BASE_URL}/opcoes/cidades")
            cidades = response.json()
            # Remover cidade de origem das opções
            cidades = [c for c in cidades if c != step_context.values["origem"]]
        except:
            # Se falhar, usar algumas opções padrão
            cidades_todas = ["Rio de Janeiro", "São Paulo", "Brasília", "Recife", "Salvador"]
            cidades = [c for c in cidades_todas if c != step_context.values["origem"]]
        
        options = [Choice(value=cidade) for cidade in cidades]
        
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Qual é o seu destino?"),
                choices=options,
                style=ListStyle.suggested_action
            )
        )
    
    async def prompt_data_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["destino"] = step_context.result.value
        
        await step_context.context.send_activity(
            MessageFactory.text("Para a data do voo, informe no formato DD/MM/AAAA (exemplo: 15/11/2025)")
        )
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Data do voo:"))
        )
    
    async def prompt_horario_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["data"] = step_context.result
        
        # Buscar voos disponíveis da API
        try:
            response = requests.get(f"{CONFIG.API_BASE_URL}/opcoes/voos")
            voos = response.json()
            
            # Encontrar voos que correspondam à origem e destino
            voo_encontrado = None
            for voo in voos:
                if voo["origem"] == step_context.values["origem"] and voo["destino"] == step_context.values["destino"]:
                    voo_encontrado = voo
                    break
            
            if voo_encontrado:
                horarios = voo_encontrado["horarios"]
                codigo_voo = voo_encontrado["codigo"]
            else:
                # Se não encontrou voo específico, usar horários padrão
                horarios = ["08:00", "12:30", "17:45", "21:00"]
                codigo_voo = f"VL{step_context.values['origem'][0]}{step_context.values['destino'][0]}123"
            
        except:
            # Se falhar, usar opções padrão
            horarios = ["08:00", "12:30", "17:45", "21:00"]
            codigo_voo = f"VL{step_context.values['origem'][0]}{step_context.values['destino'][0]}123"
        
        # Guardar o código do voo para usar depois
        step_context.values["codigo_voo"] = codigo_voo
        
        options = [Choice(value=horario) for horario in horarios]
        
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(f"Escolha um horário para o voo {codigo_voo}:"),
                choices=options,
                style=ListStyle.suggested_action
            )
        )
    
    async def confirmar_reserva_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["horario"] = step_context.result.value
        
        resumo = (
            f"**Resumo da reserva de voo:**\n\n"
            f"**Nome:** {step_context.values['nome']}\n"
            f"**Email:** {step_context.values['email']}\n"
            f"**Celular:** {step_context.values['celular']}\n"
            f"**CPF:** {step_context.values['cpf']}\n"
            f"**Origem:** {step_context.values['origem']}\n"
            f"**Destino:** {step_context.values['destino']}\n"
            f"**Data:** {step_context.values['data']}\n"
            f"**Horário:** {step_context.values['horario']}\n"
            f"**Código do voo:** {step_context.values['codigo_voo']}\n\n"
            f"Confirma a reserva?"
        )
        
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(resumo),
                choices=[Choice("Sim"), Choice("Não")],
                style=ListStyle.suggested_action
            )
        )
    
    async def processar_reserva_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result.value == "Sim":
            # Transformar a data para o formato correto
            try:
                data_parts = step_context.values["data"].split("/")
                data_iso = f"{data_parts[2]}-{data_parts[1]}-{data_parts[0]}"
                
                # Criar o payload para a API
                payload = {
                    "cliente": {
                        "nome": step_context.values["nome"],
                        "email": step_context.values["email"],
                        "celular": step_context.values["celular"],
                        "cpf": step_context.values["cpf"]
                    },
                    "cidadeOrigem": step_context.values["origem"],
                    "cidadeDestino": step_context.values["destino"],
                    "data": data_iso,
                    "horario": step_context.values["horario"],
                    "codigoVoo": step_context.values["codigo_voo"]
                }
                
                # Enviar para a API
                try:
                    response = requests.post(
                        f"{CONFIG.API_BASE_URL}/reservas-voo", 
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code in [200, 201]:
                        await step_context.context.send_activity(
                            MessageFactory.text("✅ Sua reserva de voo foi confirmada com sucesso! Em breve você receberá um e-mail com os detalhes.")
                        )
                    else:
                        await step_context.context.send_activity(
                            MessageFactory.text(f"❌ Houve um problema ao confirmar sua reserva. Por favor, tente novamente mais tarde. (Erro: {response.status_code})")
                        )
                except Exception as e:
                    await step_context.context.send_activity(
                        MessageFactory.text("❌ Não foi possível conectar com nosso sistema de reservas. Por favor, tente novamente mais tarde.")
                    )
            except Exception as e:
                await step_context.context.send_activity(
                    MessageFactory.text("❌ Formato de data inválido. Por favor, tente fazer a reserva novamente.")
                )
        else:
            await step_context.context.send_activity(MessageFactory.text("Reserva cancelada."))
        
        # Perguntar se deseja fazer algo mais
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("O que você gostaria de fazer agora?"),
                choices=[Choice("Voltar ao menu principal"), Choice("Fazer outra reserva de voo")],
                style=ListStyle.suggested_action
            )
        )
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        escolha = step_context.result.value
        
        if escolha == "Fazer outra reserva de voo":
            return await step_context.replace_dialog(self.id)
        
        # Voltar para o menu principal
        return await step_context.end_dialog()