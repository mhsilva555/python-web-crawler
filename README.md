# Google Maps Company Crawler

Este projeto é um sistema desenvolvido em **Python** e **Django** que utiliza **Selenium** para buscar informações de empresas no Google Maps com base em um segmento e cidade. Além dos dados básicos do Maps, o sistema visita o site das empresas encontradas para tentar capturar e-mails e links de redes sociais.

## Funcionalidades

- Busca por segmento (ex: "Pizzaria") e cidade (ex: "São Paulo").
- Extração de:
  - Nome da Empresa
  - Telefone
  - Website
  - E-mail (via scraping do site da empresa)
  - Redes Sociais (Facebook, Instagram, LinkedIn, etc.)
- Interface web simples para busca e visualização dos resultados.
- Exportação dos resultados para **CSV** e **XML**.
- Armazenamento histórico das buscas no banco de dados.

## Pré-requisitos

- **Python 3.8+** instalado.
- **Google Chrome** instalado (o Selenium utilizará o navegador para realizar as buscas).
- Conexão com a internet.

## Instalação e Configuração

Siga os passos abaixo para configurar o ambiente de desenvolvimento:

### 1. Clonar ou Acessar o Diretório do Projeto

Navegue até a pasta onde o projeto está localizado:

```bash
cd /caminho/para/o/projeto/crawler
```

### 2. Criar um Ambiente Virtual (Recomendado)

Crie e ative um ambiente virtual para isolar as dependências:

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual (Linux/Mac)
source venv/bin/activate

# Ativar o ambiente virtual (Windows)
venv\Scripts\activate
```

### 3. Instalar Dependências

Instale as bibliotecas necessárias listadas abaixo. Se você não tiver um arquivo `requirements.txt`, pode instalar manualmente:

```bash
pip install django selenium beautifulsoup4 webdriver-manager requests
```

### 4. Configurar o Banco de Dados

Execute as migrações do Django para criar as tabelas necessárias (SQLite por padrão):

```bash
python manage.py makemigrations search
python manage.py migrate
```

## Como Usar

1.  **Inicie o Servidor de Desenvolvimento**:

    ```bash
    python manage.py runserver
    ```

2.  **Acesse a Aplicação**:
    Abra o seu navegador e vá para: [http://127.0.0.1:8000](http://127.0.0.1:8000)

3.  **Realize uma Busca**:
    - Digite o segmento desejado (ex: "Advogados").
    - Digite a cidade (ex: "Rio de Janeiro").
    - Clique em "Buscar Systema".

    > **Nota**: O processo pode levar alguns minutos, pois o sistema abrirá um navegador em segundo plano (modo headless) para navegar no Google Maps e visitar os sites encontrados.

4.  **Visualize os Resultados**:
    Os resultados aparecerão em uma tabela contendo as informações coletadas.

## Solução de Problemas

- **Erro de Driver**: O `webdriver-manager` deve baixar automaticamente o ChromeDriver compatível. Se houver erro, certifique-se de que o Google Chrome está instalado corretamente no sistema.
- **Bloqueio do Google**: Se a busca retornar vazia repetidamente, o Google pode ter bloqueado temporariamente suas requisições automatizadas. Tente aguardar alguns minutos ou usar uma VPN.
- **Dependências**: Se houver erro na instalação do `psycopg2` ou outros pacotes de banco de dados, verifique se as dependências do sistema operacional (como `libpq-dev`) estão instaladas (embora este projeto use SQLite por padrão e não deva exigir isso).
