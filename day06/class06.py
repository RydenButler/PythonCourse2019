#### Pollster API

## http://elections.huffingtonpost.com/pollster/api/v2
# pip install pollster

## adapted from example.py at https://github.com/huffpostdata/python-pollster

import datetime
import webbrowser
import pollster

api = pollster.Api()

## not sure what a tag is!
tags = api.tags_get() ## list of dictionary-looking objects

## check out the slugs, anyway
for t in tags:
	print(t.slug)

## 2016 president looks good
charts = api.charts_get(tags = '2016-president')
len(charts.items)
## what's in a single chart (aka plot)
charts.items[0]
## navigate through it....
charts.items[0].question.name
## let's check out their plot
webbrowser.open(charts.items[0].url)

## next() does pagination
question_slug = next(c.question.slug for c in charts.items if c.question.n_polls > 30)
question_slug

## grab polls with get request that matches our question_slug 
polls = api.polls_get(
  question = question_slug,
  sort = 'created_at'
)
polls

## Grabbing info from these polls
[p.mode for p in polls.items]

[p.poll_questions[0].question.charts for p in polls.items]

## charts is our first object up above
## grab first one
chart_slug = charts.items[0].slug
trendlines = api.charts_slug_pollster_trendlines_tsv_get(chart_slug)
trendlines

## We can rearrange data too
by_date = trendlines.pivot(index='date', columns='label', values='value').sort_index(0, ascending=False)
by_date

## Now looking at question-level
questions = api.questions_get(
  cursor=None,                             # String | Special string to index into the Array
  tags='2016-president',                   # String | Comma-separated list of tag slugs (most Questions are not tagged)
  election_date=datetime.date(2016, 11, 8) # Date | Date of an election
)
questions

## and responses (question_slug is from above, as well)
question_slug

responses_clean = api.questions_slug_poll_responses_clean_tsv_get(question_slug)
responses_clean




#### Google Maps API

#pip install googlemaps

## https://console.developers.google.com/apis/credentials?project=_
## need geocoding and distance matrix APIs enabled
import imp
import sys

sys.path.insert(0, '/Users/ryden/Dropbox/Coding/Secrets')
imported_items = imp.load_source('goog', '/Users/ryden/Dropbox/Coding/Secrets/start_google.py')

gmaps = imported_items.client

whitehouse = 'The White House'
location = gmaps.geocode(whitehouse)

location[0].keys()
location[0]['geometry'].keys()
location[0]['geometry']['location']

latlong = location[0]['geometry']['location']

destination = gmaps.reverse_geocode(latlong)

## sometimes you have to dig...
print(destination[0]["address_components"][0]["short_name"])

duke = gmaps.geocode('326 Perkins Library, Durham, NC 27708')
duke_loc = duke[0]['geometry']['location']
duke_loc

washu = gmaps.geocode('1 Brookings Dr, St. Louis, MO 63130')
washu_loc = washu[0]['geometry']['location']
distance = gmaps.distance_matrix(duke_loc, latlong)
print(distance['rows'][0]['elements'][0]['distance']['text'])



## Plotting in Google Maps

## https://github.com/vgm64/gmplot
#pip install gmplot
from gmplot import gmplot
# Google_API_Key is the custom file name I gave to my key
from Google_API_Key import api_key as google_key

STL = gmaps.geocode('St. Louis')
STL[0]['geometry']['location']

## latitutde and longitude and "zoom level"
## or location and zoom level (deprecated)

plot1 = gmplot.GoogleMapPlotter(38.6270025, -90.19940419999999, 13)
plot1.apikey = google_key

stl_places = ["Forest Park, St. Louis",
"Missouri Botanical Garden, St. Louis",
"Anheuser Busch, St. Louis",
"Arch, St. Louis"]

def grab_latlng(place):
	x = gmaps.geocode(place)
	return (x[0]["geometry"]["location"]["lat"], x[0]["geometry"]["location"]["lng"])

