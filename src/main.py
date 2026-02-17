import boto3
from fastapi import FastAPI, Body
from pydantic import BaseModel
from decimal import Decimal
import json
import uuid


app = FastAPI()

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("claims")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")



class Claim(BaseModel):
    user: str
    amount: float
    status: str


@app.post("/claims")
def create_claim(claim: Claim):

    claim_id = str(uuid.uuid4())

    table.put_item(
        Item={
            "claim_id": claim_id,
            "user": claim.user,
            "amount": Decimal(str(claim.amount)),
            "status": claim.status
        }
    )

    return {"message": "Claim created", "claimId": claim_id}

@app.post("/analyze")
def analyze_claim(payload: dict = Body(...)):

    text = payload.get("text")

    if not text:
        return {"error": "text field required"}

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    return result

@app.get("/claims/{claim_id}")
def get_claim(claim_id: str):
    response = table.get_item(Key={"claim_id": claim_id})
    return response.get("Item", {})
