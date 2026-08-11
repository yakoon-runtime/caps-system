from y5n.sdk import io, ports


async def main():
    await ports.get("session").detach()
    await io.write("Detached")
