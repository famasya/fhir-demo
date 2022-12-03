import asyncio
import json
from fhirpy import AsyncFHIRClient
from rich import print

def pprint(body):
    print(json.dumps(body, sort_keys=True, indent=2))

async def main():
    # Create an instance
    client = AsyncFHIRClient(
        'https://server.fire.ly/',
        'Bearer <TOKEN>'
    )

    # Get particular patient
    patient = await client.reference('Patient', '1ca130bc-29c1-4f56-9730-f3cbecd9fca0').to_resource()
    print('Patient ID : 1ca130bc-29c1-4f56-9730-f3cbecd9fca0')
    print(patient.serialize())

    # Get particular patient (another way)
    patient_id = 'bb6cde30-be19-4b06-8f41-5fb682ba1f9f'
    patient = await client.resources('Patient').search(_id=patient_id).first()
    print('Patient ID : {}'.format(patient_id))
    print(patient)

    # Get all observations for given patient
    observations = await client.resources('Observation').search(patient=patient_id).fetch_all()
    print('Observations for given patient')
    print(observations)

    # Search for patients
    patient_resources = client.resources('Patient')  # Return lazy search set
    patients = await patient_resources.search(birthdate__gt='1944', birthdate__lt='2020').fetch() # Only fetch first page
    print('Patients born between 1944-2020 (first page)')
    print(patients)

    # Count patients born in given year
    patients_count = await patient_resources.search(birthdate__gt='1944', birthdate__lt='2020').count()
    print('Amount of patients born between 1944-2020')
    print(patients_count)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
