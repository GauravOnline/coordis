from commands.base import Command
from services.event_service import EventService
from db.base import get_session
from datetime import datetime
from ui import event_ui


class EventCommand(Command):
    def __init__(self):
        super().__init__(name="event", description="Manage events",
                         roles=["all", "student", "teacher"])

    async def execute(self, ctx, *args):
        if not args:
            await ctx.send(event_ui.usage_message())
            return

        args = args[0]
        action = args[0].lower()

        with get_session() as session:
            service = EventService(session)

            if action == "add":
                if len(args) < 3 or len(args) > 4:
                    await ctx.send("Usage: !event add <name> <due-date> <info(optional)>")
                    return
                name = args[1]
                try:
                    assigned = datetime.now()
                    due = datetime.fromisoformat(args[2])
                    info = args[3] if len(args) > 3 else "No extra event info provided."
                    event = service.create_event(name, assigned, due, info)
                    await ctx.send(event_ui.event_added_message(event))
                except ValueError:
                    await ctx.send(event_ui.invalid_date_message())

            elif action == "list":
                events = service.list_events()
                await ctx.send(event_ui.no_events_message() if not events else event_ui.events_list_message(events))

            elif action == "delete":
                if len(args) < 2 or not args[1].isdigit():
                    await ctx.send(event_ui.delete_usage_message())
                    return
                deleted = service.delete_event(int(args[1]))
                await ctx.send(event_ui.delete_result_message(deleted))

            else:
                await ctx.send(event_ui.unknown_action_message())

    def get_help_text(self):
        return f"!{self.name} [add|list|delete] <name> <due-date> <info(optional)> - {self.description}"