l = [grab_latlng(i) for i in stl_places]

attraction_lats, attraction_lons = zip(*l)
attraction_lats
attraction_lons

plot1.scatter(attraction_lats, attraction_lons,
	'black',
	size=40,
	marker=True)

# Draw
plot1.draw("my_map.html")




#### Meetup API

#pip install meetup-api

## first arg is folder name, second arg is navigating to file
meetup = imp.load_source('meet', '/Users/ryden/Dropbox/Coding/Secrets/start_meetup.py')
api = meetup.client

## methods we can use
## https://meetup-api.readthedocs.io/en/latest/meetup_api.html#api-client-details

# group object
STL_yoga = api.GetGroup({"urlname" : "STL-Clothing-Optional-Yoga"})

## check out what info is available
STL_yoga.__dict__.keys()

for k in STL_yoga.__dict__.keys():
	print(k)
	print(STL_yoga.__dict__[k])
	print("")

## member object
yoga_members = api.GetMembers({"group_urlname" : "STL-Clothing-Optional-Yoga"})

yoga_members.__dict__.keys()

## member objects
ppl = yoga_members.__dict__["results"]
len(ppl)

yoga_members.__dict__['meta']

mygroups = api.GetGroups({"member_id" : "235714231"})
mygroups.meta
mygroups.results

## more group searches
stlgroups = api.GetFindGroups({"zip" : "63112"})
len(stlgroups)

for g in stlgroups:
	print(g.category["name"])

polgroups = api.GetFindGroups({"zip" : "63112", "text" : "political"})
len(polgroups)

[g.members for g in polgroups]
[g.urlname for g in polgroups]

simgroups = api.GetGroupSimilarGroups({"urlname" : "Great-Conversations"})
len(simgroups)

[g.name for g in simgroups]





#### Twitter API

#pip install tweepy
import tweepy
# http://docs.tweepy.org/en/v3.8.0/api.html

twitter = imp.load_source('twit', '/Users/ryden/Dropbox/Coding/Secrets/start_twitter.py')
api = twitter.client

## See rate limit
limit = api.rate_limit_status()
limit.keys() ## look at dictionary's keys
# prepare for dictionaries all the way down

limit["resources"] ## another dictionary
limit["resources"].keys()
limit["resources"]["tweets"] ## another dictionary!!

for i in limit["resources"]["tweets"].keys():
	print(limit["resources"]["tweets"][i]) ## another dictionary!

## Create user objects
don = api.get_user('realDonaldTrump')
don ## biiiig object 

type(don)
dir(don)

## Trying some of these methods
print(don.id)
print(don.name)
print(don.screen_name)
print(don.location)

## Check his tweets
don.status
don.status.text
don.status._json
don.statuses_count

## Check his followers
don.followers_count

## Gives back user objects
don_20 = don.followers() ## only the first 20!
don_20

[f.screen_name for f in don_20]

don_200 = api.followers(don.id, count = 200) ## up to 200
[f.screen_name for f in don_200]

## A more round-about way, look up each user
don.followers_ids() #creates a list of user ids - up to 5000

for follower_id in don.followers_ids()[0:100]:
	user = api.get_user(follower_id)
	print(user.location)

## Normally count = 200 is limit, let's go around that.
don_statuses = []
for p in range(25):
	don_statuses.extend(api.user_timeline('realDonaldTrump', page = p))

don_statuses
len(don_statuses)

source = [x.source for x in don_statuses]
[x.text for x in don_statuses if x.source == "Twitter for iPhone"]

## Cursor performs pagination easily for you
histweets = [] ## tweet objects
for status in tweepy.Cursor(api.user_timeline, id = 'realDonaldTrump').items(500):
    histweets.append(status)

len(histweets)
histweets

## You should definitely hit the rate limit here.....
hisfollowers = []
for item in tweepy.Cursor(api.followers_ids, 'realDonaldTrump').items():
	hisfollowers.append(item)

len(hisfollowers)