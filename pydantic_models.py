from pydantic import BaseModel, computed_field, Field
from typing import Literal, Annotated, Dict, Optional
import json

class Patient(BaseModel):
    id:  Annotated[str, Field(...,description="Patient id", examples=["P010"])]
    name:Annotated[str, Field(...,description="Name of the patient", examples=["Ram Charan"])]
    height: Annotated[float , Field(...,description="Height of the patient", examples=[5.5])]
    weight: Annotated[float, Field(...,description="Weight of the patient", examples=[61.1])]
    state: Annotated[str, Field(description="State of the patient", examples=['Westbengal'])]
    disease: Annotated[str, Field(description="disease of the patient", examples=['Diabetis'])]

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight / (self.height*0.38) ** 2, 2)



class PatientUpdate(BaseModel):        
    name: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    state: Optional[str] = None
    disease: Optional[str] = None






def load_data():
    with open(r"C:\Users\csc\Desktop\Kuntal_work\Pandas_practice\fastapi_prac\patient_data\patient.json", 'r') as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open(r"C:\Users\csc\Desktop\Kuntal_work\Pandas_practice\fastapi_prac\patient_data\patient.json", 'w') as f:
        json.dump(data, f)