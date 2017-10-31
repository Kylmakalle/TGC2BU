# TGC2BU
Telegram Client to Bot Updates

# REMEMBER, TGC2BU IS UNSTABLE!
But feel free to submit [issues](https://github.com/Kylmakalle/TGC2BU/issues) and make [PRs](https://github.com/Kylmakalle/TGC2BU/pulls).
## Installation

```
git clone https://github.com/Kylmakalle/TGC2BU.git
# Edit credentials.py with your values
pip install -r requirements.txt # Please, check Telethon version, only 0.11.5 is supported now!
python run.py
```
Edit [this line](https://github.com/Kylmakalle/TGC2BU/blob/master/updates_handler.py#L107) for your needs

And [this](https://github.com/Kylmakalle/TGC2BU/blob/master/updates_handler.py#L198) If you care about non-bot's/via-bot's messages

In your code you can do something like this:
```python
if update.get('mtproto'): ## if update.mtproto ## etc.
   ### Process update from Client API, handling bytes instead of file_id, via_bot instances and etc.
else:
   ### Process update from Bot API
```


## Supported Types

**TGC2BU** supports all message types according to [Bot API docs](https://core.telegram.org/bots/api#message), but with small nuances.

Every **TGC2BU** update is marked with `'mtproto': True`

### Example Message Update
```python
{
    'mtproto': True,
    'content_type': 'text',
    'message_id': 509935,
    'from_user': {
        'id': 240044026,
        'first_name': 'IFTTT',
        'username': 'IFTTT',
        'last_name': None,
        'language_code': None,
        'is_bot': True,
        },
    'date': 1509478637,
    'chat': {
        'type': 'supergroup',
        'username': 'ru2chmobi',
        'id': -1001098866708,
        'title': '2ch /mobi/',
        'all_members_are_administrators': False,
        },
    'text': 'http://ift.tt/2yiOU3j',
    'entities': [{'type':'url', 'offset': 0, 'length': 21}],
}
```

For obvious reasons, you can't access `file_id` and etc using **TGC2BU** now. This should be implemented as forward to private chat with your bot and syncing with mtproto update. You will get `bytes` for some file types and sizes.

### Example Message with Photo via @bot
```python
{
    'mtproto': True,
    'content_type': 'photo',
    'message_id': 3758,
    'from_user': {
        'id': 317376041,
        'first_name': 'Text [some text]',
        'username': 'mobitester',
        'last_name': None,
        'language_code': None,
        'is_bot': False
    },
    'date': 1509480802,
    'chat': {
        'type': 'supergroup',
        'username': 'combottop',
        'id': -1001149082593,
        'title': 'Emoji Test: 😎😘🤔😀😊',
        'all_members_are_administrators': False
    },
    'photo': [{
        'width': 90,
        'height': 50,
        'file_size': None,
        'file_id': None,
        'bytes': b '\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x0e\n\x0b\r\x0b\t\x0e\r\x0c\r\x10\x0f\x0e\x11\x16$\x17\x16\x14\x14\x16, !\x1a$4.763.22:ASF:=N>22HbINVX]^]8EfmeZlS[]Y\xff\xdb\x00C\x01\x0f\x10\x10\x16\x13\x16*\x17\x17*Y;2;YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY\xff\xc0\x00\x11\x08\x002\x00Z\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1b\x00\x00\x02\x03\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x05\x00\x02\x04\x06\x01\x07\xff\xc4\x001\x10\x00\x02\x02\x01\x01\x06\x04\x04\x05\x05\x00\x00\x00\x00\x00\x00\x01\x02\x00\x03\x11\x04\x05\x12!"1Q\x13Aa\x81\x062q\xa1BRr\xc1\xf0\x14\x15#3\x91\xff\xc4\x00\x19\x01\x00\x03\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\xff\xc4\x00 \x11\x00\x03\x00\x02\x03\x00\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x11\x12!1\x04Aq\x81\xa1\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xdf=\x13\xc9a(\xcc"\x88U\x10k\x0c\xb0\x00\xa8!TL\x97\xea\xab\xd3\xaf\x1ef\xf2Q2\x0b\xb5\xd7\x82\xc6\xe1\xa7\x07\xa2\xa2\x02q\xef\x10\xc7j%\xc2\xceGQ\xa9\xdazbK\xeb,\x1d\xbe^?i\x0e\xdb\xd4\xe9\xd2\xbbWh\x0b\x97#},\xa8\x0cw\xe2 3\xae+(\xc2\'\xa3\xe2Jo\xda\xe3H\x11E-\xf2[\xbd\xd7\xb6G\xactpFA\xc8\x80\x00a\x07\x88g\x83\x80\n\xa6k\xf5\xd5\xd0\xdb\x80\x17~\xc3\xa0\xf7\x96\xd6]\xfd6\x92\xdb\xbf"\xe7\xa6g9N\xbfOj\x9b\x1f\xc5*\x0f\x16\xdd\xcf\x1f\\I\xaak\xc3\x7f\x8f\x8a/n\xdfC\xd5\xdaEA.\xcb\x9e\xc8\xb9\xc7\xbf\x9c\x13\xedk\xb7\xb9\x19\xc0\xec\x14\x0f\xd8\xc5M\xae\xd1\x11\xcb\xa8S\xd8\x1c\x83\xf7\x99\xae\xbe\xc6\xff\x00U\xb5/\x1f\xc5\xdag\xcd\xf8w/\x8d\rnV\xff\x00\x03$\xd4\xf8n\xe4\x17\xdf\xb0\xef\x1e|\x9c\xf7\xe9\n\xcf\xa9\x15\x9b<{T\x0f-\xe8\x9a\xcb\x90\xee\x8a\xb3\xe2`\x02\xca\xc7\x04\xe3\x8f\x03\xeb\x03v\xa3V\xec\xb4\x8b]F\xf8^S\xe6cM\xb7\xa4\x17\x87\x168\xe7k\xf41\xb3\xc7\xb2\xceck\x9227\x8fPd\xb3I\xa8\xbd7V\x9c\xe3\xcb\xbf\xf3\x8c]\xa7\xdaZ\x9d=\xaaZ\xe1\xa9FC\xb8\xcf\x93\x81\xe6!\x1fij\x98\xe7\xc7q\xfaN\x07\xda*\xb7/E\xe1\xc1\x87,\xf2HeN\xc4\xd6\xda\x84\\\x968?\x91@?\xf6j\xd1\xad\x9b3z\xaa\xd2\xca\xd8\x82\xcc\xa6\xfel\x0e\xa4\x01\xc3\xed9\xcb5V\xbf\xcfk\xb7\xd5\x89\x95\xaf.[\x8fA\x93\xf4\x92\xa9\xbe\x91\xa6L8\xe5:\xaf\xa3\xe8\x1b\x13j&\xd1\xaa\xd5\x17-\xafS`\x900H=3\x19NC\xe1]\x1bQ\xb5\xed\xb4pCIV\xe0G6T\xe3\xdb\x8c\xebs7H\xf1i\xa6\xf6\x84\x9a\xea\xde\xdd\x1d\xa9Z\x86r8\x03\xe78\x8dn\x96\xfd\x06\xa3\x169\xa4\xb8\xc8\x1b\xf8\xcf\xb8\x9d\xf3gt\xe0\xe0\xc5z\xed\x15Z\xce\x1a\x84/\x88\xda\x1c^\x97\x16\xba8\xd2\xb6X\xdb\xcfr\xb7\xa990\xfe\x18f\xc7\x89Z\x8fV\x8f?\xb0\xe9s\xca\xd6\'\xd0\xca\xbf\xc3\xaa\xd9\xdc\xd49\xf42*w\xe9\xd5\x8b<\xc2z\x9f\xe8\x93{\xc1\xea\xcaH\xfc\xa73p\xb9\x16\xc6kp\xc4\xaf\x00\xa3\xbeN;\x12~\x9e\xf3\xddF\xc0\xb1T\x8f\x10\x9fi(\xd9\x9a\xd4\xad\x15\x9bN@?\xe36)%O\xa6?xL\xe8\x8c\xf9\xde]\'\xd6\x85\xfa\x94\n\xc8\x10\xf2`\xb2\xa9\x18*\xa7\xa0#\xbc\xa6}c\x9a\xf6!v&\xfb\x1c\xb9<p&\xda\xb6\x1d\x03\xaa\x16\xfdF7)\xbe\xc8\x8c\xf7\x0b\x8c\x9c\xces\xd2@.W\x05\x11\x8fl\x0c\xce\xca\xbd\x99R|\xb5\xa0\xf6\x84;=]\xb2z\x0e\xd0I \xac\xb9)v\xfa\'\xc2\xe8\xe2\xbb\xedj\xf77\xcf\x99\xe2?\x9f\xb4}\xbd1i*\x14\xb3\x01\xf8\xb8\xcd;\xd2\x8evc= \xdeI#\x10"%\xbc\xe4\x92&i\x05\x0f\x10e\xdc\x0c\xf4\x1f(\x92H\x90W\xd1\xe8\x1c\xa9\xf4\x84Y$\x83*<\x08\xb2\xe2I \x82\x8b\xafY\xec\x92Fb\xcf\xff\xd9'
    }, {
        'width': 320,
        'height': 177,
        'file_size': 12359,
        'file_id': None,
        'bytes': None
    }, {
        'width': 800,
        'height': 442,
        'file_size': 50341,
        'file_id': None,
        'bytes': None
    }, {
        'width': 1280,
        'height': 707,
        'file_size': 104799,
        'file_id': None,
        'bytes': None
    }, {
        'width': 2560,
        'height': 1415,
        'file_size': 306312,
        'file_id': None,
        'bytes': None
    }],
    'via_bot': {
        'id': 114528005,
        'first_name': 'Yandex Image Search',
        'username': 'pic',
        'last_name': None,
        'language_code': None,
        'is_bot': True
    }
}
```



### **New** _Action_ object!
This object represents a User Action.
Example:
```python
{
  'mtproto': True,
  'content_type': 'action',
  'from_user': {'id': 24272726},
  'date': 1509478552,
  'chat': {'id': 1134108493},
  'action': 'typing'
}
```

