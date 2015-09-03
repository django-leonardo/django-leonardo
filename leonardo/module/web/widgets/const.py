
ENTER_EFFECT_CHOICES = (
    ('disabled', 'Disabled'),
    ('Attention Seekers', (
        ('bounce', 'Bounce'),
        ('flash', 'Flash'),
        ('pulse', 'Pulse'),
        ("rubberBand", 'RubberBand'),
        ("shake", 'Shake'),
        ("swing", 'Swin)g'),
        ("tada", 'Tada'),
        ("wobble", 'Wobble'),
        ("jello", 'Jello'),
    )
    ),
    ('Bouncing Entrances', (
        ('bounceIn', 'Bounce In'),
        ('bounceInDown', 'Bounce In Down'),
        ('bounceInDown', 'BounceInDown'),
        ('bounceInLeft', 'BounceInLeft'),
        ('bounceInRight', 'BounceInRight'),
        ('bounceInUp', 'BounceInUp'),
    )
    ),
    ('Bouncing Exits', (
        ('bounceIn', 'Bounce In'),
        ('bounceOut', 'BounceOut'),
        ('bounceOutDown', 'BounceOutDown'),
        ('bounceOutLeft', 'BounceOutLeft'),
        ('bounceOutRight', 'BounceOutRight'),
        ('bounceOutUp', 'BounceOutUp'),
    )
    ),
    ('Fading Entrances', (
        ('fadeIn', 'fadeIn'),
        ('fadeInDown', 'fadeInDown'),
        ('fadeInDownBig', 'fadeInDownBig'),
        ('fadeInLeft', 'fadeInLeft'),
        ('fadeInLeftBig', 'fadeInLeftBig'),
        ('fadeInRight', 'fadeInRight'),
        ('fadeInRightBig', 'fadeInRightBig'),
        ('fadeInUp', 'fadeInUp'),
        ('fadeInUpBig', 'fadeInUpBig'),
    )
    ),
    ('Fading Exits', (
        ('fadeOut', 'fadeOut'),
        ('fadeOutDown', 'fadeOutDown'),
        ('fadeOutDownBig', 'fadeOutDownBig'),
        ('fadeOutLeft', 'fadeOutLeft'),
        ('fadeOutLeftBig', 'fadeOutLeftBig'),
        ('fadeOutRight', 'fadeOutRight'),
        ('fadeOutRightBig', 'fadeOutRightBig'),
        ('fadeOutUp', 'fadeOutUp'),
        ('fadeOutUpBig', 'fadeOutUpBig'),
    )
    ),
    ('Flippers', (
        ('flip', 'flip'),
        ('flipInX', 'flipInX'),
        ('flipInY', 'flipInY'),
        ('flipOutX', 'flipOutX'),
        ('flipOutY', 'flipOutY'),
    )
    ),
    ('Lightspeed', (
        ('lightSpeedIn', 'lightSpeedIn'),
        ('lightSpeedOut', 'lightSpeedOut'),
    )
    ),
    ('Rotating Entrances', (
        ('rotateIn', 'rotateIn'),
        ('rotateInDownLeft', 'rotateInDownLeft'),
        ('rotateInDownRight', 'rotateInDownRight'),
        ('rotateInUpLeft', 'rotateInUpLeft'),
        ('rotateInUpRight', 'rotateInUpRight'),
    )
    ),
    ('Rotating Exits', (
        ('rotateOut', 'rotateOut'),
        ('rotateOutDownLeft', 'rotateOutDownLeft'),
        ('rotateOutDownRight', 'rotateOutDownRight'),
        ('rotateOutUpLeft', 'rotateOutUpLeft'),
        ('rotateOutUpRight', 'rotateOutUpRight'),
    )
    ),
    ('Sliding Entrances', (
        ('slideInUp', 'slideInUp'),
        ('slideInDown', 'slideInDown'),
        ('slideInLeft', 'slideInLeft'),
        ('slideInRight', 'slideInRight'),
    )
    ),
    ('Sliding Exits', (
        ('slideOutUp', 'slideOutUp'),
        ('slideOutDown', 'slideOutDown'),
        ('slideOutLeft', 'slideOutLeft'),
        ('slideOutRight', 'slideOutRight'),
    )
    ),
    ('Zoom Entrances', (
        ('slideOutUp', 'slideOutUp'),
        ('slideOutDown', 'slideOutDown'),
        ('slideOutLeft', 'slideOutLeft'),
        ('slideOutRight', 'slideOutRight'),
    )
    ),
    ('Zoom Exits', (
        ('zoomIn', 'zoomIn'),
        ('zoomInDown', 'zoomInDown'),
        ('zoomInLeft', 'zoomInLeft'),
        ('zoomInRight', 'zoomInRight'),
        ('zoomInUp', 'zoomInUp'),
    )
    ),
    ('Specials', (
        ('hinge', 'hinge'),
        ('rollIn', 'rollIn'),
        ('rollOut', 'rollOut'),
    )
    ),
)


WIDGET_COLOR_SCHEME_CHOICES = (
    ('Brand styles', (
        ('default', 'Default'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('custom', 'Custom'),
        ('red', 'Red'),
        ('blue', 'Blue'),
    )
    ),
)


PAGINATION_CHOICES = (
    ('paginator', 'Paginator'),
    ('cycle', 'Cycle'),
    ('slide', 'Slide'),
    ('grid', 'Grid'),
)
