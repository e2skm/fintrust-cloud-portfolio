import json
import boto3

# AWS Clients
comp = boto3.client("comprehend", region_name="af-south-1")
sqs = boto3.client("sqs", region_name="af-south-1")

# Replace ACCOUNT_ID with your AWS Account ID
URGENT_QUEUE_URL = (
    "https://sqs.af-south-1.amazonaws.com/ACCOUNT_ID/fintrust-support-urgent"
)
STANDARD_QUEUE_URL = (
    "https://sqs.af-south-1.amazonaws.com/ACCOUNT_ID/fintrust-support-standard"
)


def redact_pii(text):
    """
    Detect and redact PII from support ticket text.
    Returns redacted text and list of detected PII types.
    """
    response = comp.detect_pii_entities(
        Text=text,
        LanguageCode="en"
    )

    entities = response["Entities"]

    # Sort descending so offsets don't shift
    entities.sort(key=lambda e: e["BeginOffset"], reverse=True)

    detected_types = list({e["Type"] for e in entities})
    text_chars = list(text)

    for entity in entities:
        replacement = f'[{entity["Type"]}]'
        text_chars[
            entity["BeginOffset"]:entity["EndOffset"]
        ] = list(replacement)

    return "".join(text_chars), detected_types


def process_support_ticket(ticket_text):
    """
    Process a support ticket:
    1. Redact PII
    2. Analyse sentiment
    3. Route to the correct SQS queue
    4. Return routing summary
    """

    # Step 1: Redact PII
    redacted_text, pii_types = redact_pii(ticket_text)

    # Step 2: Detect sentiment
    sentiment_response = comp.detect_sentiment(
        Text=ticket_text,
        LanguageCode="en"
    )

    sentiment = sentiment_response["Sentiment"]

    # Step 3: Determine queue
    queue_url = (
        URGENT_QUEUE_URL
        if sentiment == "NEGATIVE"
        else STANDARD_QUEUE_URL
    )

    message = {
        "redacted_text": redacted_text,
        "sentiment": sentiment,
        "pii_types_found": pii_types,
        "priority": "HIGH"
        if sentiment == "NEGATIVE"
        else "STANDARD"
    }

    # Step 4: Send to SQS
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )

    return message


if __name__ == "__main__":
    sample_ticket = (
        "My name is Sipho Nkosi and my account number is ACC-7823041. "
        "I contacted you from 0835551234 because I cannot access my funds."
    )

    result = process_support_ticket(sample_ticket)

    print(json.dumps(result, indent=2))