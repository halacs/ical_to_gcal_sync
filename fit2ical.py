#!/bin/python3
import os
from fitparse import FitFile
from ics import Calendar, Event
from datetime import timezone, timedelta

def get_activity_datetime(fitfile_path):
    """
    Extracts the activity start date-time from a .fit file.
    Returns a UTC datetime object, or None if not found.
    """
    fitfile = FitFile(fitfile_path)

    start_time = None
    duration = 0
    sport = None
    event_name = None
    activity_name = None

    for record in fitfile.get_messages('session'):
        if not start_time:
            start_time = record.get_value('start_time')

        duration += record.get_value('total_elapsed_time')

        if not sport:
            sport = record.get_value('sport')

        if not event_name:
            event_name = record.get_value('event_name')

        if not activity_name:
            activity_name = record.get_value('activity_name')

    #title = f"{sport} - {eventName or activityName or os.path.basename(fitfile_path) or 'Unknown Activity'}"
    title = f"{sport}"

    return title, start_time, timedelta(seconds=duration)

def create_ical_from_fit_files(fit_dir, output_ics='activities.ics'):
    cal = Calendar()
    for filename in os.listdir(fit_dir):
        if filename.lower().endswith('.fit'):
            fit_path = os.path.join(fit_dir, filename)
            title, start_time, duration = get_activity_datetime(fit_path)

            if start_time:
                e = Event()
                e.name = title
                e.begin = start_time
                e.duration = duration
                e.description = f"Imported from {filename}"
                cal.events.add(e)
                print(f"Added event for: {filename} at {start_time} until {start_time + duration}. Duration: {duration}")
            else:
                print(f"Could not extract start time from: {filename}")
    with open(output_ics, 'w') as f:
        f.writelines(cal)

    print(f"\nICS file generated: {output_ics}")

if __name__ == '__main__':
    # Change this to your directory containing .fit files
    input_directory = '/tmp/fit/'
    create_ical_from_fit_files(input_directory, '/tmp/out.ics')
