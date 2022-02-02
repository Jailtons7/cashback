# Cashback

Uma API para cadastrar compras de revendedores e acompanhar o retorno de cashback de cada um.

## 1. Sobre a API

Para o desenvolvimento da API foi usado o microframework 
[Flask](https://flask.palletsprojects.com/en/2.0.x/) 
devido à sua fácil integração com pacotes de terceiros, como 
[flask-jwt-extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
que está sendo usado para autenticação de usuários e 
[flask-mongoengine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/)
que está sendo usado para conectar ao MongoDB.

## 2. Rodando a API

>Para o correto funcionamento dos comandos abaixo é aconselhável ter `python >= 3.8`, estar com o terminal na raiz do 
> projeto e [criar e ativar um ambiente virtual.](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)

#### 2.1. Variáveis de ambiente e conexão com o MongoDB
Para a conexão com o `MongoDB` será preciso uma [Cluster no Atlas](https://docs.atlas.mongodb.com/getting-started/).
Crie um arquivo `.env` e copie o conteúdo do arquivo `local.env` para ele. 
Será preciso fornecer os seus valores para o banco que será usado, `DB`, e as credenciais: `DB_USER` e `DB_PASSWORD`

#### 2.2. Instalando as dependências
Para instalar as dependências python basta rodar o comando a seguir:

```shell
pip install -r requirements.txt
```

#### 2.3. Servindo a aplicação
Para disponibilizar a aplicação execute os comandos a seguir:
```shell
export FLASK_APP=main.py  # Informa o arquivo que roda a aplicação
```
e finalmente
```shell
flask run
```
## 3. Testes

A aplicação conta com testes unitários e de integração para rodá-los use os comandos a seguir:

```shell
pytest tests/unit  # testes unitários
```

```shell
pytest tests/integrations  # testes de integração
```

```shell
pytest  # testes unitários e de integração
```

## 4. Exemplos de chamada

#### 4.1. Autenticação

##### 4.1.1. Criar usuário
```shell
POST '/authentication/users'
# headers
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}
# data
{
  "nome": "name",
  "cpf": "00000000000",
  "email": "name@example.com",
  "password": "my-secret.@"
}
```
A resposta deve ter status code 201, Created, com os dados do usuário criado .
##### 4.1.2. Token de Acesso
```shell
POST '/authentication/create-token'
# headers
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}
# data
{
  "email": 'name@example.com',
  "password": 'my-secret.@'
}
```
A resposta deve ter status code 201 created com o token de acesso.

#### 4.2. Compras
##### 4.2.1 Registrar uma nova compra
```shell
POST '/purchases'
# headers
{
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer " + access_token
}
# data
{
    "code": "1",
    "cpf": "00000000000",
    "value": 750.25,
    "date": "2022-01-28"
}
```
A resposta deve ter status code 201 created com os dados da compra adicionada.
##### 4.2.2. Recuperar as compras
```shell
GET '/purchases'
# headers
{
    "Authorization": "Bearer " + access_token
}
```
A resposta deve ter status code 200 success com as compras registradas.
