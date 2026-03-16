import pytest
from _pytest.fixtures import fixture

import engine


@fixture
def get_engine():
    return engine.Engine()


def test_charger_country_data_return_list(get_engine):
    data = get_engine.load_country_data()
    assert type(data) == list


@pytest.mark.parametrize("path", [" "])
def test_charger_country_data_raise_exception(get_engine, path):
    with pytest.raises(
        FileNotFoundError,
        match="aucun fichier trouvé/utilisation du fichier par défaut",
    ):
        get_engine.load_country_data(path)


def test_get_name(get_engine):
    assert get_engine.get_name("AD") == "Andorra"


def test_get_capital(get_engine):
    assert get_engine.get_capital(iso="AD") == "Andorra la Vella"


@pytest.mark.parametrize("iso, ans,result", [
    ('AD', 'Andorra la Vella', True),
    ('DZ', 'Algiers', True),
    ('IT', ' ', False),
])
def test_check_capital_return_true_if_good_answer(get_engine, iso,ans, result):
    assert get_engine.check_capital(iso, ans) == result

@pytest.mark.parametrize("iso, ans,result", [
    ('AD', 'Andorra', True),
    ('DZ', 'Algieria', True),
    ('IT', ' ', False),
])
def test_check_flag_return_true_if_good_answer(get_engine, iso,ans, result):
    assert get_engine.check_flag(iso, ans) == result


@pytest.mark.parametrize("iso, ans,result, type_quizz", [
    ('AD', 'Andorra la Vella', True,"capitale" ),
    ('DZ', 'Algiers', True,"capitale" ),
    ('IT', ' ', False, "capitale"),
    ('AD', 'Andorra', True, "drapeau"),
    ('DZ', 'Algieria', True, "drapeau"),
    ('IT', ' ', False, "drapeau"),
])
def test_check_answer_return_true_if_good_answer(get_engine, iso,ans, result, type_quizz):
    assert get_engine.check_answer(type_quizz, iso, ans) == result

