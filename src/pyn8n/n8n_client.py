import asyncio
import httpx
from typing import Any, Dict, List, Optional

from apiclient_pydantic import serialize_all_methods
from pydantic import BaseModel

from pyn8n.models import *


# ---------------------------
# Utility Functions
# ---------------------------

def get_json(response: httpx.Response) -> Any:
    """
    Raise an exception for non-success status codes and return the JSON content.
    """
    response.raise_for_status()
    return response.json()


# ---------------------------
# N8nClient Class
# ---------------------------

@serialize_all_methods
class N8nClient:
    def __init__(self, base_url: str = None, api_key: str = None, timeout: float = 10.0):
        settings = N8nSettings()
        self.base_url = base_url or f"{settings.protocol}://{settings.host}:{settings.port}{settings.base_path}"
        self.api_key = api_key or N8nSettings().api_key

        self.timeout = timeout

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "X-N8N-API-KEY": self.api_key,
                "Accept": "application/json"
            },
            timeout=self.timeout,
        )

    #
    # --------------
    # Workflow Endpoints
    # --------------
    #

    async def get_workflows(
        self,
        active: Optional[bool] = None,
        tags: Optional[str] = None,
        name: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> WorkflowList:
        """
        GET /workflows
        Retrieve all workflows, optionally filtered.
        """
        params: Dict[str, Any] = {}
        if active is not None:
            params["active"] = active
        if tags is not None:
            params["tags"] = tags
        if name is not None:
            params["name"] = name
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = await self.client.get("/workflows", params=params)
        return WorkflowList(**get_json(response))

    async def create_workflow(self, workflow: Workflow) -> Workflow:
        """
        POST /workflows
        Create a workflow.
        """
        response = await self.client.post("/workflows", json=workflow.model_dump(exclude_unset=True, exclude={"id", "tags", "createdAt", "updatedAt"}))
        return Workflow(**get_json(response))

    async def get_workflow(self, workflow_id: str) -> Workflow:
        """
        GET /workflows/{id}
        Retrieve a workflow by ID.
        """
        response = await self.client.get(f"/workflows/{workflow_id}")
        return Workflow(**get_json(response))

    async def update_workflow(self, workflow_id: str, workflow: Workflow) -> Workflow:
        """
        PUT /workflows/{id}
        Update a workflow.
        """
        # Remove read-only fields like `id` before sending the update payload
        payload = workflow.model_dump(exclude_unset=True, exclude={"id", "tags", "createdAt", "updatedAt"})
        response = await self.client.put(f"/workflows/{workflow_id}", json=payload)
        return Workflow(**get_json(response))

    async def delete_workflow(self, workflow_id: str) -> Workflow:
        """
        DELETE /workflows/{id}
        Delete a workflow. Returns the deleted workflow object.
        """
        response = await self.client.delete(f"/workflows/{workflow_id}")
        return Workflow(**get_json(response))

    async def activate_workflow(self, workflow_id: str) -> Workflow:
        """
        POST /workflows/{id}/activate
        Activate a workflow.
        """
        response = await self.client.post(f"/workflows/{workflow_id}/activate")
        return Workflow(**get_json(response))

    async def deactivate_workflow(self, workflow_id: str) -> Workflow:
        """
        POST /workflows/{id}/deactivate
        Deactivate a workflow.
        """
        response = await self.client.post(f"/workflows/{workflow_id}/deactivate")
        return Workflow(**get_json(response))

    async def transfer_workflow(self, workflow_id: str, destination_project_id: str) -> Dict[str, Any]:
        """
        PUT /workflows/{id}/transfer
        Transfer a workflow to another project.
        """
        payload = {"destinationProjectId": destination_project_id}
        response = await self.client.put(f"/workflows/{workflow_id}/transfer", json=payload)
        return get_json(response)

    #
    # --------------
    # Execution Endpoints
    # --------------
    #

    async def get_executions(
        self,
        status: Optional[str] = None,
        workflow_id: Optional[str] = None,
        project_id: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> ExecutionList:
        """
        GET /executions
        Retrieve all executions, optionally filtered.
        """
        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if workflow_id is not None:
            params["workflowId"] = workflow_id
        if project_id is not None:
            params["projectId"] = project_id
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = await self.client.get("/executions", params=params)
        return ExecutionList(**get_json(response))

    async def get_execution(self, execution_id: int) -> Execution:
        """
        GET /executions/{id}
        Retrieve an execution by ID.
        """
        response = await self.client.get(f"/executions/{execution_id}")
        return Execution(**get_json(response))

    async def delete_execution(self, execution_id: int) -> Execution:
        """
        DELETE /executions/{id}
        Delete an execution. Returns the deleted execution object.
        """
        response = await self.client.delete(f"/executions/{execution_id}")
        return Execution(**get_json(response))

    #
    # --------------
    # Credential Endpoints
    # --------------
    #

    async def get_credential_type(self, credential_type_name: str) -> Dict[str, Any]:
        """
        GET /credentials/schema/{credentialTypeName}
        Show credential data schema for a specific credential type.
        """
        response = await self.client.get(f"/credentials/schema/{credential_type_name}")
        return get_json(response)

    async def create_credential(self, credential: Credential) -> Credential:
        """
        POST /credentials
        Create a credential.
        """
        response = await self.client.post("/credentials", json=credential.model_dump(exclude_unset=True))
        return Credential(**get_json(response))

    async def delete_credential(self, credential_id: str) -> Credential:
        """
        DELETE /credentials/{id}
        Delete a credential. Returns the deleted credential.
        """
        response = await self.client.delete(f"/credentials/{credential_id}")
        return Credential(**get_json(response))

    async def transfer_credential(self, credential_id: str, destination_project_id: str) -> None:
        """
        PUT /credentials/{id}/transfer
        Transfer a credential to another project.
        """
        payload = {"destinationProjectId": destination_project_id}
        response = await self.client.put(f"/credentials/{credential_id}/transfer", json=payload)
        response.raise_for_status()
        return None

    #
    # --------------
    # Tag Endpoints
    # --------------
    #

    async def create_tag(self, tag: Tag) -> Tag:
        """
        POST /tags
        Create a tag.
        """
        response = await self.client.post("/tags", json=tag.model_dump(exclude_unset=True))
        return Tag(**get_json(response))

    async def get_tags(self, limit: Optional[int] = None, cursor: Optional[str] = None) -> TagList:
        """
        GET /tags
        Retrieve all tags.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = await self.client.get("/tags", params=params)
        return TagList(**get_json(response))

    async def get_tag_by_id(self, tag_id: str) -> Tag:
        """
        GET /tags/{id}
        Retrieve a tag by ID.
        """
        response = await self.client.get(f"/tags/{tag_id}")
        return Tag(**get_json(response))

    async def update_tag(self, tag_id: str, payload: Dict[str, Any]) -> Tag:
        """
        PUT /tags/{id}
        Update a tag by ID.
        """
        response = await self.client.put(f"/tags/{tag_id}", json=payload)
        return Tag(**get_json(response))

    async def delete_tag(self, tag_id: str) -> Tag:
        """
        DELETE /tags/{id}
        Delete a tag. Returns the deleted tag object.
        """
        response = await self.client.delete(f"/tags/{tag_id}")
        return Tag(**get_json(response))

    async def get_workflow_tags(self, workflow_id: str) -> List[Tag]:
        """
        GET /workflows/{id}/tags
        Retrieve tags associated with a workflow.
        """
        response = await self.client.get(f"/workflows/{workflow_id}/tags")
        raw = get_json(response)
        return [Tag(**tag) for tag in raw]

    async def update_workflow_tags(self, workflow_id: str, tag_ids: List[Dict[str, str]]) -> List[Tag]:
        """
        PUT /workflows/{id}/tags
        Update tags associated with a workflow. Returns updated tag list.
        """
        # The OpenAPI spec expects an array of tag IDs
        response = await self.client.put(f"/workflows/{workflow_id}/tags", json=tag_ids)
        raw = get_json(response)
        return [Tag(**tag) for tag in raw]

    #
    # --------------
    # Variable Endpoints
    # --------------
    #

    async def create_variable(self, variable: Variable) -> Variable:
        """
        POST /variables
        Create a variable.
        """
        response = await self.client.post("/variables", json=variable.model_dump(exclude_unset=True))
        return Variable(**get_json(response))

    async def get_variables(self, limit: Optional[int] = None, cursor: Optional[str] = None) -> VariableList:
        """
        GET /variables
        Retrieve variables from your instance.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = await self.client.get("/variables", params=params)
        return VariableList(**get_json(response))

    async def delete_variable(self, variable_id: str) -> None:
        """
        DELETE /variables/{id}
        Delete a variable (204 No Content).
        """
        response = await self.client.delete(f"/variables/{variable_id}")
        response.raise_for_status()
        return None

    #
    # --------------
    # Project Endpoints
    # --------------
    #

    async def create_project(self, project: Project) -> Project:
        """
        POST /projects
        Create a project.
        """
        response = await self.client.post("/projects", json=project.model_dump(exclude_unset=True))
        return Project(**get_json(response))

    async def get_projects(self, limit: Optional[int] = None, cursor: Optional[str] = None) -> ProjectList:
        """
        GET /projects
        Retrieve projects.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = await self.client.get("/projects", params=params)
        return ProjectList(**get_json(response))

    async def delete_project(self, project_id: str) -> None:
        """
        DELETE /projects/{projectId}
        Delete a project (204 No Content).
        """
        response = await self.client.delete(f"/projects/{project_id}")
        response.raise_for_status()
        return None

    async def update_project(self, project_id: str, project: Project) -> None:
        """
        PUT /projects/{projectId}
        Update a project (204 No Content).
        """
        response = await self.client.put(f"/projects/{project_id}", json=project.model_dump(exclude_unset=True))
        response.raise_for_status()
        return None

    #
    # --------------
    # Audit Endpoints
    # --------------
    #

    async def generate_audit(self, additional_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        POST /audit
        Generate a security audit for your n8n instance.
        """
        payload: Dict[str, Any] = {}
        if additional_options is not None:
            payload["additionalOptions"] = additional_options

        response = await self.client.post("/audit", json=payload)
        return get_json(response)

    #
    # --------------
    # User Endpoints
    # --------------
    #

    async def get_users(
        self,
        limit: Optional[int] = 100,
        cursor: Optional[str] = None,
        include_role: Optional[bool] = False,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        GET /users
        Retrieve all users from your instance. Only for instance owner.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        if include_role is not None:
            params["includeRole"] = include_role
        if project_id is not None:
            params["projectId"] = project_id

        response = await self.client.get("/users", params=params)
        return get_json(response)

    async def create_users(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        POST /users
        Create multiple users.
        """
        response = await self.client.post("/users", json=users)
        return get_json(response)

    async def get_user(self, user_identifier: str) -> Dict[str, Any]:
        """
        GET /users/{id}
        Retrieve a user by ID or email. Only for instance owner.
        """
        response = await self.client.get(f"/users/{user_identifier}")
        return get_json(response)

    async def delete_user(self, user_identifier: str) -> None:
        """
        DELETE /users/{id}
        Delete a user (204 No Content).
        """
        response = await self.client.delete(f"/users/{user_identifier}")
        response.raise_for_status()
        return None

    async def change_user_role(self, user_identifier: str, new_role: str) -> Dict[str, Any]:
        """
        PATCH /users/{id}/role
        Change a user's global role.
        """
        payload = {"newRoleName": new_role}
        response = await self.client.patch(f"/users/{user_identifier}/role", json=payload)
        return get_json(response)

    #
    # --------------
    # Source Control Endpoints
    # --------------
    #

    async def pull_changes(
        self,
        force: Optional[bool] = None,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        POST /source-control/pull
        Pull changes from the remote repository.
        """
        payload: Dict[str, Any] = {}
        if force is not None:
            payload["force"] = force
        if variables is not None:
            payload["variables"] = variables

        response = await self.client.post("/source-control/pull", json=payload)
        return get_json(response)

    #
    # --------------
    # Client Cleanup
    # --------------
    #

    async def shutdown(self) -> None:
        """
        Close the underlying HTTP client connection.
        """
        await self.client.aclose()


# ---------------------------
# Main Function to Test Endpoints
# ---------------------------

async def main():
    client = N8nClient(
        base_url="http://localhost:5678/api/v1",
        api_key=api_key,
    )

    try:
        print("=== Starting n8n API Client Tests ===\n")

        # ---------------------
        # Tag Endpoints
        # ---------------------
        print("1. Creating a new tag...")
        new_tag = Tag(name="Test Tag")
        created_tag = await client.create_tag(new_tag)
        print(f"   Created Tag: {created_tag}\n")

        print("2. Retrieving all tags...")
        tags = await client.get_tags()
        print(f"   Tags: {tags}\n")

        print("3. Retrieving tag by ID...")
        retrieved_tag = await client.get_tag_by_id(created_tag.id)
        print(f"   Retrieved Tag: {retrieved_tag}\n")

        print("4. Updating the tag's name...")
        updated_tag_payload = {"name": "Updated Test Tag"}
        updated_tag = await client.update_tag(created_tag.id, updated_tag_payload)
        print(f"   Updated Tag: {updated_tag}\n")

        print("5. Deleting the tag...")
        deleted_tag = await client.delete_tag(created_tag.id)
        print(f"   Deleted Tag: {deleted_tag}\n")

        # ---------------------
        # Project Endpoints
        # ---------------------
        # print("6. Creating a new project...")
        # new_project = Project(name="Test Project")
        # created_project = await client.create_project(new_project)
        # print(f"   Created Project: {created_project}\n")

        # print("7. Retrieving all projects...")
        # projects = await client.get_projects()
        # print(f"   Projects: {projects}\n")
        #
        # print("8. Updating the project's name...")
        # updated_project_payload = Project(name="Updated Test Project")
        # await client.update_project(created_project.id, updated_project_payload)
        # print("   Project updated successfully.\n")

        # ---------------------
        # Workflow Endpoints
        # ---------------------
        print("9. Creating a new workflow with a trigger node and a connected Set node...")
        # Define a trigger node
        trigger_node = WorkflowNode(
            id="trigger-node-1",
            name="Start",
            type="n8n-nodes-base.start",
            typeVersion=1.0,
            position=[0, 0],
            parameters={},
        )

        # Define a Set node
        set_node = WorkflowNode(
            id="set-node-1",
            name="Set",
            type="n8n-nodes-base.set",
            typeVersion=1.0,
            position=[200, 0],
            parameters={
                "values": {
                    "boolean": [],
                    "number": [],
                    "string": [
                        {"name": "exampleField", "value": "Hello, world!"}
                    ]
                }
            },
        )

        # Define the workflow connections
        connections = {
            "trigger-node-1": {  # Start node
                "main": [[{"node": "set-node-1", "type": "main", "index": 0}]]  # Connect Start -> Set
            }
        }

        # Create the workflow
        new_workflow = Workflow(
            name="Test Workflow",
            nodes=[trigger_node, set_node],  # Include both nodes
            connections=connections,
            settings={},
        )

        created_workflow = await client.create_workflow(new_workflow)
        print(f"   Created Workflow: {created_workflow}\n")

        print("10. Retrieving all workflows...")
        workflows = await client.get_workflows()
        print(f"   Workflows: {workflows}\n")

        print("11. Retrieving workflow by ID...")
        retrieved_workflow = await client.get_workflow(created_workflow.id)
        print(f"   Retrieved Workflow: {retrieved_workflow}\n")

        print("12. Updating the workflow's name...")
        # Retrieve the existing workflow to ensure all required fields are present
        retrieved_workflow = await client.get_workflow(created_workflow.id)

        # Update the name of the workflow
        retrieved_workflow.name = "Updated Test Workflow"

        # Pass the updated workflow object to the update_workflow method
        updated_wf = await client.update_workflow(retrieved_workflow.id, retrieved_workflow)
        print(f"   Updated Workflow: {updated_wf}\n")

        print("13. Activating the workflow...")
        activated_workflow = await client.activate_workflow(created_workflow.id)
        print(f"   Activated Workflow: {activated_workflow}\n")

        print("14. Deactivating the workflow...")
        deactivated_workflow = await client.deactivate_workflow(created_workflow.id)
        print(f"   Deactivated Workflow: {deactivated_workflow}\n")

        # print("15. Transferring the workflow to the new project...")
        # transfer_response = await client.transfer_workflow(created_workflow.id, created_project.id)
        # print(f"   Transfer Response: {transfer_response}\n")

        print("16. Deleting the workflow...")
        deleted_workflow = await client.delete_workflow(created_workflow.id)
        print(f"   Deleted Workflow: {deleted_workflow}\n")

        # ---------------------
        # Credential Endpoints
        # ---------------------
        print("17. Creating a new credential...")
        new_credential = Credential(
            name="Test Credential",
            type="testType",
            data={"token": "testtoken123"}
        )
        created_credential = await client.create_credential(new_credential)
        print(f"   Created Credential: {created_credential}\n")

        print("18. Retrieving credential type schema...")
        credential_schema = await client.get_credential_type("testType")
        print(f"   Credential Schema: {credential_schema}\n")

        # print("19. Transferring the credential to the new project...")
        # await client.transfer_credential(created_credential.id, created_project.id)
        # print("   Credential transferred successfully.\n")

        print("20. Deleting the credential...")
        deleted_credential = await client.delete_credential(created_credential.id)
        print(f"   Deleted Credential: {deleted_credential}\n")

        # ---------------------
        # Variable Endpoints
        # ---------------------
        print("21. Creating a new variable...")
        new_variable = Variable(key="test_key", value="test_value")
        created_variable = await client.create_variable(new_variable)
        print(f"   Created Variable: {created_variable}\n")

        print("22. Retrieving all variables...")
        variables = await client.get_variables()
        print(f"   Variables: {variables}\n")

        print("23. Deleting the variable...")
        await client.delete_variable(created_variable.id)
        print("   Variable deleted successfully.\n")

        # ---------------------
        # User Endpoints
        # ---------------------
        # Note: Creating users may send invitation emails. Uncomment if desired.
        """
        print("24. Creating new users...")
        new_users = [
            {"email": "test.user1@example.com", "role": "global:member"},
            {"email": "test.user2@example.com", "role": "global:admin"}
        ]
        created_users = await client.create_users(new_users)
        print(f"   Created Users: {created_users}\n"
        )

        print("25. Retrieving all users...")
        users = await client.get_users()
        print(f"   Users: {users}\n")

        if created_users.get("user"):
            user_id = created_users["user"]["id"]
            print(f"26. Retrieving user by ID: {user_id}...")
            user = await client.get_user(user_id)
            print(f"   Retrieved User: {user}\n")

            print(f"27. Changing user role for user ID: {user_id}...")
            updated_user = await client.change_user_role(user_id, "global:admin")
            print(f"   Updated User Role: {updated_user}\n")

            print(f"28. Deleting user ID: {user_id}...")
            await client.delete_user(user_id)
            print("   User deleted successfully.\n")
        """

        # ---------------------
        # Source Control Endpoints
        # ---------------------
        print("29. Pulling changes from source control...")
        pull_response = await client.pull_changes(force=True, variables={"key": "value"})
        print(f"   Pull Response: {pull_response}\n")

        # ---------------------
        # Audit Endpoints
        # ---------------------
        print("30. Generating an audit report...")
        audit_report = await client.generate_audit()
        print(f"   Audit Report: {audit_report}\n")

        # ---------------------
        # Final Cleanup: Delete Project
        # ---------------------
        # print("31. Deleting the project...")
        # await client.delete_project(created_project.id)
        # print("   Project deleted successfully.\n")

        print("=== n8n API Client Tests Completed Successfully ===")

    except httpx.HTTPStatusError as exc:
        print(f"HTTP Error: {exc.response.status_code} - {exc.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        await client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
