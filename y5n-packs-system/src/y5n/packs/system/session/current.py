from y5n.sdk import context, io, ports


async def main():
    rows = await ports.get("session").list()
    current_key = context.session().key
    current = next((r for r in rows if r["key"] == current_key), None)

    if current:
        await io.write(f"Session:  {current_key}")
        await io.write(
            f"clients={current['clients']}  "
            f"homes={current['homes']}  flows={current['flows']}"
        )
    else:
        await io.write(f"Session:  {current_key}")
