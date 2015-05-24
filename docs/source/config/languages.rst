
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

for switching to Czech as default redefine::

    LANGUAGE_CODE = 'cs'

    LANGUAGES = (
        ('cs', 'CS'),
        ('en', 'EN'),
    )

.. warning::

    Ordering in the ``LANGUAGES`` is important for translations ! First must be default language.