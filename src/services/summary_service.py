import json

def summarize_claim(claim_id):
    with open("mocks/notes.json") as f:
        notes = json.load(f)

    if claim_id not in notes:
        return None

    claim_notes = notes[claim_id]
    combined = " ".join(claim_notes)

    return {
        "overall_summary": f"Summary of claim: {combined}",
        "customer_summary": "Your claim is being processed.",
        "adjuster_summary": f"Detailed notes: {combined}",
        "recommended_next_step": "Proceed with inspection."
    }
