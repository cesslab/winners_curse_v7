from os import environ, getenv

GENERIC_CONFIG = {
    "app_sequence": ["instructions", "bidsample", "quiz", "questions", "bid", "payoff", "questionnaire", "venmo"],
    "num_demo_participants": 2,
    "bid_lottery_1": "1",
    "bid_lottery_2": "2",
    "bid_lottery_3": "3",
    "bid_lottery_4": "4",
    "questions_lottery_1": "1",
    "questions_lottery_2": "2",
    "questions_lottery_3": "3",
    "questions_lottery_4": "4",
}

SESSION_CONFIGS = [
    {**GENERIC_CONFIG, **{"name": "cv", "treatment": "cv"}},
    {**GENERIC_CONFIG, **{"name": "cp", "treatment": "cp"}},
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.0, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = False

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = getenv("SECRET_KEY", "9910429831890")

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ["otree"]

ROOMS = [
    {
        'name': 'cess_lab',
        'display_name': 'CESS Lab',
    },
]
# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

