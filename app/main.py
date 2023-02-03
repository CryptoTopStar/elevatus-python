from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional
from pymongo.collection import ReturnDocument
from app.config import settings
from app.routers import user, auth
from app.database import User, Candidate
from app import oauth2
from app.database import User
from app.serializers.userSerializers import userEntity, userResponseTestEntity
from app.serializers.candidateSerializers import candidateEntity, candidateListEntity
from . import schemas, utils
from app.oauth2 import AuthJWT
from datetime import datetime, timedelta
from random import randbytes
from bson.objectid import ObjectId
import os
import csv
import hashlib


app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')


# Create /user endpoint with the POST method
@app.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.UserSchema, request: Request):
    # Check if user already exist
    user = User.find_one({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
 
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at

    result = User.insert_one(payload.dict())
    print(payload.email.lower())
    print(result.inserted_id)
    new_user = User.find_one({'_id': result.inserted_id})
    data = userResponseTestEntity(new_user)
    return {"new_user":data}


# Create /cadidate endpoint with the POST method
@app.post('/candidate', status_code=status.HTTP_201_CREATED)
async def create_candidate(payload: schemas.CandidateSchema, user_id: str = Depends(oauth2.require_user)):
    # Check if candidate already exist
    candidate = Candidate.find_one({'email': payload.email.lower()})
    if candidate:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Candidate already exist')

    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at

    result = Candidate.insert_one(payload.dict())
    new_candidate = Candidate.find_one({'_id': result.inserted_id})
    data = candidateEntity(new_candidate)

    return {"new_candidate":data}


# Get /cadidate endpoint with the GET method
@app.get('/candidate/{id}', status_code=status.HTTP_201_CREATED)
async def get_candidate(id: str, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")

    candidate = Candidate.find_one({'_id': ObjectId(id)})
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with this id: {id} found")
    data = candidateEntity(candidate)
    return {"candidate":data}
  

# Update /cadidate endpoint with the PUT method
@app.put('/candidate/{id}', status_code=status.HTTP_201_CREATED)
async def update_candidate(id: str,  payload: schemas.CandidateSchema, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid id: {id}")
    updated_candidate = Candidate.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    
    data = candidateEntity(updated_candidate)
    return {"candidate":data}



# Delete /cadidate endpoint with the DELETE method
@app.delete('/candidate/{id}', status_code=status.HTTP_201_CREATED)
async def delete_candidate(id: str, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid id: {id}")
    deleted_candidate = Candidate.find_one_and_delete({'_id': ObjectId(id)})
    if not deleted_candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# Get /all-cadidate endpoint with the GET method
@app.get('/all-candidates', status_code=status.HTTP_201_CREATED)
async def get_all_candidate(request: Request, user_id: str = Depends(oauth2.require_user)):
    key = request.query_params.multi_items()[0][0]
    value = request.query_params.multi_items()[0][1]
    
    candidates = Candidate.find({key: value})
    
    if not candidates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No candidates found")
    data = candidateListEntity(candidates)
    return {"candidates":data}
   

# Get /generate-report endpoint with the GET method
@app.get('/generate-report', status_code=status.HTTP_201_CREATED)
async def generate_report():
    # making csv file and send it
    today = datetime.today()
    today = today.strftime("%m-%d-%Y")
    
    # make an API call to the MongoDB server
    mongo_docs = Candidate.find()
    if not mongo_docs:
        return {"msg":"fail"}

    fieldnames = list(mongo_docs[0].keys())
    fieldnames.remove('_id')

    # compute the output file directory and name
    filename = f'output/csv/candidate_data-{today}.csv'
    isExist = os.path.exists(filename)

    if isExist is False:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(mongo_docs)

    def iterfile():  
        with open(filename, mode="rb") as file_csv:  
            yield from file_csv  

    return StreamingResponse(iterfile(), media_type="text/csv")

