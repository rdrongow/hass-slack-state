"""
Slack state setter for notify component.
"""

import logging
import requests
import voluptuous as vol
import urllib.parse
import json

from homeassistant.components.notify import (
    BaseNotificationService, PLATFORM_SCHEMA)

from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv

CONF_TOKEN = 'token'
CONF_RESOURCE = 'https://slack.com/api/users.profile.set'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_TOKEN): cv.string,
    vol.Optional(CONF_NAME): cv.string
})

_LOGGER = logging.getLogger(__name__)


def get_service(hass, config, discovery_info=None):
    """Get the slack state notification service."""
    resource = CONF_RESOURCE
    token = config.get(CONF_TOKEN)
    return SlackStateService(hass, resource, token)


class SlackStateService(BaseNotificationService):
    """Implementation of a notification state service for slack."""

    def __init__(self, hass, resource, token):
        """Initialize the service."""
        self._resource = resource
        self._hass = hass
        self._token = token

    def send_message(self, message="", **kwargs):
        """Send a message to a user."""

        emoji = ":house:"
        if kwargs.get("data") and kwargs["data"].get("emoji"):
            emoji = kwargs["data"]["emoji"]
        profile = dict()
        profile['status_text'] = message
        profile['status_emoji'] = emoji
        url = '%s?token=%s&profile=%s' % (
            self._resource,
            self._token,
            urllib.parse.quote_plus(json.dumps(profile)))
        response = requests.post(url, timeout=10)

        if response.status_code not in (200, 201):
            _LOGGER.exception(
                "Error sending message. Response %d: %s:",
                response.status_code, response.reason)
        elif not response.json().get("ok"):
            _LOGGER.exception(
                "Error sending message: %s:",
                response.json().get("error"))
