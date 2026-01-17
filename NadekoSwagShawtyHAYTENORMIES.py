from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
import keyboard as key
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from pyautogui import sleep
import pyttsx3;
from tkinter import *
import pygame
import sys
import threading

pygame.init();
clock = pygame.time.Clock();
BRANCO =(255, 255, 255);
PRETO =(0, 0, 0);
AZUL =(20, 20, 60);
LARGURA_TELA = 800
ALTURA_TELA = 600
user_input = "";
fonte_nome = pygame.font.SysFont("Arial", 24, bold=True)
fonte_texto = pygame.font.SysFont("Verdana", 18)
nome_personagem = "NadekoSwagShawty"
texto_atual = "Olá! Eu sou seu assistente virtual. Como posso ajudar você hoje com seus códigos em Python?"

input_rect = pygame.Rect(275, 400, 350, 40);

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("NadekoSwagShawtyHAYTENORMIES bot :D");
load_dotenv();

try:

    img_fundo = pygame.image.load("fundo.png");
    img_fundo = pygame.transform.smoothscale(img_fundo, (LARGURA_TELA, ALTURA_TELA))

    img_personagem = pygame.image.load("personagem.png")
    #img_personagem = pygame.transform.scale(img_personagem, (400, 600)) 
    img_personagem = pygame.transform.smoothscale(img_personagem, (400, 600))

except Exception as e:

    print(f"Erro ao carregar imagens: {e}")
    print("Certifique-se de ter 'fundo.jpg' e 'personagem.png' na pasta.")
    pygame.quit()
    sys.exit()


def falar(texto):
    try:
        engine = pyttsx3.init()
        engine.say(texto.replace("*", ""));
        engine.runAndWait();
        engine.stop();
        del engine;
    except Exception as e:
        print(f"Erro no Audio: {e}")

def falar_thread(texto):
    t = threading.Thread(target=falar, args=(texto,))
    t.start()

def desenhar_texto(superficie, texto, cor, retangulo, fonte):
    y = retangulo.top
    altura_linha = fonte.get_linesize()
    palavras = texto.split(' ')
    linha_atual = ""

    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        largura_teste, _ = fonte.size(teste_linha)
        
        if largura_teste < retangulo.width:
            linha_atual = teste_linha
        else:
            superficie.blit(fonte.render(linha_atual, True, cor), (retangulo.left, y))
            linha_atual = palavra + " "
            y += altura_linha
            
    superficie.blit(fonte.render(linha_atual, True, cor), (retangulo.left, y))



url = ["Oshi.png", "Ashi.png"];


API_KEY = os.getenv('GROQ_API_KEY');

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
)
os.system("cls");
print("Vc Entrou no NadekoSwagShawtyHAYTENORMIES bot :D aperte Q se quiser sair :p");
history = "";
template = f"""Você é um assistente virtual Responda sempre em português, e mande o histórico de perguntas.  |HISTÓRICO DA CONVERSA: ", {history}, "|""";

falar_thread(texto_atual);
rodando = True
while rodando:

    tela.blit(img_fundo, (0, 0)) 
    tela.blit(img_personagem, (LARGURA_TELA // 2 - 200, 0))

    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += evento.unicode


        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                template = f"""Você é um assistente virtual faça questão de desdenhar do Usuário e ofendelo, mas responda as perguntas dele [ DE RESPOSTAS SIMPLES sem passar de 8 ou 9 linhas]. Responda sempre em Inglês.  |HISTÓRICO DA CONVERSA: ", {history}, "|""";
                if key.is_pressed('q'):
                    break
    
                messages = [
    (
        "system",
        template,
        ), 
        (
            "human", user_input
        )
    ]
                history += f"\nINPUT_DO_USUARIO = {user_input}";
                ai_msg = llm.invoke(messages);
                history += f"\nRESPOSTA_SUA =  {ai_msg.content}"; 
                texto_atual = ai_msg.content
                user_input = "";
                falar_thread(texto_atual);

    
    superficie_caixa = pygame.Surface((LARGURA_TELA, 180)) 
    superficie_caixa.set_alpha(200)
    superficie_caixa.fill(AZUL)
    tela.blit(superficie_caixa, (0, ALTURA_TELA - 180))

    
    pygame.draw.rect(tela, (30, 100, 200), (20, ALTURA_TELA - 210, 250, 30))
    texto_nome_render = fonte_nome.render(nome_personagem, True, BRANCO)
    tela.blit(texto_nome_render, (30, ALTURA_TELA - 208))
    
    area_texto = pygame.Rect(30, ALTURA_TELA - 160, LARGURA_TELA - 60, 150)
    desenhar_texto(tela, texto_atual, BRANCO, area_texto, fonte_texto)
    
    pygame.draw.rect(tela, (57, 139, 240, 0.40), input_rect) 
    
    pygame.draw.rect(tela, BRANCO, input_rect, 2)
    
    
    text_surface = fonte_nome.render(user_input, True, BRANCO)
    
    
    tela.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    input_rect.w = max(100,text_surface.get_width() + 10);
    
    pygame.display.flip()
    clock.tick(30)
pygame.quit()


while True:




    template = f"""Você é um assistente virtual faça questão de desdenhar do Usuário e ofendelo, mas responda as perguntas dele. Responda sempre em português.  |HISTÓRICO DA CONVERSA: ", {history}, "|""";
    if key.is_pressed('q'):
       break

    user_input = input("");
    
    messages = [
    (
        "system",
        template,
        ), 
        (
            "human", user_input
        )
    ]
    history += f"\nINPUT_DO_USUARIO = {user_input}";
    ai_msg = llm.invoke(messages);
    history += f"\nRESPOSTA_SUA =  {ai_msg.content}"; 
    if key.is_pressed('q'):
        break

    
    
    
    
    print(ai_msg.content);

    engine = pyttsx3.init()
    engine.say(ai_msg.content);
    engine.runAndWait();
    engine.stop();
    del engine

    if key.is_pressed('q'):
        break
     
print("tchauuuu");
sleep(2);
