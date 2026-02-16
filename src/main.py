import boto3
from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from decimal import Decimal


app = FastAPI()

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("claims")


class Claim(BaseModel):
    user: str
    amount: float
    status: str


@app.post("/claims")
def create_claim(claim: Claim):
    claim_id = str(uuid.uuid4())

    table.put_item(
        Item={
            "claimId": claim_id,
            "user": claim.user,
            "amount": Decimal(str(claim.amount)),
            "status": claim.status
        }
    )

    return {"message": "Claim created", "claim_id": claim_id}


@app.get("/claims/{claim_id}")
def get_claim(claim_id: str):
    response = table.get_item(Key={"claim_id": claim_id})
    return response.get("Item", {})
