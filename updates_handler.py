import time
import traceback
from getpass import getpass
from pprint import pprint
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import UpdateShort, UpdatesTg


def bytes_to_string(byte_count):
    """Converts a byte count to a string (in KB, MB...)"""
    suffix_index = 0
    while byte_count >= 1024:
        byte_count /= 1024
        suffix_index += 1

    return '{:.2f}{}'.format(byte_count,
                             [' bytes', 'KB', 'MB', 'GB', 'TB'][suffix_index])


class ClientUpdatesTelegramClient(TelegramClient):
    def __init__(self, session_user_id, user_phone, api_id, api_hash, proxy=None):
        print('Initializing interactive example...')
        super().__init__(session_user_id, api_id, api_hash, proxy)
        # super().__init__(session_user_id, api_id, api_hash, connection_mode, proxy, update_workers)

        ### --- Maybe we will need it later --- ###
        """# Store all the found media in memory here,
        # so it can be downloaded if the user wants
        self.found_media = set()"""

        print('Connecting to Telegram servers...')
        if not self.connect():
            print('Initial connection failed. Retrying...')
            if not self.connect():
                print('Could not connect to Telegram servers.')
                return

        # Then, ensure we're authorized and have access
        if not self.is_user_authorized():
            print('First run. Sending code request...')
            self.send_code_request(user_phone)

            self_user = None
            while self_user is None:
                code = input('Enter the code you just received: ')
                try:
                    self_user = self.sign_in(user_phone, code)

                # Two-step verification may be enabled
                except SessionPasswordNeededError:
                    pw = getpass('Two step verification is enabled. '
                                 'Please enter your password: ')

                    self_user = self.sign_in(password=pw)

    def run(self):
        # Listen for updates
        self.add_update_handler(self.update_handler)

        # Enter a while loop to get updates as long as the user wants
        while True:
            pass

    ### --- Maybe we will need it later --- ###
    """def download_media(self, media_id):
        try:
            # The user may have entered a non-integer string!
            msg_media_id = int(media_id)

            # Search the message ID
            for msg in self.found_media:
                if msg.id == msg_media_id:
                    # Let the output be the message ID
                    output = str('usermedia/{}'.format(msg_media_id))
                    print('Downloading media with name {}...'.format(output))
                    output = self.download_msg_media(
                        msg.media,
                        file=output,
                        progress_callback=self.download_progress_callback)
                    print('Media downloaded to {}!'.format(output))

        except ValueError:
            print('Invalid media ID given!')

    @staticmethod
    def download_progress_callback(downloaded_bytes, total_bytes):
        InteractiveTelegramClient.print_progress('Downloaded',
                                                 downloaded_bytes, total_bytes)

    @staticmethod
    def upload_progress_callback(uploaded_bytes, total_bytes):
        InteractiveTelegramClient.print_progress('Uploaded', uploaded_bytes,
                                                 total_bytes)

    @staticmethod
    def print_progress(progress_type, downloaded_bytes, total_bytes):
        print('{} {} out of {} ({:.2%})'.format(progress_type, bytes_to_string(
            downloaded_bytes), bytes_to_string(total_bytes), downloaded_bytes /
                                                total_bytes))"""

    @staticmethod
    def update_handler(update_object):
        try:
            update = convert_update(update_object.to_dict(), update_object)
            if update:
                ### Do ANYTHING you want with update there ###
                pprint(update)
        except:
            print('Error: {}'.format(traceback.format_exc()))
            pprint(update_object.to_dict())


def convert_time(date):
    return int(time.mktime(date.timetuple()))


def get_user_by_id(users, from_id):
    for user in users:
        if user['id'] == from_id:
            return user
    return {}


def get_chat_by_id(chats, to_id):
    for chat in chats:
        if chat['id'] == to_id:
            return chat
    return {}


def form_user_info(users, from_id):
    current_user = get_user_by_id(users, from_id)
    return {'id': current_user.get('id'), 'first_name': current_user.get('first_name'),
            'username': current_user.get('username'),
            'last_name': current_user.get('last_name'),
            'language_code': current_user.get(
                'lang_code'),  # seems like 'language_code' is always 'None' for bots in MTProto
            'is_bot': current_user.get('bot')}


