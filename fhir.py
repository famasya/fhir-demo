import asyncio
from fhirpy import AsyncFHIRClient


async def main():
    # Create an instance
    client = AsyncFHIRClient(
        'https://server.fire.ly/',
        'Bearer <TOKEN>'
    )

    # Search for patients
    resources = client.resources('Patient')  # Return lazy search set
    resources = resources.search(birthdate__gt='1944', birthdate__lt='2020')
    patients = await resources.fetch()  # Returns list of AsyncFHIRResource

    print(patients[0].serialize())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
