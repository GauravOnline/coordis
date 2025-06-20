from commands.base import Command
from services.event_service import EventService
from db.base import get_session
from datetime import datetime
from ui import event_ui
from core.constants import USAGE_MESSAGE_DISPLAY_TIME, FEEDBACK_MESSAGE_DISPLAY_TIME, ERROR_MESSAGE_DISPLAY_TIME


class EventCommand(Command):
    def __init__(self):
        super().__init__(name="event", description="Manage events",
                         roles=["student", "teacher"])

    async def execute(self, ctx, *args):
        if not args:
            await ctx.send(event_ui.usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
            return
        try:
            args = args[0]
            action = args[0].lower()
        except IndexError:
            await ctx.send(event_ui.usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
            return
        if (EventCommand.check_permission_role(self,ctx) == 0):
                print("\n\nits a 0\n\n")
                await ctx.send(event_ui.permission_too_low_message(ctx.author.name), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)
                return
        with get_session() as session:
            service = EventService(session)

            if action == "add":
                if len(args) < 3 or len(args) > 4:
                    await ctx.send(event_ui.add_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
                    return
                name = args[1]
                try:
                    assigned = datetime.now()
                    due = datetime.fromisoformat(args[2])
                    info = args[3] if len(args) > 3 else "No extra event info provided."
                    event = service.create_event(name, assigned, due, info)
                    await ctx.send(event_ui.event_added_message(event), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)
                except ValueError:
                    await ctx.send(event_ui.invalid_date_message(), delete_after=ERROR_MESSAGE_DISPLAY_TIME)

            elif action == "list":
                events = service.list_events()
                if not events:
                    await ctx.send(event_ui.no_events_message(), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)
                else:
                    await ctx.send(event_ui.events_list_message(events))

            elif action == "delete":
                if len(args) < 2 or not args[1].isdigit():
                    await ctx.send(event_ui.delete_usage_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)
                    return
                deleted = service.delete_event(int(args[1]))
                await ctx.send(event_ui.delete_result_message(deleted), delete_after=FEEDBACK_MESSAGE_DISPLAY_TIME)

            else:
                await ctx.send(event_ui.unknown_action_message(), delete_after=USAGE_MESSAGE_DISPLAY_TIME)

    def get_help_text(self):
        return f"!{self.name} [add|list|delete] <name> <due-date> <info(optional)> - {self.description}"
