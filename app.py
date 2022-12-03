from random import randint
import requests as requests
from sanic import Sanic
from sanic.log import logger
from sanic.response import json, text

import json as jsondump
from fhirpy import SyncFHIRClient
from fhirpy.base.exceptions import ResourceNotFound

app = Sanic(__name__)
fhir_base_url = 'https://server.fire.ly/'
client_sync = SyncFHIRClient(
    fhir_base_url,
    'Bearer <TOKEN>'
)

# Utility function for pretty-print
def pprint(body):
    print(jsondump.dumps(body, sort_keys=True, indent=2))

# Always run in sync
@app.get('/patient/<patient_id>')
def get_patient(patient_id):
    try:
        patient = client_sync.reference('Patient', patient_id).to_resource()
        return json(patient)
    except ResourceNotFound:
        return json({
            'message': 'Resource not found'
        }), 404
    except:
        return json({
            'message': 'Cannot handle this request'
        }), 400

'''
An asynchronous function to fetch observations
and write to a file to mimic database operation
'''
async def fetch_observations(patient_id):
    try:
        observations = client_sync.resources('Observation')
        observations = observations.search(patient=patient_id).fetch_all()

        # If no resources found, raise exception
        if not observations:
            raise ResourceNotFound            

        # Write to a file
        with open("observations.json", "w") as outfile:
            outfile.write(jsondump.dumps(observations, indent=2))
    except ResourceNotFound:
        logger.warning({'message': 'Resource not found'})
    except Exception as e:
        logger.error(e)

# Run observations in async
@app.get('/observations/<patient_id>')
def get_observation(request, patient_id):
    try:
        app.add_task(fetch_observations(patient_id=patient_id))
        return json({
          'message': 'OK'
        })
        return observations
    except ResourceNotFound:
        return json({
            'message': 'Resource not found'
        }), 404
    except:
        return json({
            'message': 'Cannot handle this request'
        }), 400

# Run observations in sync
@app.get('/observations-sync/<patient_id_sync>')
def get_observation_sync(request, patient_id_sync):
    try:
        observations = client_sync.resources('Observation')
        observations = observations.search(patient=patient_id_sync).fetch_all()
        return json(observations)
    except ResourceNotFound:
        return json({
            'message': 'Resource not found'
        }), 404
    except:
        return json({
            'message': 'Cannot handle this request'
        }), 400

if __name__ == '__main__':
    app.run(port=8000, debug=True, auto_reload=True)
