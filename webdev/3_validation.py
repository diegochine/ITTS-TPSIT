from fastapi import FastAPI, Query
from pydantic import Required

app = FastAPI()


@app.get("/email/")
async def validate_email(email: str = Query(default=Required,  # also: default=...,
                                            min_length=5,
                                            max_length=50,
                                            title='Query email',
                                            description='email address to be validated',
                                            regex=r"[a-z0-9\.]+@[a-z]+.(com|it)")):
    return {'message': f'email {email} validated'}
