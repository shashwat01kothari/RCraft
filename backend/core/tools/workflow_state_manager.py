import redis
import os
import uuid
import json
from typing import Optional
from backend.core.data_models import FinalResumeSections

class WorkflowStateManager:
    """
    Manages the temporary storage and retrieval of workflow results using Redis.
    
    This class handles the connection to Redis and provides a simple interface
    to save and load the state of a completed resume generation workflow.
    """

    def __init__(self):
        """
        Initializes the state manager and attempts to connect to Redis.
        The host is now read from an environment variable for container flexibility.

        """
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379)) # Also make the port configurable

        self.redis_client: Optional[redis.Redis] = None
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
            self.redis_client.ping()
            print(f"--- TOOL: Connected to Redis successfully at {redis_host}:{redis_port}. ---")
        except redis.exceptions.ConnectionError as e:
            print(f"--- TOOL: ERROR: Could not connect to Redis at {redis_host}:{redis_port}. Details: {e} ---")
            self.redis_client = None

    def save_state(self, resume_data: FinalResumeSections, ttl_seconds: int = 600) -> str:
        """
        Saves the structured resume data to Redis with a Time-To-Live (TTL).

        Args:
            resume_data: The Pydantic model of the final resume sections.
            ttl_seconds: Time-to-live for the cache entry (default is 10 minutes).

        Returns:
            A unique workflow_id string that can be used to retrieve the state.
            
        Raises:
            ConnectionError: If the Redis client is not connected.
        """
        if not self.redis_client:
            raise ConnectionError("Redis service is not available. Cannot save workflow state.")
            
        # Generate a new, unique ID for this workflow instance.
        workflow_id = str(uuid.uuid4())
        
        # Serialize the Pydantic model into a JSON string for storage.
        state_json = resume_data.model_dump_json()
        
        # Use the 'set' command with the 'ex' (expire) parameter to automatically handle the TTL.
        self.redis_client.set(workflow_id, state_json, ex=ttl_seconds)
        
        print(f"--- TOOL: Saved workflow state to Redis with ID: {workflow_id} (TTL: {ttl_seconds}s) ---")
        return workflow_id

    def load_state(self, workflow_id: str) -> FinalResumeSections:
        """
        Retrieves and reconstructs the resume data from Redis using a workflow ID.

        Args:
            workflow_id: The unique ID of the workflow run, previously returned by save_state.

        Returns:
            A FinalResumeSections Pydantic model instance.
            
        Raises:
            ConnectionError: If the Redis client is not connected.
            FileNotFoundError: If the workflow_id does not exist in Redis or has expired.
        """
        if not self.redis_client:
            raise ConnectionError("Redis service is not available. Cannot load workflow state.")

        # Retrieve the JSON string from Redis.
        state_json = self.redis_client.get(workflow_id)
        
        # If the key doesn't exist (or has expired), Redis returns None.
        if not state_json:
            raise FileNotFoundError(f"Workflow ID '{workflow_id}' not found in Redis or has expired.")
        
        print(f"--- TOOL: Loaded workflow state from Redis for ID: {workflow_id} ---")
        
        # Deserialize the JSON string and use Pydantic to parse and validate it back into a model instance.
        # This is a critical validation step.
        return FinalResumeSections(**json.loads(state_json))
    
