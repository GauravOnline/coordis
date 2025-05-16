from commands.base import Command
from services.event_service import EventService
from db.base import get_session
from datetime import datetime


class EventCommand(Command):
    def __init__(self):
        super().__init__(name="event", description="Manage events",
                         roles=["all", "student", "teacher"])

    async def execute(self, ctx, *args):
        if not args:
            await ctx.send("Usage: !event [add|list|delete] ...")
            return

        args = args[0]
        action = args[0].lower()

        with get_session() as session:
            service = EventService(session)

            if action == "add":
                print(args)
                if len(args) < 2:
                    await ctx.send("Usage: !event add <name> <due-date>")
                    return
                name = args[1]
                try:
                    assigned = datetime.now()
                    due = datetime.fromisoformat(args[2])
                    event = service.create_event(name, assigned, due)
                    await ctx.send(f"✅ Event '{event.event_name}' added.")
                except ValueError:
                    await ctx.send("❌ Invalid date format. Use ISO 8601 (e.g. 2024-05-07T15:30).")

            elif action == "list":
                events = service.list_events()
                if not events:
                    await ctx.send("No events found.")
                else:
                    msg = "\n".join(
                        f"[{e.id}] {e.event_name} - assigned: {e.date_assigned}, due: {e.date_due}" for e in events
                    )
                    await ctx.send(f"📅 Events:\n{msg}")

            elif action == "delete":
                if len(args) < 2 or not args[1].isdigit():
                    await ctx.send("Usage: !event delete <id>")
                    return
                deleted = service.delete_event(int(args[1]))
                await ctx.send("🗑️ Event deleted." if deleted else "❌ Event not found.")

            else:
                await ctx.send("Unknown action. Use add, list, or delete.")

    def get_help_text(self):
        """
        Get help text for this command.

        Returns:
            str: Help text describing the command usage
        """
        return f"!{self.name} [add|list|delete] <name> <due-date> - {self.description}"
