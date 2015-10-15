import sys
import json
import urllib2


def send_message(settings, payload):
    print >> sys.stderr, "DEBUG Sending message with settings %s" % settings

    service_key = settings.get('service_key')
    print >> sys.stderr, "INFO service_key=%s" % (service_key)
    
    url = 'https://events-pagerduty-com-h1wht6shd77e.runscope.net/generic/2010-04-15/create_event.json'
    body = json.dumps(dict(
        details=dict(payload),
        service_key=service_key,
        event_type='trigger',
        description="Splunk Alert: %s" % (payload.get('search_name')),
        client='Splunk',
        client_url= payload.get('results_link')
    ))
    print >> sys.stderr, 'INFO Calling url="%s" with body=%s' % (url, body)
    return True
    if False: 
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

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        if not send_message(payload.get('configuration'), payload):
            print >> sys.stderr, "FATAL Failed trying to send room notification"
            sys.exit(2)
        else:
            print >> sys.stderr, "INFO Room notification successfully sent"
    else:
        print >> sys.stderr, "FATAL Unsupported execution mode (expected --execute flag)"
        sys.exit(1)
