from database import proxy


def user_proxy_data():
    return (
        proxy.UserProxy,
        {
            'username': 'username',
            'password': 'password',
        },
    )
