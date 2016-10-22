from twilio.rest import TwilioRestClient

def sendMessage(_newJobs):
    client = TwilioRestClient(account="AC65f8bda5168de34947f482a09c0f2b98",
                              token="dd32bce6497b19f9f52baf3677fa8192")
    _str = "Insert Message here"
    #client.messages.create(from_="+13143251480",
     #                      to="+13145831629",
      #                     body=_str)
    client.messages.create(from_="+12198416729",
                           to="+12198412242",
                           body=_str)