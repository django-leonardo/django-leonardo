
from django.apps import AppConfig

default_app_config = 'leonardo.module.oauth.OAuthConfig'


class Default(object):

    optgroup = ('External auth')

    @property
    def apps(self):
        return [
            'allauth',
            'allauth.account',
            'allauth.socialaccount',
            'allauth.socialaccount.providers.amazon',
            'allauth.socialaccount.providers.angellist',
            'allauth.socialaccount.providers.bitbucket',
            'allauth.socialaccount.providers.bitly',
            'allauth.socialaccount.providers.coinbase',
            'allauth.socialaccount.providers.dropbox',
            #'allauth.socialaccount.providers.facebook',
            'allauth.socialaccount.providers.flickr',
            'allauth.socialaccount.providers.feedly',
            'allauth.socialaccount.providers.fxa',
            'allauth.socialaccount.providers.github',
            'allauth.socialaccount.providers.google',
            'allauth.socialaccount.providers.hubic',
            'allauth.socialaccount.providers.instagram',
            'allauth.socialaccount.providers.linkedin',
            'allauth.socialaccount.providers.linkedin_oauth2',
            'allauth.socialaccount.providers.odnoklassniki',
            'allauth.socialaccount.providers.openid',
            'allauth.socialaccount.providers.persona',
            'allauth.socialaccount.providers.soundcloud',
            'allauth.socialaccount.providers.stackexchange',
            'allauth.socialaccount.providers.tumblr',
            'allauth.socialaccount.providers.twitch',
            'allauth.socialaccount.providers.twitter',
            'allauth.socialaccount.providers.vimeo',
            'allauth.socialaccount.providers.vk',
            'allauth.socialaccount.providers.weibo',
            'allauth.socialaccount.providers.xing',
        ]

    @property
    def auth_backends(self):
        return ["allauth.account.auth_backends.AuthenticationBackend"]

    @property
    def ctp(self):
        return [
            "allauth.socialaccount.context_processors.socialaccount"
        ]


class OAuthConfig(AppConfig, Default):
    name = 'leonardo.module.oauth'
    verbose_name = "External Authorization"


default = Default()
