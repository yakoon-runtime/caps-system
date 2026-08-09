"""events list — show the runtime's history (ADR-17 Phase 3).

Lists activity events across all packs, newest first. Audit is not a
subsystem; it is a saved view over the Event Store.
"""

from y5n.runtime.api.naming import Namespace
from y5n.runtime.store.event.models import IndexKey
from y5n.sdk import context, io, store


async def main():
    req = context.request()
    limit = int(req.option("limit", default=20))

    db = store()
    keys, _ = await db.scan(
        namespace=Namespace("system", "activity", "global"),
        index_key=IndexKey("all"),
        value="1",
    )
    if not keys:
        await io.write("No events recorded.")
        return

    rows = []
    for key in keys:
        history = await db.history(key=key)
        if not history:
            continue
        rev = history[-1]
        data = rev.get("data") or {}
        rows.append((rev.get("ts"), str(key), data))

    rows.sort(key=lambda x: x[0] or "", reverse=True)
    rows = rows[:limit]

    await io.write("Events:", mode="append")
    for ts, key, data in rows:
        kind = data.get("kind", "?")
        short_id = key.rsplit("#", 1)[-1][:8]
        await io.write(f"  {short_id}  {kind}  {ts}", mode="append")
