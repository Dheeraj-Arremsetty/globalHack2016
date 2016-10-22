#!/usr/bin/env python2.7

from twilio.rest import TwilioRestClient

def sendMessage(message, phone_number):
    client = TwilioRestClient(account="AC65f8bda5168de34947f482a09c0f2b98",
                              token="dd32bce6497b19f9f52baf3677fa8192")
    client.messages.create(from_="+12198416729",
                           to="+12198412242",
                           body=message)

if __name__ == '__main__':
    sendMessage("Testing message", "1234567890")
