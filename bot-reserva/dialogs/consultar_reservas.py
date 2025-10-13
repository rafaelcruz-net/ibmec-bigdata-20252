import json
import requests
from datetime import datetime
from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice, ListStyle
from config import DefaultConfig

CONFIG = DefaultConfig()

class ConsultarReservasDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ConsultarReservasDialog, self).__init__("ConsultarReservasDialog")
        
        # Guarda na memória onde o usuário parou no diálogo
        self.user_state = user_state
        
        # Adiciona prompts necessários
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        
        # Configurando o ChoicePrompt para usar botões por padrão
        choice_prompt = ChoicePrompt(ChoicePrompt.__name__)
        choice_prompt.style = ListStyle.suggested_action
        self.add_dialog(choice_prompt)
        
        # Conversação Sequencial (Steps)        
        self.add_dialog(
            WaterfallDialog(
                "ConsultarReservasDialog",
                [
                    self.prompt_cpf_step,
                    self.prompt_tipo_reserva_step,
                    self.process_consulta_step,
                    self.final_step
                ]
            )
        )
                
        self.initial_dialog_id = "ConsultarReservasDialog"
        
    async def prompt_cpf_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Por favor, digite seu CPF para consultar suas reservas:"))
        )
    
    async def prompt_tipo_reserva_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Armazena o CPF informado
        step_context.values["cpf"] = step_context.result
        
        # Pergunta qual tipo de reserva quer consultar
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Qual tipo de reserva você deseja consultar?"),
                choices=[Choice("Hotéis"), Choice("Voos"), Choice("Ambos")],
                style=ListStyle.suggested_action
            )
        )
    
    async def process_consulta_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        tipo_reserva = step_context.result.value
        cpf = step_context.values["cpf"]
        
        await step_context.context.send_activity(f"Consultando reservas para o CPF: {cpf}...")
        
        reservas_hotel = []
        reservas_voo = []
        encontrou_reservas = False
        
        # Consultar reservas de hotel
        if tipo_reserva in ["Hotéis", "Ambos"]:
            try:
                response = requests.get(f"{CONFIG.API_BASE_URL}/reservas-hotel/cliente/cpf/{cpf}")
                if response.status_code == 200:
                    reservas_hotel = response.json()
            except Exception as e:
                await step_context.context.send_activity("Não foi possível conectar ao sistema de reservas de hotéis.")
        
        # Consultar reservas de voo
        if tipo_reserva in ["Voos", "Ambos"]:
            try:
                response = requests.get(f"{CONFIG.API_BASE_URL}/reservas-voo/cliente/cpf/{cpf}")
                if response.status_code == 200:
                    reservas_voo = response.json()
            except Exception as e:
                await step_context.context.send_activity("Não foi possível conectar ao sistema de reservas de voos.")
        
        # Mostrar resultados
        if (tipo_reserva in ["Hotéis", "Ambos"] and reservas_hotel) or (tipo_reserva in ["Voos", "Ambos"] and reservas_voo):
            await step_context.context.send_activity("Aqui estão suas reservas:")
            encontrou_reservas = True
            
            # Mostrar reservas de hotel
            if tipo_reserva in ["Hotéis", "Ambos"]:
                if reservas_hotel:
                    for i, reserva in enumerate(reservas_hotel):
                        # Formatar as datas
                        data_entrada = datetime.fromisoformat(reserva.get("dataEntrada", "").split('T')[0]).strftime("%d/%m/%Y")
                        data_saida = datetime.fromisoformat(reserva.get("dataSaida", "").split('T')[0]).strftime("%d/%m/%Y")
                        
                        mensagem = (
                            f"**Reserva de Hotel #{i+1}**\n"
                            f"Hotel: {reserva.get('hotel', 'N/A')}\n"
                            f"Cidade: {reserva.get('cidade', 'N/A')}\n"
                            f"Check-in: {data_entrada}\n"
                            f"Check-out: {data_saida}\n"
                        )
                        await step_context.context.send_activity(mensagem)
                else:
                    await step_context.context.send_activity("Você não possui reservas de hotéis.")
            
            # Mostrar reservas de voo
            if tipo_reserva in ["Voos", "Ambos"]:
                if reservas_voo:
                    for i, reserva in enumerate(reservas_voo):
                        # Formatar a data
                        data = datetime.fromisoformat(reserva.get("data", "").split('T')[0]).strftime("%d/%m/%Y")
                        
                        mensagem = (
                            f"**Reserva de Voo #{i+1}**\n"
                            f"Código do voo: {reserva.get('codigoVoo', 'N/A')}\n"
                            f"Origem: {reserva.get('cidadeOrigem', 'N/A')}\n"
                            f"Destino: {reserva.get('cidadeDestino', 'N/A')}\n"
                            f"Data: {data}\n"
                            f"Horário: {reserva.get('horario', 'N/A')}\n"
                        )
                        await step_context.context.send_activity(mensagem)
                else:
                    await step_context.context.send_activity("Você não possui reservas de voos.")
        
        if not encontrou_reservas:
            await step_context.context.send_activity("Não encontramos reservas para este CPF.")
            
        # Perguntar se deseja fazer nova consulta ou voltar ao menu
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("O que você deseja fazer agora?"),
                choices=[Choice("Voltar ao menu principal"), Choice("Nova consulta")],
                style=ListStyle.suggested_action
            )
        )
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        escolha = step_context.result.value
        
        if escolha == "Nova consulta":
            return await step_context.replace_dialog(self.id)
        
        # Voltar para o menu principal
        return await step_context.end_dialog()