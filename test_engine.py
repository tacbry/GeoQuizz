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


@pytest.mark.parametrize(
    "continent",["America"])
def test_get_filtered_countries(continent):
    ...
def test_check_capital_return_true_if_good_answer():
    ...
def test_check_answer_return_true_if_good_answer():
    ...#tester des flag et capitale



