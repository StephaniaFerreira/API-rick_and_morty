from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from models.models import Personagem, Dublador, Episodio
import requests
from database import get_db
import config

ID_SERIE = 60625 #ID DA SERIE RICK AND MORTY NA API TMDB

def importar():
    personagens = consultar_personagens()
    dublador = consultar_dubladores()
    episodios = consultar_episodios()
    response = popular_BD(personagens, dublador, episodios)
    return response

def listar_dubladores():
    db = get_db()
    dubladores = db.query(Dublador.name, Dublador.id_dublador ,Dublador.character).filter_by(serie = ID_SERIE).order_by(Dublador.name).all()
    response = []
    for item in dubladores:
        nome_dublador = item[0]
        id_dublador = item[1]
        nome_personagem = item[2]

        p = db.query(Personagem).filter(Personagem.name.contains(" ".join(nome_personagem.split()[:2]))).all()

        d = {'name': nome_dublador,'id': id_dublador, 'personagem': p}

        response.append(d)

    return response

def listar_episodios(idDublador):
    db = get_db()

    nome_personagem = db.query(Dublador.character).filter_by(id_dublador = idDublador).first()
    id_personagem = db.query(Personagem.id_personagem).filter(Personagem.name.contains(" ".join(nome_personagem[0].split()[:2]))).first()
    epi = db.query(Episodio).filter_by(id_personagem = id_personagem[0]).all()

    return epi


def consultar_personagens():
    url = 'https://rickandmortyapi.com/api/character'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao consultar Personagens.'
        )
    
    return data

def consultar_dubladores():
    url = f'https://api.themoviedb.org/3/tv/{ID_SERIE}/credits'
    params = {'api_key': config.API_KEY, 'language': 'pt-BR', 'page':1}
    response = requests.get(url, params)
    data = {}
    if response.status_code == 200:
        data = response.json()
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao consultar Dubladores.'
        )
    
    return data

def consultar_episodios():
    url = f'https://api.themoviedb.org/3/tv/{ID_SERIE}'
    params = {'api_key': config.API_KEY, 'language': 'pt-BR', 'page':1}
    response = requests.get(url, params)
    episodios = []
    if response.status_code == 200:
        temporadas = int(response.json()['number_of_seasons'])
        for ID_SEASON in range(1,temporadas+1):
            url = f'https://api.themoviedb.org/3/tv/{ID_SERIE}/season/{ID_SEASON}'
            params = {'api_key': config.API_KEY, 'language': 'pt-BR', 'page':1}
            response = requests.get(url, params)
            episodios.extend(response.json()['episodes']) 
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro ao consultar Episodios.'
        )
    data = {}
    for e in episodios:
        chave = (e['season_number'],e['episode_number'])
        data[chave] = e
    
    return data

def popular_BD(personagens, dublador, episodios):
    personagens_inserir = []
    dublador_inserir = []
    episodios_inserir = []
    db = get_db()

    for result in personagens["results"]:
        p = Personagem(
            id_personagem = result['id'],
            name = result['name'],
            status = result['status'],
            species = result['species'],
            gender = result['gender'],
            location = result['location']['name']
        )
        personagens_inserir.append(p)

        for key in episodios:
            e = Episodio(
                id_externo = episodios[key]['id'],
                episode_number = episodios[key]['episode_number'],
                name = episodios[key]['name'],
                overview = episodios[key]['overview'],
                runtime = episodios[key]['runtime'],
                id_personagem = result['id'],
                season = episodios[key]['season_number']
            )
            episodios_inserir.append(e)

    db.add_all(personagens_inserir)
    db.add_all(episodios_inserir)

    for result in dublador['cast']:
        c = Dublador(
            id_dublador= result['id'],
            name = result['name'],
            character = result['character'],
            serie = ID_SERIE
        )
        dublador_inserir.append(c)

    
    db.add_all(dublador_inserir)

    try:
        db.commit()
    except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Erro ao inserir no banco: {str(e)}'
            )
    db.close()
    return 'Informações inseridas com sucesso!'