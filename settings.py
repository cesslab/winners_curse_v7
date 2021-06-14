from os import environ, getenv

GENERIC_CONFIG = {
    "app_sequence": ["instructions", "bidsample", "quiz", "bid", "questions", "payoff"],
    "num_demo_participants": 2,
    "lottery_1": "1",
    "lottery_2": "2",
    "lottery_3": "3",
    "lottery_4": "4",
    "lottery_5": "5",
    "lottery_6": "6",
    "lottery_7": "7",
    "lottery_8": "8",
    "endowment_tokens": "100",
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
    real_world_currency_per_point=0.167, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = True

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = getenv("SECRET_KEY", "9910429831890")

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ["otree"]
