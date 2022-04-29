from database import proxy, schemas


def user_proxy_data():
    return (
        proxy.UserProxy,
        schemas.User,
        {
            'username': 'username',
            'password': 'password',
        },
    )
