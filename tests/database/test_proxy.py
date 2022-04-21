import pytest

from database import proxy


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        (
            proxy.UserProxy,
            {
                'username': 'username',
                'password': 'password',
            },
        ),
    ],
)
def test_proxy_create(prepare_db_env, model, parameters):
    model.create(**parameters)
    assert model.get(**parameters) is not None
