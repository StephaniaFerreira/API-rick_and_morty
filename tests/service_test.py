from services import service

def test_consultar_personagens():
    result = service.consultar_personagens()

    assert isinstance(result, dict)
    assert 'id' in result["results"][0]
    assert 'name' in result["results"][0]
    assert 'status' in result["results"][0]
    assert 'species' in result["results"][0]
    assert 'gender' in result["results"][0]
    assert 'location' in result["results"][0]

def test_consultar_dublador():
    result = service.consultar_dublador()

    assert isinstance(result, dict)
    assert 'id' in result['cast'][0]
    assert 'name' in result['cast'][0]
    assert 'character' in result['cast'][0]

def test_consultar_episodio():
    result = service.consultar_episodio()

    assert isinstance(result, dict)
    chave = (1,1)
    assert 'id' in result[chave]
    assert 'episode_number' in result[chave]
    assert 'name' in result[chave]
    assert 'overview' in result[chave]
    assert 'runtime' in result[chave]
    assert 'season_number' in result[chave]

