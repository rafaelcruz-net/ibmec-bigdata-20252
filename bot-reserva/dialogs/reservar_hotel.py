import json
import requests
from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt, DateTimePrompt
from botbuilder.dialogs.choices import Choice, ListStyle
from config import DefaultConfig

CONFIG = DefaultConfig()

class ReservarHotelDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ReservarHotelDialog, self).__init__("ReservarHotelDialog")
        
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
                "ReservarHotelDialog",
                [
                    self.prompt_nome_step,
                    self.prompt_email_step,
                    self.prompt_celular_step,
                    self.prompt_cpf_step,
                    self.prompt_cidade_step,
                    self.prompt_hotel_step,
                    self.prompt_data_entrada_step,
                    self.prompt_data_saida_step,
                    self.confirmar_reserva_step,
                    self.processar_reserva_step,
                    self.final_step
                ]
            )
        )
                
        self.initial_dialog_id = "ReservarHotelDialog"
    
    async def prompt_nome_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        await step_context.context.send_activity(MessageFactory.text("Vamos realizar sua reserva de hotel!"))
        
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
    
    async def prompt_cidade_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
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
                prompt=MessageFactory.text("Para qual cidade você deseja viajar?"),
                choices=options,
                style=ListStyle.suggested_action
            )
        )
    
    async def prompt_hotel_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["cidade"] = step_context.result.value
        
        # Buscar hotéis disponíveis da API
        try:
            response = requests.get(f"{CONFIG.API_BASE_URL}/opcoes/hoteis")
            hoteis_por_cidade = response.json()
            hoteis = hoteis_por_cidade.get(step_context.values["cidade"], [])
        except:
            # Se falhar, usar algumas opções padrão
            hoteis_padrao = {
                "Rio de Janeiro": ["Copacabana Palace", "Windsor Oceanico"],
                "São Paulo": ["Renaissance Hotel", "Tivoli Mofarrej"],
                "Brasília": ["Royal Tulip", "Melia Brasil 21"],
                "Recife": ["Mar Hotel", "Sheraton Reserva"],
                "Salvador": ["Wish Hotel da Bahia", "Gran Hotel Stella Maris"]
            }
            hoteis = hoteis_padrao.get(step_context.values["cidade"], ["Hotel Padrão A", "Hotel Padrão B"])
        
        options = [Choice(value=hotel) for hotel in hoteis]
        
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(f"Qual hotel em {step_context.values['cidade']} você deseja reservar?"),
                choices=options,
                style=ListStyle.suggested_action
            )
        )
    
    async def prompt_data_entrada_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["hotel"] = step_context.result.value
        
        await step_context.context.send_activity(
            MessageFactory.text("Para a data de entrada, informe no formato DD/MM/AAAA (exemplo: 15/11/2025)")
        )
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Data de check-in:"))
        )
    
    async def prompt_data_saida_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["data_entrada"] = step_context.result
        
        await step_context.context.send_activity(
            MessageFactory.text("Para a data de saída, informe no formato DD/MM/AAAA (exemplo: 20/11/2025)")
        )
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Data de check-out:"))
        )
    
    async def confirmar_reserva_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["data_saida"] = step_context.result
        
        resumo = (
            f"**Resumo da reserva:**\n\n"
            f"**Nome:** {step_context.values['nome']}\n"
            f"**Email:** {step_context.values['email']}\n"
            f"**Celular:** {step_context.values['celular']}\n"
            f"**CPF:** {step_context.values['cpf']}\n"
            f"**Cidade:** {step_context.values['cidade']}\n"
            f"**Hotel:** {step_context.values['hotel']}\n"
            f"**Check-in:** {step_context.values['data_entrada']}\n"
            f"**Check-out:** {step_context.values['data_saida']}\n\n"
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
            # Transformar as datas para o formato correto
            try:
                data_entrada_parts = step_context.values["data_entrada"].split("/")
                data_saida_parts = step_context.values["data_saida"].split("/")
                
                data_entrada_iso = f"{data_entrada_parts[2]}-{data_entrada_parts[1]}-{data_entrada_parts[0]}"
                data_saida_iso = f"{data_saida_parts[2]}-{data_saida_parts[1]}-{data_saida_parts[0]}"
                
                # Criar o payload para a API
                payload = {
                    "cliente": {
                        "nome": step_context.values["nome"],
                        "email": step_context.values["email"],
                        "celular": step_context.values["celular"],
                        "cpf": step_context.values["cpf"]
                    },
                    "cidade": step_context.values["cidade"],
                    "hotel": step_context.values["hotel"],
                    "dataEntrada": data_entrada_iso,
                    "dataSaida": data_saida_iso
                }
                
                # Enviar para a API
                try:
                    response = requests.post(
                        f"{CONFIG.API_BASE_URL}/reservas-hotel", 
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code in [200, 201]:
                        await step_context.context.send_activity(
                            MessageFactory.text("✅ Sua reserva de hotel foi confirmada com sucesso! Em breve você receberá um e-mail com os detalhes.")
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
                choices=[Choice("Voltar ao menu principal"), Choice("Fazer outra reserva de hotel")],
                style=ListStyle.suggested_action
            )
        )
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        escolha = step_context.result.value
        
        if escolha == "Fazer outra reserva de hotel":
            return await step_context.replace_dialog(self.id)
        
        # Voltar para o menu principal
        return await step_context.end_dialog()