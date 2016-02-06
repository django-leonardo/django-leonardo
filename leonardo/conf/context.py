def offline_context():
    from django.conf import settings
    from leonardo.module.web.models import PageTheme

    for theme in PageTheme.objects.all():
        for color_scheme in theme.templates.all():
            yield {
                'STATIC_URL': settings.STATIC_URL,
                'LEONARDO_CONFIG': settings.HORIZON_CONFIG,
                'HORIZON_CONFIG': settings.HORIZON_CONFIG,
                'WEBROOT': '/',
                'leonardo_page': {
                    'theme': {
                        'name': theme.name.lower()
                    },
                    'color_scheme': {
                        'name': color_scheme.name.lower()
                    }
                }
            }
