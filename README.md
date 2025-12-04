O TaferasApp é uma aplicação de desktop/multiplataforma desenvolvida em Python com a biblioteca Kivy para a interface gráfica (GUI). Ele permite a um prestador de serviços, como o Roger Barreto, registrar, rastrear e gerenciar tarefas de clientes, incluindo detalhes como endereço, tipo de serviço, valor de mão de obra e até mesmo anexar uma imagem como prova ou referência do trabalho.

O sistema utiliza o SQLite para armazenar todos os dados de forma local e persistente.

🌟 Funcionalidades Principais

Registro Detalhado: Adição de tarefas com descrição, nome e endereço do cliente, tipo de serviço e valor da mão de obra.

Gestão de Prazos: Campos dedicados para registrar a data de execução e a data de conclusão do serviço.

Anexo de Imagens: Suporte para carregar imagens a partir de um caminho local (utilizando a biblioteca PIL para redimensionamento e compressão) e armazená-las como BLOBs no banco de dados SQLite.

Listagem Dinâmica: Visualização em tempo real de todas as tarefas cadastradas, com a opção de exclusão.

Persistência de Dados: Todos os dados são salvos no arquivo tasks.db e carregados automaticamente ao iniciar o aplicativo.

🛠️ Tecnologias Utilizadas

Python 3: Linguagem principal de desenvolvimento.

Kivy: Framework para criação de interfaces gráficas multiplataforma.

SQLite3: Banco de dados leve e integrado, usado para armazenamento local dos dados das tarefas.

Pillow (PIL): Biblioteca utilizada para manipular (carregar, redimensionar e comprimir) as imagens antes de armazená-las no banco de dados, otimizando o desempenho do aplicativo.

io e datetime: Módulos padrão para manipulação de streams de bytes e validação de formatos de data.

⚙️ Instalação e Configuração

⚠️ AVISO IMPORTANTE SOBRE A INSTALAÇÃO DO KIVY:

O Kivy requer pacotes binários específicos (wheels) para funcionar no Windows, especialmente para as dependências como SDL2. Estas dependências geralmente não suportam as versões mais recentes do Python imediatamente.

O seu projeto exige que você utilize uma versão do Python que seja compatível com os binários do Kivy, como o Python 3.10 ou 3.11.

1. Requisitos

Certifique-se de ter uma versão compatível do Python (Recomendado: Python 3.11).

2. Instalação das Dependências

Para instalar as bibliotecas Kivy e Pillow (PIL), use o seguinte comando no terminal, aproveitando o repositório de binários do Kivy:
