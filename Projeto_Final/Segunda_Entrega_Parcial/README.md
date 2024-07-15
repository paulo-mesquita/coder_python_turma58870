# Documentação - Projeto Final (Projeto PokéAPI)

## Configuração do Ambiente Virtual e Criação do Arquivo `requirements.txt`

Este script Python automatiza a configuração de um ambiente virtual e a geração do arquivo `requirements.txt`, listando as bibliotecas necessárias para o seu projeto, juntamente com suas versões específicas. Executar este script é essencial antes de prosseguir com o desenvolvimento, garantindo um ambiente consistente e controlado para suas dependências.

## Funcionalidades

1. **Verificação e Criação do Ambiente Virtual:**
   - Verifica se o ambiente virtual especificado ("projeto_final_coderhouse_python311") já existe.
   - Se não existir, cria um novo ambiente virtual com todas as configurações necessárias.

2. **Instalação Automática de Bibliotecas:**
   - Verifica se as bibliotecas essenciais estão instaladas ("requests", "plyer", "pygame", "logging").
   - Instala automaticamente qualquer biblioteca ausente utilizando o gerenciador de pacotes `pip`.

3. **Registro das Versões das Bibliotecas:**
   - Obtém as versões específicas de cada biblioteca instalada, garantindo consistência no desenvolvimento.

4. **Geração do Arquivo `requirements.txt`:**
   - Escreve no arquivo `requirements.txt` todas as bibliotecas instaladas juntamente com suas versões, no formato `biblioteca==versao`.
   - Garante que o arquivo resultante seja claro e sem quebras de linha extras entre as entradas.

## Como Utilizar

1. **Execução do Script:**
   - Execute o script `setup_virtualenv_and_requirements.py` no seu terminal ou IDE, dentro do ambiente virtual desejado.

2. **Criação do Arquivo `requirements.txt`:**
   - Após a execução bem-sucedida, o arquivo `requirements.txt` será gerado no diretório atual.
   - Este arquivo é essencial para gerenciar e replicar as dependências do projeto em diferentes ambientes de desenvolvimento ou produção.

# Projeto PokéAPI - Informações de Pokémons para Idosos

Este projeto utiliza a PokéAPI para fornecer informações detalhadas sobre Pokémons, visando oferecer entretenimento e curiosidades sobre essas criaturas fictícias. A aplicação é voltada para idosos, buscando garantir qualidade de vida e lazer através do conhecimento e diversão proporcionados pelos Pokémons.

## Pré-requisitos

- Python 3.x instalado.
- Bibliotecas necessárias:
  - requests
  - plyer
  - pygame
  - logging

## Estrutura de Pastas

- O projeto assume a existência de um diretório 'audio' na mesma pasta onde está sendo executado.
- Dentro de 'audio', é necessário ter um arquivo de áudio 'quem_e_esse_pokemon.mp3' para os efeitos sonoros da Pokédex.

## Funcionalidades

1. **Consulta de Informações de Pokémon:**
   - O usuário pode inserir o nome de um Pokémon ou pressionar Enter para selecionar um Pokémon aleatório da lista pré-definida.
   - O script consulta primeiro o banco de dados local para verificar se as informações do Pokémon já estão disponíveis.
   - Caso não encontre no banco de dados, consulta a PokéAPI para obter os dados do Pokémon selecionado.

2. **Formatação e Apresentação de Dados:**
   - Os dados são formatados e traduzidos para exibir informações como atributos (HP, Ataque, Defesa, Velocidade), habilidades e tipos do Pokémon.

3. **Notificação com Informações do Pokémon:**
   - Uma notificação é exibida com as informações do Pokémon, acompanhada de um som característico do anime para reconhecimento auditivo.

## Detalhes Técnicos

- As traduções são realizadas utilizando dicionários pré-definidos para habilidades, tipos e atributos. Caso uma tradução não esteja disponível, o nome original em inglês será utilizado.
- O projeto utiliza módulos para reprodução de áudio (pygame) e exibição de notificações (plyer), garantindo uma experiência interativa e acessível.

## Base de Dados e Logs

- **Base de Dados:** O projeto mantém uma base de dados local (arquivo .db) para armazenar as informações dos Pokémons consultados, permitindo consultas rápidas e offline.
- **Logs:** Todas as interações e processos do código são registrados em um arquivo de log (`log.txt`), fornecendo um registro detalhado de todas as consultas à PokéAPI, consultas ao banco de dados e notificações exibidas.

## Garantia de Qualidade

- O código foi desenvolvido para ser robusto e capaz de lidar com situações de erro, como falhas na conexão com a PokéAPI ou requisições mal-sucedidas. Caso ocorra algum problema, uma notificação de erro é exibida para o usuário.
- A interface de notificação é projetada para ser visualmente clara e fácil de entender, ideal para usuários idosos.

## Autores e Curso

- **Autores:** Paulo Mesquita, Fernando Loriggio, João Alves e Nivaldo Junior
- **Curso:** Python CODERHOUSE - Turma 58870
- **Data de Criação:** 08/07/2024
