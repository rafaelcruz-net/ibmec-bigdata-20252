@echo off
REM filepath: c:\Users\joaop\Chatbot-Viagem\iniciar-sistema.bat
echo Iniciando o sistema de reservas de viagem...

REM Iniciar o Docker com PostgreSQL
echo Iniciando o PostgreSQL via Docker...
docker-compose up -d

REM Aguardar o PostgreSQL iniciar completamente
echo Aguardando o PostgreSQL inicializar (10 segundos)...
timeout /t 10 /nobreak

REM Iniciar o backend Spring Boot
echo Iniciando o backend Spring Boot...
start cmd /k "cd chatbot-api && mvnw spring-boot:run"

REM Aguardar o backend iniciar
echo Aguardando o backend inicializar (15 segundos)...
timeout /t 15 /nobreak

REM Iniciar o bot Python
echo Iniciando o chatbot...
start cmd /k "cd bot-reserva && python app.py"

echo.
echo Sistema iniciado! Abra o Bot Framework Emulator e conecte-se a:
echo http://localhost:3979/api/messages
echo.