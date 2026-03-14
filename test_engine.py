import pytest
from _pytest.fixtures import fixture

import engine

@fixture
def get_engine():
    return engine.Engine()

def test_charger_country_data_return_list():
    data = engine.Engine.load_country_data()
    assert type(data) == list


@pytest.mark.parametrize("path",[" "])
def test_charger_country_data_raise_exception(path):
    with pytest.raises(FileNotFoundError,match="aucun fichier trouvé/utilisation du fichier par défaut"):
        engine.Engine.load_country_data(path)


def test_get_name(get_engine):
    assert get_engine.get_name('AD') == 'Andorra'

def test_get_capital():
    assert engine.Engine.get_capitals(iso = 'AD') == 'Andorra la Vella'


@pytest.mark.parametrize(
    "continent",["America"])
def test_get_filtered_countries(continent):
    ...
def test_check_capital_return_true_if_good_answer():
    ...
def test_check_answer_return_true_if_good_answer():
    ...#tester des flag et capitale



