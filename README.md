# Next steps
1. Waiting list with date_joined
2. Integrate testing


# Features
Features ideas:
1. Waiting list
   1. ~~Add waiting list when event is full~~
   2. Must use another model to keep order of waiting list https://docs.djangoproject.com/en/dev/topics/db/models/#intermediary-manytomany 
   3. Auto-fill oldest user in the waiting list (and notify them)
2. Add possibility to add a reminder to participants X days before the event with confirmation by the participants
   1. Celery sounds like the way to go https://docs.celeryq.dev/en/latest/django/
   2. We cound schedule a daily process that goes through all the users and defines all emails that need to be send (to avoid sending more than 1 email/day per user)
3. Add maps API to help fill the event location - https://locationiq.com/
4. Add filtering activities/categories
5. Add ordering for activities/categories
6. Add statistics of activities to home page
8. Add participation rate as a score to participants

# Non-essential features
1. Allow activity creator to reach out to users of activity.
2. Add scoring system to users 
3. Add competitions/tournaments
4. Add **comments** to activities (not sure it is a good idea)
5. Allow selection of circle in profile picture



# Issues
1. Calendar widget has bad display on mobile
2. After joinning activity, needs to go back twice to go back


# TODOs
1. Add ~20 Categories with pictures, store them in static
2. Make date picker skip minutes in 5/10 minute chunks
3. Keep an initial data dump for the correct functionality of the website 
