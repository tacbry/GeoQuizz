import pytest
import engine



def test_charger_country_data_return_list():
    data = engine.load_country_data()
    assert type(data) == list


@pytest.mark.parametrize("path",[" "])
def test_charger_country_data_raise_exception(path):
    with pytest.raises(FileNotFoundError,match="aucun fichier trouvé/utilisation du fichier par défaut"):
        engine.load_country_data(path)

