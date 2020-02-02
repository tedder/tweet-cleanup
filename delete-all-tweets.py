#!/usr/bin/env python3

import twitter
import json
import sys
import datetime
import os

#DRY_RUN = True
DRY_RUN = False
DATA_DIR = os.environ.get('DATA_DIR', '')
DELETED_LOG = os.path.join(DATA_DIR, 'deleted_tweets.json')


class Tweeter:
  def __init__(self):
    self.api = twitter.api.Api(
      consumer_key =       os.environ.get('consumer_key'),
      consumer_secret =    os.environ.get('consumer_secret'),
      access_token_key =   os.environ.get('access_token_key'),
      access_token_secret = os.environ.get('access_token_secret')
    )
  def validate_login(self):
    credinfo = self.api.VerifyCredentials()
    #print(credinfo)
    #print(type(credinfo))
    if not isinstance(credinfo, twitter.models.User) or not credinfo.id:
      raise Exception('eep, we should be logged into Twitter but must not be. login info: {}'.format(credinfo))

tw = Tweeter()
print(f"tw? {tw}")
tw.validate_login()

first_tweet = None
earliest_tweet = 875029297852841984
with open(DELETED_LOG, 'a') as f:
  tw.validate_login()
  us = tw.api.GetUserTimeline(screen_name='tedder42', count=2, exclude_replies=False, include_rts=True)

  if len(us) == 0:
    print("no tweets :/")
    sys.exit(0)
  earliest_tweet = min(us, key=lambda x: x.id).id
  while True:
    us = tw.api.GetUserTimeline(screen_name='tedder42', count=200, max_id=earliest_tweet, exclude_replies=False)

    print("count: {}".format(len(us)))
    if len(us) < 2:
      print(tw.api.rate_limit.__dict__['resources'])
      print(us)
      break

    #print(us[0])
    for st in us:
      #print(st['created_at'], st.get('created_at_seconds'))
      tweet_time = datetime.datetime.utcfromtimestamp(st.created_at_in_seconds)
      delta_time_hours = (datetime.datetime.utcnow()-tweet_time).total_seconds()/(3600)
      if delta_time_hours < 24*7:
        continue
      if st.favorite_count > 10 or 'Look, a newsfeed' in st.text:
        print("loved tweet:", st.AsJsonString())
        continue

      #print(st.AsJsonString())
      ##print(f"{st.id} -- {st.AsJsonString()}")
      #print(st.id)
      print(st.text)
      earliest_tweet = min(earliest_tweet, st.id)
      if not DRY_RUN:
        print(st.AsJsonString(), file=f)
        tw.api.DestroyStatus(st.id)

print("done!")