def form_chat_info(chats, to_id):
    all_members_are_administrators = False
    if isinstance(to_id, int):
        current_chat = get_chat_by_id(chats, to_id)
    else:
        current_chat = get_chat_by_id(chats, list(to_id.values())[0])
    chat_id = current_chat['id']
    if current_chat.get('megagroup'):
        chat_id = int('-100' + str(chat_id))
        chat_type = 'supergroup'
    elif current_chat.get('broadcast'):
        chat_id = int('-100' + str(chat_id))
        chat_type = 'channel'
    else:
        chat_type = 'group'
        if current_chat.get('democracy'):
            all_members_are_administrators = True
            chat_id = -1 * current_chat['id']

    return {'type': chat_type, 'last_name': current_chat.get('last_name'), 'first_name': current_chat.get('first_name'),
            'username': current_chat.get('username'),
            'id': chat_id, 'title': current_chat.get('title'),
            'all_members_are_administrators': all_members_are_administrators}


def convert_update(update, update_type):
    res = {'mtproto': True, 'content_type': None, 'message_id': None,
           'from_user': {'id': None, 'first_name': None, 'username': None, 'last_name': None,
                         'language_code': None}, 'date': None,
           'chat': {'type': None, 'last_name': None, 'first_name': None, 'username': None,
                    'id': None, 'title': None, 'all_members_are_administrators': None},
           'forward_from_chat': None,
           'forward_from': None, 'forward_from_message_id': None, 'forward_date': None,
           'reply_to_message': None, 'edit_date': None,
           'text': None,
           'entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None,
           'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None,
           'venue': None,
           'new_chat_member': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None,
           'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None,
           'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None,
           'pinned_message': None, 'invoice': None, 'successful_payment': None}
    if isinstance(update_type, UpdatesTg):
        for i in range(len(update['updates'])):

            if len(update['users']):
                anonymous = False
            else:
                anonymous = True

            is_bot = False

            if not anonymous:
                for usr in update['users']:
                    if usr['bot']:
                        is_bot = True
                        break

            if update['updates'][i].get('message') and (update['updates'][i]['message'].get('via_bot_id') or is_bot):
                #  User/Bot info

                if not anonymous:
                    res['from_user'] = form_user_info(update['users'], update['updates'][i]['message']['from_id'])
                if update['updates'][i]['message'].get('via_bot_id'):
                    res['via_bot'] = form_user_info(update['users'], update['updates'][i]['message']['via_bot_id'])
                # Chat info
                if update['chats']:
                    res['chat'] = form_chat_info(update['chats'], update['updates'][i]['message']['to_id'])
                else:
                    return

                # Message Info
                res['message_id'] = update['updates'][i]['message']['id']
                res['date'] = convert_time(update['updates'][i]['message']['date'])

                if update['updates'][i]['message'].get('fwd_from'):
                    res['forward_date'] = convert_time(update['updates'][i]['message']['fwd_from']['date'])
                    res['forward_from'] = form_user_info(update['users'],
                                                         update['updates'][i]['message']['fwd_from']['from_id'])
                    if update['updates'][i]['message']['fwd_from'].get('channel_id'):
                        res['forward_from_chat'] = form_chat_info(update['chats'],
                                                                  update['updates'][i]['message']['fwd_from'][
                                                                      'channel_id'])
                    if update['updates'][i]['message']['fwd_from'].get('channel_post'):
                        res['forward_from_message_id'] = update['updates'][i]['message']['fwd_from'].get('channel_post')

                if update['updates'][i]['message'].get('edit_date'):
                    res['edit_date'] = convert_time(update['updates'][i]['message']['edit_date'])

                if update['updates'][i]['message']['entities']:
                    res['entities'] = update['updates'][i]['message']['entities']

                if update['updates'][i]['message']['message']:
                    res['text'] = update['updates'][i]['message']['message']
                    res['content_type'] = 'text'

                if update['updates'][i]['message']['reply_to_msg_id']:
                    # TODO: Full Message object in 'reply_to_message'
                    res['reply_to_message'] = {'message_id': update['updates'][i]['message']['reply_to_msg_id']}

                elif update['updates'][i]['message']['media']:
                    # Photo
                    if update['updates'][i]['message']['media'].get('document'):
                        if list(update['updates'][i]['message']['media'].keys())[0] == 'photo':
                            res['content_type'] = 'photo'
                            res['photo'] = []
                            for pht in update['updates'][i]['message']['media']['photo']['sizes']:
                                res['photo'].append(
                                    {'width': pht['w'], 'height': pht['h'], 'file_size': pht['size'], 'file_id': None})

                        elif list(update['updates'][i]['message']['media'].keys())[0] == 'document' and 'webp' in str(
                                update['updates'][i]['message']['media']['document'].get('mime_type')):
                            # Sticker)
                            res['content_type'] = 'sticker'
                            res['sticker'] = {'file_id': None}
                            res['sticker']['width'] = \
                                update['updates'][i]['message']['media']['document']['attributes'][0]['w']
                            res['sticker']['height'] = \
                                update['updates'][i]['message']['media']['document']['attributes'][0]['h']
                            res['sticker']['emoji'] = \
                                update['updates'][i]['message']['media']['document']['attributes'][1]['alt']
                            res['sticker']['file_size'] = update['updates'][i]['message']['media']['document']['size']
                        elif 'video' in update['updates'][i]['message']['media']['document']['mime_type']:
                            if update['updates'][i]['message']['media']['document']['attributes'][0]['round_message']:
                                # Video
                                res['video_note'] = {'file_id': None}
                                res['content_type'] = 'video_note'
                            else:
                                # Video Message
                                res['video'] = {'file_id': None}
                                res['content_type'] = 'video'
                            video_type = res['content_type']
                            if video_type == 'video':
                                res[video_type]['width'] = \
                                    update['updates'][i]['message']['media']['document']['attributes'][0]['w']
                                res[video_type]['height'] = \
                                    update['updates'][i]['message']['media']['document']['attributes'][0]['h']
                            else:
                                res[video_type]['length'] = \
                                    update['updates'][i]['message']['media']['document']['attributes'][0]['w']
                            res[video_type]['duration'] = \
                                update['updates'][i]['message']['media']['document']['attributes'][0]['duration']
                            res[video_type]['mime_type'] = update['updates'][i]['message']['media']['document'][
                                'mime_type']
                            res[video_type]['file_size'] = update['updates'][i]['message']['media']['document']['size']
                            if update['updates'][i]['message']['media']['document']['thumb']:
                                res[video_type]['thumb'] = {'file_id': None}
                                res[video_type]['thumb']['width'] = \
                                    update['updates'][i]['message']['media']['document']['thumb']['w']
                                res[video_type]['thumb']['height'] = \
                                    update['updates'][i]['message']['media']['document']['thumb']['h']
                                res[video_type]['thumb']['file_size'] = \
                                    update['updates'][i]['message']['media']['document']['size']
                                if update['updates'][i]['message']['media']['document']['thumb'].get('bytes'):
                                    res[video_type]['thumb']['bytes'] = \
                                        update['updates'][i]['message']['media']['document']['thumb']['bytes']

                        elif 'audio' in update['updates'][i]['message']['media']['document']['mime_type']:
                            if update['updates'][i]['message']['media']['document']['attributes'][0].get('voice'):
                                # Voice
                                res['content_type'] = 'voice'
                                res['voice'] = {'file_id': None}
                                res['voice']['duration'] = \
                                    update['updates'][i]['message']['media']['document']['attributes'][0]['duration']
                                res['voice']['mime_type'] = \
                                    update['updates'][i]['message']['media']['document'].get('mime_type')
                                res['voice']['file_size'] = \
                                    update['updates'][i]['message']['media']['document']['size']
                            else:
                                # Audio
                                res['content_type'] = 'audio'
                                res['audio'] = {'file_id': None}
                                res['audio']['duration'] = \
                                    update['updates'][i]['message']['media']['document']['attributes'][0]['duration']
                                res['audio']['mime_type'] = \
                                    update['updates'][i]['message']['media']['document'].get('mime_type')
                                res['audio']['file_size'] = \
                                    update['updates'][i]['message']['media']['document']['size']
                                res['audio']['title'] = \
                                    update['updates'][i]['message']['media']['document']['attributes'][0]['title']
                                res['audio']['performer'] = \
                                    update['updates'][i]['message']['media']['document']['attributes'][0].get(
                                        'performer')

                        else:
                            # Other
                            res['content_type'] = 'document'
                            res['document'] = {'file_id': None}
                            res['document']['mime_type'] = \
                                update['updates'][i]['message']['media']['document'].get('mime_type')
                            res['document']['file_name'] = \
                                update['updates'][i]['message']['media']['document']['attributes'][0].get('file_name')
                            res['document']['file_size'] = \
                                update['updates'][i]['message']['media']['document']['attributes'].get('size')

                    elif update['updates'][i]['message']['media'].get('geo'):
                        # Location
                        res['content_type'] = 'location'
                        res['location'] = {}
                        res['location']['longitude'] = update['updates'][i]['message']['media']['geo']['long']
                        res['location']['latitude'] = update['updates'][i]['message']['media']['geo']['lat']

                    elif 'venue_id' in update['updates'][i]['message']['media']:
                        # Venue
                        res['content_type'] = 'venue'
                        res['venue'] = {'location': {}}
                        res['venue']['location']['longitude'] = update['updates'][i]['message']['media']['geo']['long']
                        res['venue']['location']['latitude'] = update['updates'][i]['message']['media']['geo']['lat']
                        res['venue']['title'] = update['updates'][i]['message']['media'].get('title')
                        res['venue']['address'] = update['updates'][i]['message']['media'].get('address')
                        res['venue']['foursquare_id'] = update['updates'][i]['message']['media'].get('venue_id')

                    elif 'phone_number' in update['updates'][i]['message']['media']:
                        # Contact
                        res['content_type'] = 'contact'
                        res['contact'] = {}
                        res['contact']['first_name'] = update['updates'][i]['message']['media']['first_name']
                        res['contact']['last_name'] = update['updates'][i]['message']['media']['last_name']
                        res['contact']['phone_number'] = update['updates'][i]['message']['media']['phone_number']
                        res['contact']['user_id'] = update['updates'][i]['message']['media'].get('user_id')

                    elif 'game' in update['updates'][i]['message']['media']:
                        # Game
                        res['content_type'] = 'game'
                        res['game'] = {}
                        res['game']['title'] = update['updates'][i]['message']['media']['game']['title']
                        res['game']['description'] = update['updates'][i]['message']['media']['game']['description']
                        res['game']['text'] = res['text']
                        res['text'] = None  # Overriding
                        res['game']['text_entities'] = res['entities']
                        res['entities'] = None  # Overriding

                        res['game']['photo'] = []
                        for pht in update['updates'][i]['message']['media']['game']['photo']['sizes']:
                            res['game']['photo'].append(
                                {'width': pht['w'], 'height': pht['h'], 'file_size': pht['size'], 'file_id': None})
                        if update['updates'][i]['message']['media']['game'].get('document'):
                            res['animation'] = {'file_id': None}
                            if len(update['updates'][i]['message']['media']['game']['document']['attributes']) > 1:
                                res['animation']['file_name'] = \
                                    update['updates'][i]['message']['media']['game']['document']['attributes'][1].get(
                                        'file_name')
                            res['animation']['mime_type'] = update['updates'][i]['message']['media']['game'][
                                'document'].get('mime_type')
                            res['animation']['file_size'] = update['updates'][i]['message']['media']['game'][
                                'document'].get('size')
                            if update['updates'][i]['message']['media']['game']['document'].get('thumb'):
                                res['animation']['thumb'] = {'file_id': None}
                                res['animation']['thumb']['width'] = \
                                    update['updates'][i]['message']['media']['game']['document']['thumb']['w']
                                res['animation']['thumb']['height'] = \
                                    update['updates'][i]['message']['media']['game']['document']['thumb']['h']
                                res['animation']['thumb']['file_size'] = \
                                    update['updates'][i]['message']['media']['game']['document']['thumb']['size']
                            else:
                                res['animation']['thumb'] = None

                    if update['updates'][i]['message']['media'].get('caption'):
                        res['caption'] = update['updates'][i]['message']['media']['caption']
    elif isinstance(update_type, UpdateShort) and update['update'].get('chat_id') and 'action' in update['update']:
        res['content_type'] = 'action'
        if update['update']['action']:
            res['action'] = 'upload'  # Can't get accurate info what's uploading
        else:
            res['action'] = 'typing'
        res['date'] = convert_time(update['date'])
        res['from_user'] = {'id': update['update']['user_id']}
        res['chat'] = {'id': update['update']['chat_id']}

    else:
        # Other Updates
        return
    if res['content_type']:  # A bit tricky but fast
        return res
