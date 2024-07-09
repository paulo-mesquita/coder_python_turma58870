import sys
import requests
from plyer import notification
import random
import pygame
import os
import logging
import sqlite3

# Constantes
URL_BASE_POKEMON = 'https://pokeapi.co/api/v2/pokemon/'
POKEMONS_ALEATORIOS = [
    'pikachu', 'bulbasaur', 'ivysaur', 'venusaur', 'charmander', 
    'charmeleon', 'charizard', 'squirtle', 'wartortle', 'blastoise', 
    'caterpie', 'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill', 
    'pidgey', 'pidgeotto', 'pidgeot', 'rattata', 'raticate'
]

# Dicionário de emojis correspondentes aos Pokémon
EMOJIS_POKEMON = {
    'pikachu': '⚡️',
    'bulbasaur': '🌿',
    'ivysaur': '🌿',
    'venusaur': '🌿',
    'charmander': '🔥',
    'charmeleon': '🔥',
    'charizard': '🔥',
    'squirtle': '💧',
    'wartortle': '💧',
    'blastoise': '💧',
    'caterpie': '🐛',
    'metapod': '🐛',
    'butterfree': '🦋',
    'weedle': '🐛',
    'kakuna': '🐛',
    'beedrill': '🐝',
    'pidgey': '🐦',
    'pidgeotto': '🐦',
    'pidgeot': '🦅',
    'rattata': '🐭',
    'raticate': '🐭'
}

# Dicionário de tradução de habilidades
traducao_habilidades = {
    'overgrow': 'Espessura',
    'chlorophyll': 'Clorofila',
    'blaze': 'Chama',
    'solar-power': 'Poder Solar',
    'torrent': 'Torrente',
    'rain-dish': 'Cura pela Chuva',
    'shield-dust': 'Poeira de Escudo',
    'run-away': 'Fuga',
    'tinted-lens': 'Lente Colorida',
    'swarm': 'Enxame',
    'sniper': 'Francoatirador',
    'keen-eye': 'Olhos Afiados',
    'tangled-feet': 'Pés Confusos',
    'big-pecks': 'Peito Inchado',
    'guts': 'Guts',
    'hustle': 'Hustle',
    'static': 'Estática',
    'lightning-rod': 'Para-Raios',
    'intimidate': 'Intimidação',
    'rattled': 'Amedrontado'
}

# Dicionário de tradução de tipos
traducao_tipos = {
    'normal': 'Normal',
    'fire': 'Fogo',
    'water': 'Água',
    'electric': 'Elétrico',
    'grass': 'Grama',
    'ice': 'Gelo',
    'fighting': 'Lutador',
    'poison': 'Veneno',
    'ground': 'Terra',
    'flying': 'Voador',
    'psychic': 'Psíquico',
    'bug': 'Inseto',
    'rock': 'Pedra',
    'ghost': 'Fantasma',
    'dragon': 'Dragão',
    'dark': 'Sombrio',
    'steel': 'Aço',
    'fairy': 'Fada'
}

# Dicionário de tradução de atributos
traducao_atributos = {
    'hp': 'HP',
    'attack': 'Ataque',
    'defense': 'Defesa',
    'speed': 'Velocidade'
}

# Configuração do logger
def configurar_logger():
    log = logging.getLogger('projeto_final')
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Logger para registrar em arquivo log.txt
    file_handler = logging.FileHandler('log.txt')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    # Logger para registrar na saída padrão
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)

    return log

# Função para formatar a mensagem de notificação
def formatar_mensagem_notificacao(mensagem, tipo='info'):
    niveis = {'info': 1, 'erro': 3}
    nivel = niveis.get(tipo, 1)

    if tipo == 'info':
        titulo = f"🔔 Alerta! Nível {nivel} - Status da sua PokéDex!"
    else:
        titulo = f"🔔 Alerta! Nível {nivel} - ⚠️ Erro na sua PokéDex!"

    return titulo, mensagem

# Função para exibir notificação e som da Pokédex
def alerta(mensagem, tipo='info'):
    titulo, mensagem_notificacao = formatar_mensagem_notificacao(mensagem, tipo)
    pygame.mixer.init()

    som_path = os.path.join(os.getcwd(), './audio/quem_e_esse_pokemon.mp3')
    if not os.path.exists(som_path):
        som_path = None

    if som_path:
        pygame.mixer.music.load(som_path)
        pygame.mixer.music.play()
    else:
        pass

    notification.notify(
        title=titulo,
        message=mensagem_notificacao,
        app_name='Notificação - PokéAPI',
        timeout=10
    )

