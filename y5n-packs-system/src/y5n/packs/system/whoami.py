from y5n.sdk import ports, runtime


async def main():
    doc = ports.get("document")
    current = await ports.get("session").current()
    user = current.get("user_name") or ""

    result = await doc.render(name="default", state={"user": user})
    await runtime.io.write(result)
