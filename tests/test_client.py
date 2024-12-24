# tests/test_client.py

import pytest
import respx
from httpx import Response
from pydantic import ValidationError
from typing import List

from pyn8n.client import N8nClient
from pyn8n.models import Workflow, Workflowlist, Credential, Credentiallist
from pyn8n.exceptions import (
    InvalidRequestException,
    ResourceNotFoundException,
    NotAuthorizedException,
)

API_KEY = "test-api-key"
BASE_URL = "http://localhost:5678/api/v1"

@pytest.fixture
def client():
    return N8nClient(
        api_key=API_KEY,
        protocol="http",
        host="localhost",
        port=5678,
    )

@pytest.fixture
def respx_mock():
    with respx.mock(base_url=BASE_URL) as mock:
        yield mock

def test_api_key_header(client, respx_mock):
    route = respx_mock.get("/workflows").respond(
        json={"data": []}, status_code=200
    )

    client.get_workflows()

    assert route.called
    request = route.calls[0].request
    assert request.headers.get("X-N8N-API-KEY") == API_KEY
    assert request.headers.get("Accept") == "application/json"

def test_get_workflows_success(client, respx_mock):
    mock_response = {
        "data": [
            {"name": "Workflow 1", "nodes": [], "connections": {}, "active": True, "settings": {}, "tags": []},
            {"name": "Workflow 2", "nodes": [], "connections": {}, "active": False, "settings": {}, "tags": []},
        ]
    }
    respx_mock.get("/workflows").respond(json=mock_response, status_code=200)

    workflows = client.get_workflows()

    assert isinstance(workflows, Workflowlist)
    assert len(workflows.data) == 2
    assert workflows.data[0].name == "Workflow 1"
    assert workflows.data[1].active is False

def test_create_workflow_success(client, respx_mock):
    workflow_name = "New Workflow"
    mock_response = {
        "data": {
            "name": workflow_name,
            "nodes": [
                {
                    "parameters": {},
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "typeVersion": 1,
                    "position": [250, 300],
                }
            ],
            "connections": {},
            "active": False,
            "settings": {},
            "tags": [],
        }
    }
    respx_mock.post("/workflows").respond(json=mock_response, status_code=200)

    created_workflow = client.create_workflow(workflow_name)

    assert isinstance(created_workflow, Workflow)
    assert created_workflow.name == workflow_name
    assert len(created_workflow.nodes) == 1
    assert created_workflow.active is False

def test_get_workflow_success(client, respx_mock):
    workflow_id = 123
    mock_response = {
        "data": {
            "name": "Existing Workflow",
            "nodes": [],
            "connections": {},
            "active": True,
            "settings": {},
            "tags": [],
        }
    }
    respx_mock.get(f"/workflows/{workflow_id}").respond(json=mock_response, status_code=200)

    workflow = client.get_workflow(workflow_id)

    assert isinstance(workflow, Workflow)
    assert workflow.name == "Existing Workflow"
    assert workflow.active is True

def test_add_credentials_success(client, respx_mock):
    name = "MyCredential"
    credential_type = "exampleType"
    nodes_access = ["n8n-nodes-base.httpRequest"]
    data = {"key": "value"}

    mock_response = {
        "data": {
            "name": name,
            "type": credential_type,
            "nodesAccess": [{"nodeType": "n8n-nodes-base.httpRequest"}],
            "data": data,
            "id": "cred_12345",
        }
    }
    respx_mock.post("/credentials").respond(json=mock_response, status_code=200)

    credential = client.add_credentials(name, credential_type, nodes_access, data)

    assert isinstance(credential, Credential)
    assert credential.name == name
    assert credential.type == credential_type
    assert credential.nodesAccess == [{"nodeType": "n8n-nodes-base.httpRequest"}]
    assert credential.data == data
    assert credential.id == "cred_12345"

def test_get_workflow_not_found(client, respx_mock):
    workflow_id = 999
    respx_mock.get(f"/workflows/{workflow_id}").respond(json={"message": "Not Found"}, status_code=404)

    with pytest.raises(ResourceNotFoundException) as exc_info:
        client.get_workflow(workflow_id)

    assert str(exc_info.value) == "Resource not found"

def test_authentication_failure(client, respx_mock):
    respx_mock.get("/workflows").respond(json={"message": "Unauthorized"}, status_code=401)

    with pytest.raises(InvalidRequestException) as exc_info:
        client.get_workflows()

    assert "[401] - Unauthorized" in str(exc_info.value)

def test_delete_workflow_success(client, respx_mock):
    workflow_id = 123
    mock_response = {"message": "Workflow deleted successfully"}
    respx_mock.delete(f"/workflows/{workflow_id}").respond(json=mock_response, status_code=200)

    response = client.delete_workflow(workflow_id)

    assert response["message"] == "Workflow deleted successfully"

def test_activate_workflow_success(client, respx_mock):
    workflow_id = 123
    existing_workflow = {
        "data": {
            "name": "Workflow to Activate",
            "nodes": [],
            "connections": {},
            "active": False,
            "settings": {},
            "tags": [],
        }
    }
    updated_workflow = {
        "data": {
            "name": "Workflow to Activate",
            "nodes": [],
            "connections": {},
            "active": True,
            "settings": {},
            "tags": [],
        }
    }

    respx_mock.get(f"/workflows/{workflow_id}").respond(json=existing_workflow, status_code=200)
    respx_mock.patch(f"/workflows/{workflow_id}").respond(json=updated_workflow, status_code=200)

    activated_workflow = client.activate_workflow(workflow_id)

    assert isinstance(activated_workflow, Workflow)
    assert activated_workflow.active is True

def test_execute_node_success(client, respx_mock):
    workflow_id = 123
    node_name = "Start"
    session_id = "session_abc123"
    workflow_data = {
        "name": "Workflow to Execute",
        "nodes": [],
        "connections": {},
        "active": True,
        "settings": {},
        "tags": [],
    }
    execute_payload = {
        "workflowData": workflow_data,
        "startNodes": [node_name],
        "destinationNode": node_name,
    }
    mock_response = {"executionId": 456, "status": "started"}

    respx_mock.post("/workflows/run").respond(json=mock_response, status_code=200)

    response = client.execute_node(workflow_id, node_name, session_id, workflow_data)

    assert response["executionId"] == 456
    assert response["status"] == "started"

def test_get_node_icon_success(client, respx_mock):
    node_name = "n8n-nodes-base.start"
    mock_icon_content = b"<svg>...</svg>"

    respx_mock.get(f"/node-icon/{node_name}").respond(content=mock_icon_content, status_code=200)

    response = client.get_node_icon(node_name)

    assert response == mock_icon_content

def test_change_credentials_success(client, respx_mock):
    credential_id = 123
    name = "UpdatedCredential"
    credential_type = "updatedType"
    nodes_access = ["n8n-nodes-base.httpRequest"]
    data = {"key": "new_value"}

    mock_response = {
        "data": {
            "id": credential_id,
            "name": name,
            "type": credential_type,
            "nodesAccess": [{"nodeType": "n8n-nodes-base.httpRequest"}],
            "data": data,
        }
    }
    respx_mock.patch(f"/credentials/{credential_id}").respond(json=mock_response, status_code=200)

    updated_credential = client.change_credentials(
        credential_id, name, credential_type, nodes_access, data
    )

    assert isinstance(updated_credential, Credential)
    assert updated_credential.name == name
    assert updated_credential.type == credential_type
    assert updated_credential.nodesAccess == [{"nodeType": "n8n-nodes-base.httpRequest"}]
    assert updated_credential.data == data
    assert updated_credential.id == credential_id
