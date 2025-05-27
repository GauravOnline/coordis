def usage_message():
    return "Usage: !event [add|list|delete] ..."


def invalid_date_message():
    return "❌ Invalid date format. Use ISO 8601 (e.g. 2024-05-07T15:30)."


def event_added_message(event):
    return f"✅ Event '{event.event_name}' added."


def no_events_message():
    return "No events found."


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
