import sys
import json
import urllib2


def send_message(settings):
    print >> sys.stderr, "DEBUG Sending message with settings %s" % settings
    room = settings.get('room')
    auth_token = settings.get('auth_token')
    base_url = settings.get('base_url').rstrip('/')
    fmt = settings.get('format', 'text')
    print >> sys.stderr, "INFO Sending message to hipchat room=%s with format=%s" % (room, fmt)
    url = "https://events-pagerduty-com-h1wht6shd77e.runscope.net/6b69fbcc6df04479a8c172a301eba966/events/enqueue"
    
    body = json.dumps(dict(
        version=3,
        service_key:"8fad31507784012f4c54123139146e6c",
        evnt_type:"trigger",
        description:"Splunk issue",
        message=settings.get('message'),
        message_format=fmt,
        color=settings.get('color', "green"),
        notify=normalize_bool(settings.get('notify', 'false')),
        settings=dict(settings),
        auth_token=settings.get("auth_token")
    ))
    print >> sys.stderr, 'DEBUG Calling url="%s" with body=%s' % (url, body)
    req = urllib2.Request(url, body, {"Content-Type": "application/json"})
    try:
        res = urllib2.urlopen(req)
        body = res.read()
        print >> sys.stderr, "INFO HipChat server responded with HTTP status=%d" % res.code
        print >> sys.stderr, "DEBUG HipChat server response: %s" % json.dumps(body)
        return 200 <= res.code < 300
    except urllib2.HTTPError, e:
        print >> sys.stderr, "ERROR Error sending message: %s" % e
        return False


def normalize_bool(value):
    return True if value.lower() in ('1', 'true') else False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        if not send_message(payload.get('configuration')):
            print >> sys.stderr, "FATAL Failed trying to send room notification"
            sys.exit(2)
        else:
            print >> sys.stderr, "INFO Room notification successfully sent"
    else:
        print >> sys.stderr, "FATAL Unsupported execution mode (expected --execute flag)"
        sys.exit(1)
