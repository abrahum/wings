from wings import new_world_with_time

if __name__ == "__main__":
    import asyncio

    async def run():
        world = new_world_with_time()
        await world.process()
        await asyncio.sleep(1)
        await world.process()
        await asyncio.sleep(1)

    asyncio.run(run())
