import asyncio

from pyn8n.n8n_client import N8nClient
from pyn8n.models import *


async def create_credentials():
    settings = N8nSettings()
    # Initialize the client
    client = N8nClient(
        base_url="http://localhost:5678/api/v1",
        api_key=settings.api_key,
    )

    try:
        # Define the credential to create
        new_credential = Credential(
            name="Groq API Key",   # Name of the credential
            type="groqApi",       # Credential type as defined in n8n
            data={"apiKey": "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"}  # Replace with your Groq API Key
        )

        # Create the credential using the client
        created_credential = await client.create_credential(new_credential)

        # Output the created credential
        print(f"Created Credential: {created_credential}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.shutdown()

if __name__ == "__main__":
    asyncio.run(create_credentials())
