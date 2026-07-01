"""
PrepPal AI — Custom Exception Hierarchy
Provides structured exceptions for clear error propagation across all layers.
"""


class PrepPalError(Exception):
    """Base exception for all PrepPal AI errors."""
    def __init__(self, message: str, code: str = "PREPPAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class DatabaseError(PrepPalError):
    """Raised when a database operation fails."""
    def __init__(self, message: str, operation: str = ""):
        super().__init__(message, code="DATABASE_ERROR")
        self.operation = operation


class RecordNotFoundError(PrepPalError):
    """Raised when a requested record does not exist."""
    def __init__(self, resource: str, identifier: str | int):
        super().__init__(f"{resource} not found: {identifier}", code="NOT_FOUND")
        self.resource = resource
        self.identifier = identifier


class ValidationError(PrepPalError):
    """Raised when input validation fails."""
    def __init__(self, message: str, field: str = ""):
        super().__init__(message, code="VALIDATION_ERROR")
        self.field = field


class AgentError(PrepPalError):
    """Raised when an ADK agent invocation fails."""
    def __init__(self, message: str, agent_name: str = ""):
        super().__init__(message, code="AGENT_ERROR")
        self.agent_name = agent_name


class MCPToolError(PrepPalError):
    """Raised when an MCP tool call fails."""
    def __init__(self, message: str, tool_name: str = ""):
        super().__init__(message, code="MCP_TOOL_ERROR")
        self.tool_name = tool_name


class ServiceError(PrepPalError):
    """Raised when a service-layer operation fails."""
    def __init__(self, message: str, service: str = ""):
        super().__init__(message, code="SERVICE_ERROR")
        self.service = service


class ConfigurationError(PrepPalError):
    """Raised when required configuration/env vars are missing."""
    def __init__(self, message: str, key: str = ""):
        super().__init__(message, code="CONFIG_ERROR")
        self.key = key
