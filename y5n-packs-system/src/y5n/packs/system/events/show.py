"""events show — inspect a single event (ADR-17 Phase 3).

Shows the full record of one event: kind, timestamp, payload, and the
context envelope (actor, session, command, trace) it carried.

The id may be abbreviated (e.g. the short id shown by ``events list``);
the full event id is resolved from the store index.
"""

from y5n.runtime.api.naming import Key, Namespace
from y5n.runtime.store.event.models import IndexKey
from y5n.sdk import context, io, store


async def _resolve_event_key(db, event_id: str) -> tuple[Key | None, list[str]]:
    """Resolve a (possibly abbreviated) event id to its full key.

    Returns (key, matches). Matches lists every full id whose prefix is
    ``event_id``; the caller decides how to render 0 / 1 / many hits
    (Git-style prefix resolution).
    """
    keys, _ = await db.scan(
        namespace=Namespace("system", "activity", "global"),
        index_key=IndexKey("all"),
        value="1",
    )
    matches = [key for key in keys if key.id.startswith(event_id)]
    if len(matches) == 1:
        return matches[0], [key.id for key in matches]
    return None, [key.id for key in matches]


async def main():
    req = context.request()
    if not req.has_args():
        await io.write("Usage: events show <id>")
        return

    event_id = req.arg(0)

    db = store.get("runtime")

    key, matches = await _resolve_event_key(db, event_id)
    if key is None:
        if not matches:
            await io.write(f"No event found: {event_id}")
            return
        await io.write(f"Ambiguous event id '{event_id}'.")
        await io.write("Matches:")
        for match in matches:
            await io.write(f"  {match[:8]}  {match}", mode="append")
        return

    history = await db.history(key=key)
    if not history:
        await io.write(f"No event found: {event_id}")
        return

    rev = history[-1]
    data = rev.get("data") or {}
    envelope = rev.get("context") or {}

    await io.write(f"Event {key.id[:8]}", mode="append")
    await io.write(f"  id:      {key.id}", mode="append")
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
