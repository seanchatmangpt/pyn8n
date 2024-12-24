import httpx
from pyn8n.n8n_client import N8nClient
from pyn8n.models import *


async def main():
    client = N8nClient(
    )

    try:
        print("=== Starting Workflow Test ===")

        # Use the helper function to create a valid workflow model
        workflow = await Workflow.from_json(file_path="factorial_workflow.json")

        # Create the workflow
        print("Creating a workflow with Cron and Manual triggers...")
        # print(f"   Workflow: {workflow}\n")
        created_workflow = await client.create_workflow(workflow)
        print(f"   Created Workflow: {created_workflow}\n")

        # Activate the workflow
        print("Activating the workflow...")
        activated_workflow = await client.activate_workflow(created_workflow.id)
        print(f"   Activated Workflow: {activated_workflow}\n")

        print("Workflow is ready. You can trigger it manually or wait for the cron schedule.")

    except httpx.HTTPStatusError as exc:
        print(f"HTTP Error: {exc.response.status_code} - {exc.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        await client.shutdown()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
