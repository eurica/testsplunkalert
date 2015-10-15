# HipChat alert settings

action.hipchat = [0|1]
* Enable hipchat notification

action.hipchat.param.room = <string>
* Name of the room to send the notification to
* (required)

action.hipchat.param.message = <string>
* The message to send to the hipchat room. 
* (required)

action.hipchat.param.message_format = [html|text]
* The format of the room notification (optional)
* Default is "html"
* (optional)

action.hipchat.param.color = [red|green|blue|yellow|grey]
* Background color of the room notification (optional)
* (optional)

action.hipchat.param.notify = [1|0]
* Notify users in the room
* Defaults to 0 (not notifying users in the room)
* (optional)

action.hipchat.param.auth_token = <string>
* Override Hipchat API auth token from global alert_actions config
* (optional)
