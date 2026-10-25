from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic_models import Patient, load_data, save_data, PatientUpdate
import uvicorn
from pydantic import BaseModel, Field, computed_field
from typing import List, Literal, Dict, Annotated
import os
import json



app =FastAPI()




# Home Page

@app.get("/")
def Home():
    return {"Messages": "Welcome"}

@app.get('/details')
def details():
    return {"Details": "This is a Patient Details APP"}


@app.get("/view")
def View_Patient():
    data =load_data()
    return data

@app.get("/patient/{patient_id}")
def Individual_patient(patient_id: str = Path(...,  description="This is Patient ID", example="P001", max_length=100, min_length=4)):
    data = load_data()
    if data.get(patient_id):
        return data.get(patient_id)
    else: 
        raise HTTPException(status_code=404, detail="Patient Not Found", headers="Error")


@app.get("/sort")
def sort_values(sortby: str = Query(..., description="The Feature on which the data will be sorted", example="height"),
                order: str = Query('asc', example='asc')):
    features = ["height", "bmi", "weight", "name", 'state']
    order_features=['asc', 'desc']
    sortby, order = sortby.lower(), order.lower()

    if sortby not in features:
        raise HTTPException(status_code=400, detail=f"enter values from {features}")

    if order not in order_features:
            raise HTTPException(status_code=400, detail=f"enter values from {order_features}")

    order_as = False
    if order.lower() == "desc":
        order_as = True
    

    data =load_data()
    result = sorted(data.values(), key= lambda x: x.get(sortby), reverse=order_as)
    return result


@app.post("/create")
def add_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient id is already there, if the patient is new use diffrent ID")

    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201, content={'messages': f"Patient created sucessfully for id {patient.id}"})


@app.delete("/remove/{patient_id}")
def delete_patient(patient_id: str = Path(description="Patient ID", example="P001")):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f"Patient ID {patient_id} not found, Get valid id")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": f"Patient ID {patient_id} deleted successfully"})


@app.put("/edit/{patient_id}")
def update_patient_information(state: PatientUpdate, patient_id: str=Path(description="Patient ID", example="P005")):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    exisiting_pat_info=data[patient_id]
    updated_data=state.model_dump(exclude_unset=True)

    for k, v in updated_data.items():
        exisiting_pat_info[k]= v
    data[patient_id]=exisiting_pat_info
    save_data(data)
    return JSONResponse(status_code=200, content={"message": f"Patient ID {patient_id} updated successfully"})














if __name__=="__main__":
    uvicorn.run('fastapi_prac.patien_data.main:app', reload=True)




