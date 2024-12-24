from dslmodel.agent_model import AgentModel
from pydantic import BaseModel, Field
from typing import Optional, Any, List, Dict
from datetime import datetime

from pydantic_settings import BaseSettings


class Credential(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the credential.")
    name: str = Field(..., description="Name of the credential.")
    type: str = Field(..., description="Type identifier for the credential.")
    data: Dict[str, Any] = Field(default_factory=dict, description="Credential data.")
    createdAt: Optional[str] = Field(None, description="Timestamp when created.")
    updatedAt: Optional[str] = Field(None, description="Timestamp when updated.")


class AuditReport(BaseModel):
    credentials: Optional[Dict[str, Any]] = Field(None, description="Risk report related to credentials.")
    database: Optional[Dict[str, Any]] = Field(None, description="Risk report related to database usage.")
    filesystem: Optional[Dict[str, Any]] = Field(None, description="Risk report related to filesystem access.")
    nodes: Optional[Dict[str, Any]] = Field(None, description="Risk report related to nodes.")
    instance: Optional[Dict[str, Any]] = Field(None, description="Risk report related to instance configuration.")


class WorkflowNode(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the node.")
    name: str = Field(..., description="Name of the node.")
    type: str = Field(..., description="Type identifier for the node.")
    typeVersion: float = Field(..., description="Version of the node type.")
    position: List[int] = Field(..., description="Position of the node in the editor.")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Configuration parameters for the node.")
    credentials: Optional[Dict[str, Credential]] = Field(None, description="Credentials associated with the node.")
    disabled: Optional[bool] = Field(False, description="Whether the node is disabled.")
    notesInFlow: Optional[bool] = Field(False, description="Whether notes are displayed in the workflow flow.")
    notes: Optional[str] = Field(None, description="Optional notes about the node.")
    executeOnce: Optional[bool] = Field(False, description="Whether the node executes only once.")
    alwaysOutputData: Optional[bool] = Field(False, description="Whether the node always outputs data.")
    retryOnFail: Optional[bool] = Field(False, description="Whether to retry execution on failure.")
    maxTries: Optional[int] = Field(None, description="Maximum number of retry attempts.")
    waitBetweenTries: Optional[int] = Field(None, description="Wait time in seconds between retries.")
    onError: Optional[str] = Field("stopWorkflow", description="Error handling behavior.")
    createdAt: Optional[str] = Field(None, description="Timestamp of when the node was created.", readOnly=True)
    updatedAt: Optional[str] = Field(None, description="Timestamp of when the node was last updated.", readOnly=True)


class WorkflowSettings(BaseModel):
    saveExecutionProgress: Optional[bool] = Field(False, description="Save execution progress.")
    saveManualExecutions: Optional[bool] = Field(False, description="Save manual execution data.")
    saveDataErrorExecution: Optional[str] = Field("none", description="Save data on error executions.")
    saveDataSuccessExecution: Optional[str] = Field("none", description="Save data on successful executions.")
    executionTimeout: Optional[int] = Field(3600, description="Execution timeout in seconds.")
    timezone: Optional[str] = Field("UTC", description="Workflow timezone.")


class Workflow(AgentModel):
    id: Optional[str] = Field(None, description="Unique identifier for the workflow.")
    name: str = Field(..., description="Name of the workflow.")
    nodes: List[WorkflowNode] = Field(..., description="Nodes in the workflow.")
    connections: Dict[str, Any] = Field(..., description="Connections between nodes.")
    settings: Optional[WorkflowSettings] = Field(None, description="Workflow-specific settings.")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the workflow.")


class WorkflowList(BaseModel):
    data: List[Workflow] = Field(..., description="List of workflows.")
    nextCursor: Optional[str] = Field(None, description="Cursor for pagination.")


class Execution(BaseModel):
    id: str = Field(..., description="Unique identifier for the execution.")
    finished: bool = Field(..., description="Indicates whether the execution has finished.")
    mode: str = Field(..., description="Mode of execution.")
    retryOf: Optional[str] = Field(None, description="Retry execution ID if applicable.")
    retrySuccessId: Optional[str] = Field(None, description="ID of successful retry if applicable.")
    startedAt: datetime = Field(..., description="Start timestamp.")
    stoppedAt: Optional[datetime] = Field(None, description="Stop timestamp.")
    workflowId: str = Field(..., description="Associated workflow ID.")
    waitTill: Optional[datetime] = Field(None, description="Resume timestamp if waiting.")


class ExecutionList(BaseModel):
    data: List[Execution] = Field(..., description="List of executions.")
    nextCursor: Optional[str] = Field(None, description="Cursor for pagination.")


class CredentialList(BaseModel):
    data: List[Credential] = Field(..., description="List of credentials.")


class Tag(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the tag.")
    name: str = Field(..., description="Name of the tag.")
    createdAt: Optional[str] = Field(None, description="Timestamp when created.")
    updatedAt: Optional[str] = Field(None, description="Timestamp when updated.")


class TagList(BaseModel):
    data: List[Tag] = Field(..., description="List of tags.")
    nextCursor: Optional[str] = Field(None, description="Cursor for pagination.")


class Variable(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the variable.")
    key: str = Field(..., description="Variable key.")
    value: str = Field(..., description="Variable value.")


class VariableList(BaseModel):
    data: List[Variable] = Field(..., description="List of variables.")
    nextCursor: Optional[str] = Field(None, description="Cursor for pagination.")


class Project(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the project.")
    name: str = Field(..., description="Name of the project.")


class ProjectList(BaseModel):
    data: List[Project] = Field(..., description="List of projects.")
    nextCursor: Optional[str] = Field(None, description="Cursor for pagination.")


class ErrorResponse(BaseModel):
    code: Optional[str] = Field(None, description="Error code.")
    message: str = Field(..., description="Error message.")
    description: Optional[str] = Field(None, description="Detailed error description.")


class N8nSettings(BaseSettings):
    """
    Configuration for N8nClient, using Pydantic's BaseSettings for environment variable support.
    """
    api_key: str = "n8n-api-key"
    host: str = "localhost"
    port: int = 5678
    protocol: str = "http"
    base_path: str = "/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "N8N_"