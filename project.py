import sys

import import_data
import insert_admin
import add_venue
import reserve_slot
import cancel_reservation
import update_event
import delete_organizer
import available_events
import popular_event_types
import participant_schedule
import organizer_stats
import venue_events


COMMANDS = {
    "import": import_data.import_data,
    "insertAdmin": insert_admin.insert_admin,
    "addVenue": add_venue.add_venue,
    "reserveSlot": reserve_slot.reserve_slot,
    "cancelReservation": cancel_reservation.cancel_reservation,
    "updateEvent": update_event.update_event,
    "deleteOrganizer": delete_organizer.delete_organizer,
    "availableEvents": available_events.available_events,
    "popularEventTypes": popular_event_types.popular_event_types,
    "participantSchedule": participant_schedule.participant_schedule,
    "organizerStats": organizer_stats.organizer_stats,
    "venueEvents": venue_events.venue_events,
}


def print_result(result):
    if isinstance(result, bool):
        print("Success" if result else "Fail")
    else:
        for row in result:
            print(",".join("NULL" if value is None else str(value) for value in row))


def main():
    command = sys.argv[1]
    args = [None if arg == "NULL" else arg for arg in sys.argv[2:]]
    result = COMMANDS[command](args)
    print_result(result)


if __name__ == "__main__":
    main()
