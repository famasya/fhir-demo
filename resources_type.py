from typing import TypedDict

class PatientResource(TypedDict):
  id: list
  gender: str
  birthDate: str
  meta: dict
  text: dict
  extension: list
  identifier: list
  name: list
  telecom: list
  address: list
  communication: list
