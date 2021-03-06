"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            SELECT
                    *
                FROM EVENTS_BY_USER
                    """)

            dataset = dict_fetch_all(db_cursor)

            events_by_user = []

            for row in dataset:

                event = {
                    "id": row['id'],
                    "date": row['date'],
                    "time": row['time'],
                    "game_name": row['title'],
                    "description": row['description']
                }

            # See if the gamer has been added to the events_by_user list already
                user_dict = None
                for user_event in events_by_user:
                    if user_event['gamer_id'] == row['organizer_id']:
                        user_dict = user_event

                if user_dict:
                    # If the user_dict is already in the events_by_user list, append the game to the events list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the events_by_user list, create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['organizer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })

        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
