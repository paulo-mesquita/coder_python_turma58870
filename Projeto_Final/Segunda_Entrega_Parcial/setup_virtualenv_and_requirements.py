"""
Script para configuração e execução do ambiente virtual e do projeto final da Pokédex.

Este script automatiza a configuração do ambiente virtual, instalação das bibliotecas
necessárias, criação do arquivo requirements.txt e execução do projeto final da Pokédex.

Ele realiza as seguintes etapas:
1. Criação de um ambiente virtual específico (`projeto_final_coderhouse_python311`).
2. Instalação das bibliotecas necessárias para o projeto (requests, plyer, pygame, logging).
3. Criação do arquivo requirements.txt contendo as versões das bibliotecas instaladas.
4. Execução do projeto final da Pokédex que gerencia dados de Pokémon, consultando inicialmente
   um banco de dados local e, se necessário, a API para informações atualizadas.

O arquivo de log será criado para registrar detalhes das operações realizadas.

Nota: Certifique-se de ter o Python e as ferramentas necessárias instaladas no ambiente de execução.
"""

import os
import subprocess
import venv

def criar_ambiente_virtual(venv_name):
    """
    Cria um ambiente virtual se ele não existir.

    Args:
        venv_name (str): Nome do ambiente virtual a ser criado.
    
    Returns:
        str: Caminho para o ambiente virtual criado.
    """
    venv_path = os.path.join(os.getcwd(), venv_name)

    if not os.path.exists(venv_path):
        venv.create(venv_path, with_pip=True, prompt=venv_name)

    return venv_path

def instalar_bibliotecas(venv_path, libs):
    """
    Instala bibliotecas no ambiente virtual especificado.

    Args:
        venv_path (str): Caminho para o ambiente virtual.
        libs (list): Lista de strings com os nomes das bibliotecas a serem instaladas.
    
    Returns:
        dict: Dicionário com as versões das bibliotecas instaladas.
    """
    if os.name == 'nt':
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_exe = os.path.join(venv_path, "bin", "python")

    versions = {}
    for lib in libs:
        try:
            subprocess.check_call([python_exe, '-c', f'import {lib}'])
            versao = subprocess.check_output([python_exe, '-m', 'pip', 'show', lib]).decode('utf-8').split('Version: ')[1].split('\n')[0]
            print(f'{lib} ({versao}) já está instalada')
        except subprocess.CalledProcessError:
            print(f'{lib} não está instalada. Instalando...')
            subprocess.check_call([python_exe, '-m', 'pip', 'install', lib])
            versao = subprocess.check_output([python_exe, '-m', 'pip', 'show', lib]).decode('utf-8').split('Version: ')[1].split('\n')[0]
        versions[lib] = versao

    return versions

def criar_requirements_txt(versions):
    """
    Cria o arquivo requirements.txt com as versões das bibliotecas instaladas.

    Args:
        versions (dict): Dicionário contendo as versões das bibliotecas instaladas.
    """
    req_file_path = os.path.join(os.getcwd(), "requirements.txt")

    with open(req_file_path, "w") as req_file:
        req_file.write("\n".join([f"{lib}=={versao}" for lib, versao in versions.items()]))

    print("Arquivo requirements.txt criado com sucesso!")

def executar_projeto_final():
    """
    Executa o projeto final da Pokédex que gerencia dados de Pokémon.
    """
    try:
        subprocess.check_call(["python", "pokedex_database_manager_V2.py"])
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o projeto final da Pokédex: {e}")

def main():
    print(__doc__.strip())  # Exibe o texto de introdução do script

    # Nome do ambiente virtual
    venv_name = "projeto_final_coderhouse_python311"

    # Criar o ambiente virtual se não existir
    venv_path = criar_ambiente_virtual(venv_name)

    # Bibliotecas a serem instaladas
    libs = ["requests", "plyer", "pygame", "logging"]

    # Instalar as bibliotecas no ambiente virtual
    versions = instalar_bibliotecas(venv_path, libs)

    # Criar o arquivo requirements.txt com as versões instaladas
    criar_requirements_txt(versions)

    # Exibe linhas em branco para separar as mensagens de configuração das mensagens do projeto final
    print("\n\n\n\n\n\n\n\n\n\n")

    # Executar o projeto final da Pokédex
    executar_projeto_final()

if __name__ == "__main__":
    main()
