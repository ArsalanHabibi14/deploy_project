import json

from ippanel import Client

api_key = "tiFfLmfYlgQDqrclxgMyx2DnGx9nrSZZBfpLnbd_EQc="
sms = Client(api_key)


def OTPService(to, code):
    pattern_values = {
        "code": str(code),
    }
    to = to[1:]
    bulk_id = sms.send_pattern(
        "vuduuykm0qdri4w",  # pattern code
        "983000505",  # originator
        to,  # recipient
        pattern_values,  # pattern values
    )


def OrderStatusService(to, id, pattern):
    pattern_values = {
        "id": id,
    }

    bulk_id = sms.send_pattern(
        pattern,  # pattern code
        "983000505",  # originator
        to,  # recipient
        pattern_values,  # pattern values
    )
