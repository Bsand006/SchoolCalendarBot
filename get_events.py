from initcalendar import main


def get_list_event(eventnumber, tmin, tmax):
   
    service = main()  # Call calendar api

    events_result = service.events().list(calendarId='charterschool.org_3r1ursppmcobfchc63ghg33u64@group.calendar.google.com',
                                        timeMin=tmin,
                                        timeMax=tmax,
                                        maxResults=eventnumber,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    print(events)
    eventlist = []
   
    if not events:  # If no events are found
        print('No upcoming events found.')
 
    print(f'Getting List of {len(events)} events')  # Print number of events found
   
    for event in events:
            # Create fields for each event
    
        end = event['end'].get('dateTime', event['end'].get('date'))
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_title_summary = event['summary']
        event_description = event['summary']
        html_link = event['htmlLink']
           
        # Load events into eventlist array
        eventlist.append({'start_datetime': start,
                        'end_datetime':end,
                        'eventtitle': event_title_summary,
                        'html_link': html_link,
                        'event_desc': event_description})
        
    print(eventlist)

    return(eventlist)
