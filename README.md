# API-RICK_AND_MORTY

API implementada para teste técnico

## Tecnologias Utilizadas

- python (versão = 3.8.10)
- fastapi (versão = 0.116.1)
- requests (versão = 2.22.0)
- sqlalchemy (2.0.43p)
- pytest (versão = 8.3.5)
- SQLite (versão = 3.31.1)
- Pydantic (versão = 2.10.6)
- VS Code
- uvicorn (versão 0.33.0)

## Organização da Aplicação

A API é organizada em:
- Controller: responsável por receber as requisições, chamar os serviços adequados e devolver a resposta, ou seja, é a interface da API.
- Service:  responsável pela lógica de negócio da aplicação.
- Model: representa a estrutura de dados
- Pasta test: contém o teste unitário.

## Executar Aplicação
 - Verifique se todas as dependências estão na máquina.
 - Na raiz do projeto abra o terminal e execute:
```bash
    uvicorn main:app --reload
```
 - Abra no navegador:
 ```bash
    http://127.0.0.1:8000/docs
 ```