import boto3
from fastapi import FastAPI
from pydantic import BaseModel
from decimal import Decimal
import json
import uuid


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

    # Convert entire object safely to Decimal
    item = json.loads(
        json.dumps(claim.dict()),
        parse_float=Decimal
    )

    item["claimId"] = claim_id

    table.put_item(Item=item)

    return {"message": "Claim created", "claimId": claim_id}


@app.get("/claims/{claim_id}")
def get_claim(claim_id: str):
    response = table.get_item(Key={"claim_id": claim_id})
    return response.get("Item", {})
