
=========
Languages
=========

For settings Langugages follow standard Django settings like this::

    LANGUAGE_CODE = 'en'

    LANGUAGES = (
        ('en', 'EN'),
        ('cs', 'CS'),
    )

This is default settings which specify English as default Language

.. note::

    location of these settings is ``local_settings.py`` or your Site settings file

for switching to Czech as default redefine::

    LANGUAGE_CODE = 'cs'

    LANGUAGES = (
        ('cs', 'CS'),
        ('en', 'EN'),
    )

.. warning::

    Ordering in the ``LANGUAGES`` is important for translations ! First must be default language.

Leonardo provides one management command for making messages and theirs compiling::

    python manage.py update_translations
