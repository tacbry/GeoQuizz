import pytest
import engine



def test_charger_country_data_return_list():
    data = engine.load_country_data()
    assert type(data) == list


@pytest.mark.parametrize("path",[" "])
def test_charger_country_data_raise_exception(path):
    with pytest.raises(FileNotFoundError,match="aucun fichier trouvé/utilisation du fichier par défaut"):
        engine.load_country_data(path)


def test_get_name():
    assert engine.get_name('AD') == 'Andorra'

def test_get_capital():
    assert engine.get_capitals('AD') == 'Andorra la Vella'



#un test qui test tous les iso?

