import httpx

from pyn8n.n8n_client import N8nClient
from pyn8n.models import *


def get_valid_workflow_with_webhook(webhook_url: str) -> Workflow:
    """
    Creates a valid Workflow model with a Webhook trigger node.

    Args:
        webhook_url (str): The test webhook URL to configure the Webhook node.

    Returns:
        Workflow: A Workflow model ready for creation and activation.
    """
    # Define a Webhook trigger node
    webhook_node = WorkflowNode(
        id="webhook-node-1",
        name="Webhook Trigger",
        type="n8n-nodes-base.webhook",
        typeVersion=1.0,
        position=[0, 0],
        parameters={
            "path": "test-webhook",
            "httpMethod": "POST",
            "responseMode": "onReceived",
            "responseData": {
                "contentType": "application/json",
                "responseData": {"key": "value"}
            },
        },
        credentials={},  # Explicitly setting credentials as an empty object
    )

    # Define a Set node
    set_node = WorkflowNode(
        id="set-node-1",
        name="Set Node",
        type="n8n-nodes-base.set",
        typeVersion=1.0,
        position=[200, 0],
        parameters={
            "values": {
                "string": [{"name": "exampleField", "value": "Webhook received"}]
            }
        },
        credentials={},  # Explicitly setting credentials as an empty object
    )

    # Define the connections
    connections = {
        "webhook-node-1": {  # Webhook Trigger
            "main": [[{"node": "set-node-1", "type": "main", "index": 0}]]  # Webhook -> Set Node
        }
    }

    # Create the workflow
    workflow = Workflow(
        name="Webhook Test Workflow",
        nodes=[webhook_node, set_node],
        connections=connections,
        settings=WorkflowSettings(),
        tags=[],
    )

    return workflow


async def main():
    print("=== Workflow Model Test ===")
    client = N8nClient(
        base_url="http://localhost:5678/api/v1",
    )

    print("Creating a valid workflow model with a Webhook trigger...")
    wf = get_valid_workflow_with_webhook("http://localhost:5678/test-webhook")
    print(await wf.to_yaml())


async def main2():
    client = N8nClient(
        base_url="http://localhost:5678/api/v1",
    )

    try:
        print("=== Starting Workflow Test ===")

        # Use the helper function to create a valid workflow model
        workflow_model = get_valid_workflow_with_webhook("http://localhost:5678/test-webhook")

        # Create the workflow
        print("Creating a workflow with a Webhook trigger...")
        created_workflow = await client.create_workflow(workflow_model)
        print(f"   Created Workflow: {created_workflow}\n")

        # Activate the workflow
        print("Activating the workflow...")
        activated_workflow = await client.activate_workflow(created_workflow.id)
        print(f"   Activated Workflow: {activated_workflow}\n")

        # You can now test the webhook by sending a POST request to the Webhook URL
        webhook_test_url = f"http://localhost:5678/webhook/test-webhook"
        print(f"Send a POST request to {webhook_test_url} to test the webhook.")

    except httpx.HTTPStatusError as exc:
        print(f"HTTP Error: {exc.response.status_code} - {exc.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        await client.shutdown()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())