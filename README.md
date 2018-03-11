# Purpose

This is a custom component for the awesome ![Home Assistant](https://home-assistant.io). It extends the `BaseNotificationService` to set the user state for a ![slack team](https://slack.com). It should be used in combination with automations.

# Installation

Simply put the component in `~/.homeassistant/custom_components/notify/slack_state.py`. The component is configured like this in the `configuration.yaml`:

```
notify:
  - name: slack_state
    platform: slack_state
    token: [your token] # you might want to put this secrets.yml
```

You might want to generate a ![legacy token](https://api.slack.com/custom-integrations/legacy-tokens) to get started. You could also use an oauth token and register an app, which is the preferred and modern way at slack. The oauth process itself is not supoorted by this component, yet.

# Example automation

One way to use this component is to base your user state on a geo location. Home Assistant provides ![support](https://home-assistant.io/components/device_tracker.owntracks/) for ![Owntracks](http://owntracks.org/) and also for geo fencing with the ![zone component](https://home-assistant.io/components/zone/). Let's suppose you want to set a state, when you enter your office zone. You would need to configure a zone in the `configuration.yaml`:

```
zone 1:
  name: My Office
  latitude: [latitude]
  longitude: [longitude]
  radius: 100
```

Now you are all set to set a state, once you enter this zone. Put the following
in your `automations.yaml`:

```
- id: enter_office
  alias: "enter my office"
  trigger:
    platform: zone
    entity_id: device_tracker.my_device_id
    zone: zone.my_office
    event: enter
  action:
    - service: notify.slack_state
      data:
        message: "in office"
        data: 
          emoji: ":office:"
```

# Comparison to other components

This component is only a simplified variant of the REST notification component, which is much more powerful, but not very convenient for this sepcial usecase, since the profile parameter needs to be passed as urlencoded json.

Home Assistant ships with a slack notification component, which is very good to post messages into channels. It can't be used, to set the state, though.

# To Do

* be compliant to home assistant coding standard
* make default emoji configurable

