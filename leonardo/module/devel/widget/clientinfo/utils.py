
from .simple_devices import simple_devices


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_client_type(request):
    # defaults
    request.is_android_device = False
    request.is_kindle_device = False
    request.is_ios_device = False
    request.is_ios5_device = False
    request.is_touch_device = False
    request.is_simple_device = False
    request.is_webkit = False
    request.is_webos = False
    request.is_wide_device = False
    request.is_windows_phone_device = False

    if 'HTTP_USER_AGENT' in request.META:
        s = request.META["HTTP_USER_AGENT"].lower()

        if 'applewebkit' in s:
            request.is_webkit = True

        if 'ipad' in s:
            request.is_ios_device = True
            request.is_touch_device = True
            request.is_wide_device = True

        elif 'iphone' in s or 'ipod' in s:
            request.is_ios_device = True
            request.is_touch_device = True

        elif 'android' in s:
            request.is_android_device = True
            request.is_touch_device = True

            if 'xoom' in s:
                request.is_wide_device = True

        elif 'webos' in s:
            request.is_webos_device = True
            request.is_touch_device = True

        elif 'windows phone' in s:
            request.is_windows_phone_device = True
            request.is_touch_device = True

        elif 'kindle' in s:
            request.is_kindle_device = True

        # Now that all the good devices are out of the way, lets see if this is an
        # old phone.

        elif 'HTTP_X_OPERAMINI_FEATURES' in request.META:
            request.is_simple_device = True

        elif 'application/vnd.wap.xhtml+xml' in request.META.get('HTTP_ACCEPT', '').lower():
            request.is_simple_device = True

        elif any([device in s for device in simple_devices]):
            request.is_simple_device = True

        else:
            # assume desktop at this point
            request.is_wide_device = True

        if request.is_ios_device and 'os 5' in s:
            request.is_ios5_device = True
    else:
        request.is_wide_device = True
    return request