# Função para criar o banco de dados SQLite e tabela se não existirem
def criar_bd():
    try:
        conexao = sqlite3.connect('pokedex.db')
        cursor = conexao.cursor()

        # Criar tabela se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                altura REAL,
                peso REAL,
                hp INTEGER,
                attack INTEGER,
                defense INTEGER,
                speed INTEGER,
                habilidades TEXT,
                tipos TEXT
            )
        ''')
        conexao.commit()
        return conexao, cursor
    except sqlite3.Error as error:
        print("Erro ao criar o banco de dados:", error)
        return None, None

# Função para consultar dados do banco de dados
def consultar_bd(cursor, nome_pokemon):
    try:
        cursor.execute('SELECT * FROM pokemon WHERE nome=?', (nome_pokemon,))
        return cursor.fetchone()
    except sqlite3.Error as error:
        print("Erro ao consultar o banco de dados:", error)
        return None

# Função para inserir dados no banco de dados
def inserir_dados(conexao, cursor, pokemon):
    try:
        # Preparar dados para inserção
        altura = pokemon.get('height', 0) / 10  # Tratar altura se não estiver presente
        peso = pokemon.get('weight', 0) / 10  # Tratar peso se não estiver presente
        hp = next((stat['base_stat'] for stat in pokemon['stats'] if stat['stat']['name'] == 'hp'), 0)
        attack = next((stat['base_stat'] for stat in pokemon['stats'] if stat['stat']['name'] == 'attack'), 0)
        defense = next((stat['base_stat'] for stat in pokemon['stats'] if stat['stat']['name'] == 'defense'), 0)
        speed = next((stat['base_stat'] for stat in pokemon['stats'] if stat['stat']['name'] == 'speed'), 0)
        habilidades = ', '.join(traduzir_habilidades(pokemon['abilities']))
        tipos = ', '.join(traduzir_tipos(pokemon['types']))

        # Inserir dados no banco de dados
        cursor.execute('''
            INSERT INTO pokemon (nome, altura, peso, hp, attack, defense, speed, habilidades, tipos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (pokemon['name'], altura, peso, hp, attack, defense, speed, habilidades, tipos))

        conexao.commit()
    except sqlite3.Error as error:
        print("Erro ao inserir dados:", error)

# Função para obter dados da PokéAPI
def obter_dados_pokemon(nome_pokemon):
    try:
        resposta = requests.get(URL_BASE_POKEMON + nome_pokemon)
        if resposta.status_code == 200:
            return resposta.json()
        else:
            print(f'Não foi possível encontrar o Pokémon {nome_pokemon} na PokéAPI (Código do erro: {resposta.status_code}). Tente novamente!')
            return None
    except requests.RequestException as e:
        print(f'Ocorreu um erro ao acessar a PokéAPI ({e}). Verifique sua conexão e tente novamente!')
        return None

# Função para traduzir habilidades
def traduzir_habilidades(habilidades):
    habilidades_traduzidas = []
    for habilidade in habilidades:
        nome_habilidade = habilidade['ability']['name']
        habilidade_traduzida = traducao_habilidades.get(nome_habilidade, nome_habilidade)
        habilidades_traduzidas.append(habilidade_traduzida)
    return habilidades_traduzidas

# Função para traduzir tipos
def traduzir_tipos(tipos):
    tipos_traduzidos = []
    for tipo in tipos:
        nome_tipo = tipo['type']['name']
        tipo_traduzido = traducao_tipos.get(nome_tipo, nome_tipo)
        tipos_traduzidos.append(tipo_traduzido)
    return tipos_traduzidos

# Função para traduzir atributos
def traduzir_atributos(atributos):
    atributos_traduzidos = []
    for atributo in atributos:
        nome_atributo = atributo['stat']['name']
        if nome_atributo in traducao_atributos:
            atributo_traduzido = f"{traducao_atributos[nome_atributo]}: {atributo['base_stat']}"
            atributos_traduzidos.append(atributo_traduzido)
    return atributos_traduzidos

