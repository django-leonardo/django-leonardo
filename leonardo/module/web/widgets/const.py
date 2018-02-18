
ENTER_EFFECT_CHOICES = (
    ('disabled', 'Disabled'),
    ('Fade animations', (
        ('fade', 'Fade'),
        ('fade-up', 'Fade Up'),
        ('fade-down', 'Fade Down'),
        ('fade-left', 'Fade Left'),
        ('fade-right', 'Fade Right'),
        ('fade-up-right', 'Fade Up Right'),
        ('fade-up-left', 'Fade Up Left'),
        ('fade-down-right', 'Fade Down Right'),
        ('fade-down-left', 'Fade Down Left'),
    )
    ),
    ('Flip animations', (
        ('flip-up', 'Flip Up'),
        ('flip-down', 'Flip Down'),
        ('flip-left', 'Flip Left'),
        ('flip-right', 'Flip Right'),
    )
    ),
    ('Slide animations', (
        ('slide-up', 'Slide Up'),
        ('slide-down', 'Slide Down'),
        ('slide-left', 'Slide Left'),
        ('slide-right', 'Slide Right'),
    )
    ),
    ('Zoom animations', (
        ('zoom-in', 'zoom In'),
        ('zoom-in-up', 'Zoom In Up'),
        ('zoom-in-down', 'Zoom In Down'),
        ('zoom-in-left', 'Zoom In Left'),
        ('zoom-in-right', 'Zoom In Right'),
        ('zoom-out', 'Zoom Out'),
        ('zoom-out-up', 'Zoom Out Up'),
        ('zoom-out-down', 'Zoom Out Down'),
        ('zoom-out-left', 'Zoom Out Left'),
        ('zoom-out-right', 'Zoom Out Right'), 
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
