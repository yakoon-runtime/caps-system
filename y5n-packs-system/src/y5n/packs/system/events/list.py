"""events list — show the runtime's history (ADR-17 Phase 3).

Lists activity events across all packs, newest first. Audit is not a
subsystem; it is a saved view over the Event Store.
"""

from y5n.runtime.api.naming import Namespace
from y5n.runtime.store.event.models import IndexKey
from y5n.sdk import io
from y5n.sdk import store as store_factory


async def main():
    store = store_factory()

    results = await store.scan(
        namespace=Namespace("system", "activity", "global"),
        index_key=IndexKey("all"),
        value="1",
    )
    if not results:
        await io.write("No events recorded.")
        return

    rows = []
    for r in results:
        if r is None or r.key is None:
            continue
        history = await store.history(key=r.key)
        if not history:
            continue
        rev = history[-1]
        data = rev.get("data") or {}
        rows.append((rev.get("ts"), str(r.key), data))

    rows.sort(key=lambda x: x[0] or "", reverse=True)

    await io.write("Events:", mode="append")
    for ts, key, data in rows:
        kind = data.get("kind", "?")
        short_id = key.rsplit("#", 1)[-1][:8]
        await io.write(f"  [{short_id}] {kind}  {ts}", mode="append")