# Função para criar a interface da Pokedex
# Função para criar a interface da Pokedex
def criar_interface_pokedex():
    pygame.init()

    largura_tela = 800
    altura_tela = 600
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption('Pokédex')

    fonte = pygame.font.SysFont('Arial', 24)
    cor_branca = (255, 255, 255)
    cor_preto = (0, 0, 0)
    cor_vermelha = (255, 0, 0)

    nome_pokemon = ''
    executando = True
    mostrar_informacoes = False
    tempo_exibicao = 5000  # Tempo de exibição das informações em milissegundos
    inicio_exibicao = 0
    mensagem_final = ""

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nome_pokemon.strip():
                        mensagem_final = executar_consulta_pokemon(nome_pokemon.strip().lower())
                    else:
                        nome_pokemon = random.choice(POKEMONS_ALEATORIOS)
                        mensagem_final = executar_consulta_pokemon(nome_pokemon)
                    nome_pokemon = ''  # Limpa o campo de entrada após a consulta
                    mostrar_informacoes = True
                    inicio_exibicao = pygame.time.get_ticks()  # Tempo atual
                elif evento.key == pygame.K_BACKSPACE:
                    nome_pokemon = nome_pokemon[:-1]
                else:
                    nome_pokemon += evento.unicode

        tela.fill(cor_preto)
        texto_prompt = fonte.render('Digite o nome do Pokémon ou pressione Enter para um aleatório:', True, cor_branca)
        retangulo_prompt = texto_prompt.get_rect()
        retangulo_prompt.midtop = (largura_tela // 2, 10)
        tela.blit(texto_prompt, retangulo_prompt)

        texto_digitado = fonte.render(nome_pokemon, True, cor_branca)
        retangulo_digitado = texto_digitado.get_rect()
        retangulo_digitado.midtop = (largura_tela // 2, retangulo_prompt.height + 20)
        tela.blit(texto_digitado, retangulo_digitado)

        if mostrar_informacoes:
            linhas_mensagem = mensagem_final.split('\n')
            for i, linha in enumerate(linhas_mensagem):
                texto_informacoes = fonte.render(linha, True, cor_branca)
                retangulo_informacoes = texto_informacoes.get_rect()
                retangulo_informacoes.midtop = (largura_tela // 2, retangulo_prompt.height + 60 + (i * 30))
                tela.blit(texto_informacoes, retangulo_informacoes)

            if pygame.time.get_ticks() - inicio_exibicao > tempo_exibicao:
                mostrar_informacoes = False

        pygame.display.flip()

    pygame.quit()


# Função principal para executar a consulta do Pokémon
def executar_consulta_pokemon(nome_pokemon):
    log = configurar_logger()

    try:
        conexao, cursor = criar_bd()
        if not conexao or not cursor:
            log.error("Não foi possível conectar ao banco de dados.")
            return "Erro de conexão com o banco de dados."

        log.info(f"Consultando dados do Pokémon: {nome_pokemon}")

        # Consultar banco de dados
        pokemon_bd = consultar_bd(cursor, nome_pokemon)

        if pokemon_bd:
            log.info(f"Dados do Pokémon {nome_pokemon} encontrados no banco de dados.")
            altura, peso, hp, attack, defense, speed, habilidades, tipos = pokemon_bd[2:]

            mensagem_final = f"{EMOJIS_POKEMON.get(nome_pokemon, '')} {nome_pokemon.capitalize()} - Altura: {altura:.2f}m, Peso: {peso:.2f}kg\nAtributos: HP: {hp}, Ataque: {attack}, Defesa: {defense}, Velocidade: {speed}\nHabilidades: {habilidades}, Tipos: {tipos}"
            alerta(mensagem_final, 'info')
            return mensagem_final

        else:
            log.info(f"Dados do Pokémon {nome_pokemon} não encontrados no banco de dados. Consultando API...")

            # Consultar API
            dados_pokemon = obter_dados_pokemon(nome_pokemon)

            if dados_pokemon:
                log.info(f"Dados do Pokémon {nome_pokemon} obtidos da API. Inserindo no banco de dados...")
                inserir_dados(conexao, cursor, dados_pokemon)

                atributos_traduzidos = traduzir_atributos(dados_pokemon['stats'])
                habilidades_traduzidas = traduzir_habilidades(dados_pokemon['abilities'])
                tipos_traduzidos = traduzir_tipos(dados_pokemon['types'])
                peso = dados_pokemon.get('weight', 0) / 10
                altura = dados_pokemon.get('height', 0) / 10

                mensagem_final = f"{EMOJIS_POKEMON.get(nome_pokemon, '')} {nome_pokemon.capitalize()} - Altura: {altura:.2f}m, Peso: {peso:.2f}kg\nAtributos: {', '.join(atributos_traduzidos)}\nHabilidades: {', '.join(habilidades_traduzidas)}, Tipos: {', '.join(tipos_traduzidos)}"
                alerta(mensagem_final, 'info')
                return mensagem_final

            else:
                mensagem_erro = f"Não foi possível encontrar o Pokémon {nome_pokemon} na API ou no banco de dados."
                log.error(mensagem_erro)
                return mensagem_erro

    except Exception as e:
        mensagem_erro = f"Ocorreu um erro na execução da automação: {e}"
        log.error(mensagem_erro)
        return mensagem_erro

    finally:
        if conexao:
            conexao.close()


# Função principal
def main():
    criar_interface_pokedex()

if __name__ == "__main__":
    main()
