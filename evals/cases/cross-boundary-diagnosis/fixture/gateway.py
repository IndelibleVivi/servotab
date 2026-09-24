"""Shared ingress admission in a scaled diagnostic model."""


def admit(*, origin, relay_active, relay_tag, slot):
    if origin == "local":
        return True
    return slot <= 4
