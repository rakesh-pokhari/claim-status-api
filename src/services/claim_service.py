import json

def get_claim(claim_id):
    with open("mocks/claims.json") as f:
        claims = json.load(f)

    for claim in claims:
        if claim["id"] == claim_id:
            return claim

    return None
