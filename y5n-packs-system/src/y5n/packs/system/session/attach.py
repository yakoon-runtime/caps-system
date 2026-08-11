from y5n.sdk import context, io, ports


async def main():
    target = context.request().arg(0)
    if not target:
        await io.write("Usage: session attach <key>")
        return

    await ports.get("session").attach(target_key=target)
    await io.write(f"Attached to session {target}")
