def usage_message():
    return "Usage: !event [add|list|delete] ..."


def invalid_date_message():
    return "❌ Invalid date format. Use ISO 8601 (e.g. 2024-05-07T15:30)."


def add_usage_message():
    return "Usage: !event add <name> <due-date> <info(optional)>"


def event_added_message(event):
    return f"✅ Event '{event.event_name}' added."


def no_events_message():
    return "No events found."

def permission_too_low_message(name):
    return f"please check permissions level \"{name}\" does not have correct permissions to use this command"

def events_list_message(events):
    return "📅 Events:\n" + "\n".join(
        f"[{e.id}] {e.event_name} - assigned: {e.date_assigned}, due: {e.date_due} \nInfo: {e.event_info}"
        for e in events
    )


def delete_usage_message():
    return "Usage: !event delete <id>"


def delete_result_message(deleted):
    return "🗑️ Event deleted." if deleted else "❌ Event not found."


def unknown_action_message():
    return "Unknown action. Use add, list, or delete."


def alarm_message(event):
    # TODO Seperate behaviour for private events
    return "@here Event Alarm!" + "\n" + event.event_name + " is due at " + event.date_due.strftime("%Y-%m-%d %H:%M:%S") + "." + "\n" + "React ⏰ to turn off alarm for event no." + "\n" + str(event.id)

def alarm_off_message(off):
    return "Alarm Off." if off else "Alarm Off Error, Most likely event was not found."