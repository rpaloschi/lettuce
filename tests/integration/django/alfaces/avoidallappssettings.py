DEBUG = True
ROOT_URLCONF = 'urls'
SECRET_KEY = 'secret'

INSTALLED_APPS = (
    'foobar',
    'donothing',
    'lettuce.django',
)

LETTUCE_AVOID_APPS = (
    'foobar',
    'donothing',
)
