import traceback
from credentials import api_id, api_hash, phone_number
from updates_handler import ClientUpdatesTelegramClient
# from telethon.network.connection import ConnectionMode


def load_settings(path='api/settings'):
    """Loads the user settings located under `api/`"""
    result = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            value_pair = line.split('=')
            left = value_pair[0].strip()
            right = value_pair[1].strip()
            if right.isnumeric():
                result[left] = int(right)
            else:
                result[left] = right

    return result


if __name__ == '__main__':
    # Load the settings and initialize the client
    # settings = load_settings()
    # kwargs = {'connection_mode': ConnectionMode.TCP_FULL}
    kwargs = {}
    """if settings.get('socks_proxy'):
        import socks  # $ pip install pysocks
        host, port = settings['socks_proxy'].split(':')
        kwargs = dict(proxy=(socks.SOCKS5, host, int(port)))"""

    client = ClientUpdatesTelegramClient(
        session_user_id='userupdates',
        user_phone=phone_number,
        api_id=api_id,
        api_hash=api_hash,
        # update_workers=4,  # More - faster??
        **kwargs)

    print('Initialization done!')

    try:
        client.run()

    except Exception as e:
        print('Unexpected error ({}): {} at\n{}'.format(
            type(e), e, traceback.format_exc()))
