
==========
Thumbnails
==========

Sometimes is hard to manage all templates to use one thumbnail tag.

Leonardo has one thumbnail tag which lives under ``thumbnail`` templatetags.

This template tag combine ``sorl`` and ``easy-thumbnails``. This templatetag can render different thumbnails in same template without syntax error.

this makes big advantages with supporting more backends for example we use ``easy_thumbnails`` and if we install ``leonardo_module_eshop`` or plain ``Django oscar`` which requires ``sorl-thumbnail`` as default thumbnail library we have problem. Leonardo support many variations thumbnail tags

Sorl
====

.. code-block:: html

    {% load thumbnail %}
    {% thumbnail widget.image.file size format="PNG" as thumb %}
        <img src='{{ thumb.url }}' alt='my-image' />
    {% endthumbnail %}

Easy-thumbnails
===============

.. code-block:: html

    {% load thumbnail %}
    <img src="{% thumbnail profile.photo 50x50 crop %}" alt="" />

Combined
========

.. code-block:: html

    {% load thumbnail %}

    {% thumbnail widget.image.file size format="PNG" as thumb %}
        <img src='{{ thumb.url }}' alt='my-image' />
    {% endthumbnail %}

    <img src="{% thumbnail profile.photo 50x50 crop %}" alt="" />


For more examples and settings must follow appropriate pages. For Sorl http://sorl-thumbnail.readthedocs.org/en/latest/index.html and for Easy-Thumbnails https://github.com/SmileyChris/easy-thumbnails