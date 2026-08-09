"""events show — inspect a single event (ADR-17 Phase 3).

Shows the full record of one event: kind, timestamp, payload, and the
context envelope (actor, session, command, trace) it carried.
"""

from y5n.runtime.api.naming import Key
from y5n.sdk import context, io, store


async def main():
    ctx = context.current()
    args = ctx.args
    if not args:
        await io.write("Usage: events show <id>")
        return

    event_id = args[0]
    key = Key.from_parts("system", "activity", "global", event_id)

    db = store()
    history = await db.history(key=key)
    if not history:
        await io.write(f"No event found: {event_id}")
        return

    rev = history[-1]
    data = rev.get("data") or {}
    envelope = rev.get("context") or {}

    await io.write(f"Event {event_id}", mode="append")
    await io.write(f"  kind:    {data.get('kind', '?')}", mode="append")
    await io.write(f"  ts:      {rev.get('ts')}", mode="append")

    payload = data.get("payload")
    if payload:
        await io.write(f"  payload: {payload}", mode="append")

    if envelope:
        actor = envelope.get("actor") or {}
        sess = envelope.get("session") or {}
        cmd = envelope.get("command") or {}
        await io.write("  context:", mode="append")
        await io.write(
            f"    actor:   {actor.get('name') or actor.get('id') or '?'}",
            mode="append",
        )
        await io.write(f"    session: {sess.get('key') or '?'}", mode="append")
        if cmd.get("path"):
            await io.write(f"    command: {cmd.get('path')}", mode="append")
