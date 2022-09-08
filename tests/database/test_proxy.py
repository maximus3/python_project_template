# pylint: disable=unused-argument
import uuid

import pytest


@pytest.mark.parametrize(
    'created_model',
    ['created_dps_user'],
)
def test_proxy_eq_error(request, migrated_postgres, created_model):
    created_model = request.getfixturevalue(created_model)
    assert not created_model.proxy.get(**created_model.data.dict()) == 1


@pytest.mark.parametrize(
    'dps_model',
    ['dps_user'],
)
def test_proxy_create_error_no_such_param(
    request, migrated_postgres, dps_model
):
    dps_model = request.getfixturevalue(dps_model)
    with pytest.raises(TypeError):
        dps_model.proxy.create(no_param='no_param')


@pytest.mark.parametrize(
    'dps_model',
    [
        'dps_user',
    ],
)
def test_proxy_create(request, migrated_postgres, dps_model):
    dps_model = request.getfixturevalue(dps_model)
    dps_model.proxy.create(**dps_model.data.dict())
    assert dps_model.proxy.get(**dps_model.data.dict()) is not None


@pytest.mark.parametrize(
    'dps_model',
    [
        'dps_user',
    ],
)
def test_proxy_get_or_create(request, migrated_postgres, dps_model):
    dps_model = request.getfixturevalue(dps_model)
    assert dps_model.proxy.get_or_create(**dps_model.data.dict()) is not None
    assert dps_model.proxy.get(**dps_model.data.dict()) is not None


@pytest.mark.parametrize(
    'created_model',
    [
        'created_dps_user',
    ],
)
def test_proxy_get_or_create_exists(request, migrated_postgres, created_model):
    created_model = request.getfixturevalue(created_model)
    assert (
        created_model.proxy.get_or_create(**created_model.data.dict())
        is not None
    )


@pytest.mark.parametrize(
    'dps_model',
    [
        'dps_user',
    ],
)
def test_proxy_get_none(request, migrated_postgres, dps_model):
    dps_model = request.getfixturevalue(dps_model)
    assert dps_model.proxy.get(**dps_model.data.dict()) is None


@pytest.mark.parametrize(
    'created_model',
    [
        'created_dps_user',
    ],
)
def test_proxy_get_expect(request, migrated_postgres, created_model):
    created_model = request.getfixturevalue(created_model)
    assert created_model.proxy.get_expect(**created_model.data.dict())


@pytest.mark.parametrize(
    'created_model',
    [
        'created_dps_user',
    ],
)
def test_proxy_get_model(request, migrated_postgres, create_session, created_model):
    created_model = request.getfixturevalue(created_model)
    assert created_model.proxy.get_model(**created_model.data.dict())
    with create_session() as session:
        assert created_model.proxy(
            created_model.proxy.get_model(**created_model.data.dict(), session=session)
        ) == created_model.proxy.get_expect(**created_model.data.dict())


@pytest.mark.parametrize(
    'created_model',
    [
        'created_dps_user',
    ],
)
def test_proxy_get_schema_model(request, migrated_postgres, create_session, created_model):
    created_model = request.getfixturevalue(created_model)
    assert created_model.proxy.get_schema_model(**created_model.data.dict())
    with create_session() as session:
        assert created_model.proxy.get_schema_model(
            **created_model.data.dict()
        ) == created_model.schema.from_orm(
            created_model.proxy.get_model(**created_model.data.dict(), session=session)
        )


@pytest.mark.parametrize(
    'created_model',
    [
        'created_dps_user',
    ],
)
def test_proxy_get_all(request, migrated_postgres, created_model):
    created_model = request.getfixturevalue(created_model)
    assert created_model.proxy.get_all(**created_model.data.dict()) == [
        created_model.proxy.get_expect(**created_model.data.dict())
    ]


@pytest.mark.parametrize(
    'created_model',
    [
        'created_dps_user',
    ],
)
def test_proxy_update_none(request, migrated_postgres, created_model):
    created_model = request.getfixturevalue(created_model)
    proxy_model = created_model.proxy.get(**created_model.data.dict())
    proxy_model.id = uuid.uuid4()
    assert proxy_model.update(**created_model.data.dict()) is None


@pytest.mark.parametrize(
    'created_model',
    [
        'created_dps_user',
    ],
)
def test_proxy_update_no_attr(request, migrated_postgres, created_model):
    created_model = request.getfixturevalue(created_model)
    proxy_model = created_model.proxy.get(**created_model.data.dict())
    assert (
        proxy_model.update(
            **created_model.data.dict(), no_such_parameter='no_such_parameter'
        )
        is None
    )


@pytest.mark.parametrize(
    'created_model',
    [
        'created_dps_user',
    ],
)
def test_proxy_update(request, migrated_postgres, created_model):
    created_model = request.getfixturevalue(created_model)
    assert created_model.proxy.get(**created_model.data.dict()).update(
        **created_model.data.dict()
    ) == created_model.proxy.get(**created_model.data.dict())
