from dataclasses import dataclass


@dataclass
class Service:
    url: str
    method: str
    headers: dict = None
    json: dict = None
    params: dict = None
    data: dict = None
    addition_to_url: dict = None


SERVICES = (
    Service(
        'https://eda.yandex/api/v1/user/request_authentication_code',
        'POST',
        json={'phone_number': '%s'},
    ),
    Service(
        'https://api.groshi247.com/v2/registration',
        'POST',
        json={'Registration': {'phone': '%s'}}
    ),
    Service(
        'https://api.sweet.tv/SignupService/SetPhone.json',
        'POST',
        json={
            "phone": '%s',
            "device": {
                "type": "DT_Web_Browser",
                "application": {"type": "AT_SWEET_TV_Player"},
                'model': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                "firmware": {"versionCode": 1, "versionString": "2.8.68"},
                "uuid": "0b40027f-893a-4d08-bb19-1ba74096b55a",
                "supported_drm": {"widevine_modular": True}
            },
            "locale": "uk"
        }
    ),
    Service(
        'https://vohngerxsaiweinge.com/api/2/auth/password/recover/send/',
        'POST',
        json={
            'phone': '%s',
            'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/91.0.4472.124 Safari/537.36'
        }
    ),
    Service(
        'https://synthetic.ua/api/auth/register/',
        'POST',
        json={
            "mobile_phone": '%s',
            "password": '123456789',
            "password_confirm": '123456789'
        }
    ),
    Service(
        'https://powernow.ua/api/application',
        'POST',
        json={"phone": "%s", "type": "sms_link"}
    ),
    Service(
        'https://api.boosty.to/oauth/phone/authorize',
        'POST',
        data={"client_id": "%s"}
    ),
    # Service(
    #     'https://mobile-api.qiwi.com/oauth/authorize',
    #     'POST',
    #     data={
    #         "response_type": "urn:qiwi:oauth:response-type:confirmation-id",
    #         "username": "%s",
    #         "client_id": "android-qw",
    #         "client_secret": "zAm4FKq9UnSe7id",
    #     },
    # ),
    Service(
        'https://mistercat.com.ua/index.php',
        'POST',
        params={
            "option": "com_ksenmart",
            "view": "profile",
            "task": "profile.sms_auth",
            "tmpl": "ksenmart",
        },
        data={"phone": "%s", "type": "send"},
    ),
)


proxies = {
    '100.19.135.109': 80,
    '51.222.121.247': 9300,
    '51.222.21.94': 32768,
    '143.198.167.240': 80,
    '64.225.1.248': 80,
    '149.56.1.48': 8181,
    '138.197.161.92': 80,
    '198.50.177.44': 44699,
    '143.244.157.101': 80,
    '159.203.12.49': 8888,
    '51.222.21.95': 32768,
    '51.161.35.79': 80,
    '51.222.123.192': 9300,
    '51.222.123.214': 9300,
    '64.225.61.1': 8080,
    '158.69.25.178': 32769,
    '51.222.121.242': 9300,
    '138.197.102.119': 80,
    '51.161.81.69': 9300,
    '51.222.123.191': 9300,
    '51.222.121.244': 9300,
    '51.222.121.246': 9300,
    '51.222.123.195': 9300,
    '51.222.123.218': 9300,
    '51.222.17.143': 9300,
    '51.222.123.211': 9300,
    '51.222.123.213': 9300,
    '51.222.123.204': 9300,
    '67.207.83.225': 80,
    '51.222.123.212': 9300
}
