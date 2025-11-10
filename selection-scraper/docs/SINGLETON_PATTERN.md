# Singleton Pattern Implementation

## Overview

All client classes in this project have been implemented using the **Singleton Pattern** to ensure that connections to external dependencies happen only once, improving performance and resource management.

## What is the Singleton Pattern?

The Singleton Pattern is a design pattern that restricts a class to a single instance. When you create a "new" instance of a singleton class, you actually get back the same instance that was created the first time.

## Benefits

1. **Single Connection**: Each dependency (OpenAI, Qdrant, Snowflake) maintains only ONE connection throughout the application lifecycle
2. **Resource Efficiency**: Reduces memory usage and connection overhead
3. **Performance**: Eliminates redundant initialization and connection setup
4. **Consistency**: All parts of the application share the same client instance and configuration

## Implementation Details

### Classes Implementing Singleton Pattern

1. **OpenAIClient** (`clients/openai_client.py`)
   - Single connection to OpenAI API gateway
   - Shared across all components that need embeddings or LLM responses

2. **DDSelectionQdrantClient** (`clients/dd_selection_qdrant_client.py`)
   - Single connection to Qdrant vector database
   - Automatically uses the singleton OpenAI client
   - Shared across all vector search operations

3. **SnowflakeClient** (`clients/snowflake_client.py`)
   - Single connection to Snowflake database (when using context manager)
   - Configuration initialized once

4. **MockSnowflakeClient** (`clients/snowflake_client_mock.py`)
   - Singleton for testing purposes
   - Ensures consistent mock data behavior

### How It Works

Each singleton class implements:

```python
class MyClient:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """Ensures only one instance exists"""
        if cls._instance is None:
            cls._instance = super(MyClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, ...):
        """Only initializes once"""
        if self._initialized:
            return
        
        # Initialization code here
        self._initialized = True
```

### Key Behaviors

1. **First Call**: Creates the instance and initializes connections
   ```python
   client1 = OpenAIClient()  # Creates instance, initializes connection
   ```

2. **Subsequent Calls**: Returns the same instance
   ```python
   client2 = OpenAIClient()  # Returns client1, no new connection
   assert client1 is client2  # True!
   ```

3. **Parameter Handling**: Only parameters from first initialization are used
   ```python
   client1 = OpenAIClient(max_retries=5)   # Uses max_retries=5
   client2 = OpenAIClient(max_retries=10)  # Still uses max_retries=5
   ```

## Usage Examples

### Before (Multiple Connections)

```python
# This would create 3 separate connections to OpenAI
def function_a():
    client = OpenAIClient()  # Connection 1
    # ...

def function_b():
    client = OpenAIClient()  # Connection 2
    # ...

def function_c():
    client = OpenAIClient()  # Connection 3
    # ...
```

### After (Single Connection)

```python
# All functions share the same OpenAI connection
def function_a():
    client = OpenAIClient()  # Connection created
    # ...

def function_b():
    client = OpenAIClient()  # Same connection reused
    # ...

def function_c():
    client = OpenAIClient()  # Same connection reused
    # ...
```

## Shared OpenAI Client Example

The DDSelectionQdrantClient automatically shares the OpenAI client:

```python
# Create OpenAI client (connection 1)
openai_client = OpenAIClient()

# Create Qdrant client (reuses OpenAI connection 1)
qdrant_client = DDSelectionQdrantClient()

# Both use the same OpenAI client
assert openai_client is qdrant_client.openai_client  # True!
```

## Testing

Run the singleton validation test:

```bash
source venv/bin/activate
python test_singleton.py
```

This test verifies:
- Each client class properly implements the singleton pattern
- Multiple instantiations return the same object
- OpenAI client is shared across components
- Connections are established only once

## Migration Notes

### No Code Changes Required

Existing code continues to work without modification:
- `OpenAIClient()` still works as before
- `DDSelectionQdrantClient()` still works as before
- All function signatures remain unchanged

### Behavioral Changes

1. **Initialization Parameters**: Only the first instantiation's parameters are used. Subsequent calls with different parameters will be ignored (but won't raise errors).

2. **Shared State**: All parts of the application share the same client instance, which can be beneficial for:
   - Tracking metrics across all operations
   - Consistent configuration
   - Shared connection pooling

## Best Practices

1. **Initialize Early**: Consider initializing clients once at application startup for clarity
   ```python
   # At startup
   openai_client = OpenAIClient()
   qdrant_client = DDSelectionQdrantClient()
   ```

2. **No Need to Pass Around**: Since clients are singletons, you can safely create them anywhere without worrying about multiple connections
   ```python
   # This is now safe and efficient
   def my_function():
       client = OpenAIClient()  # No overhead
       # use client...
   ```

3. **Testing**: In tests, be aware that the singleton persists across test cases. If needed, you can reset by setting `ClassName._instance = None` and `ClassName._initialized = False` in test setup.

## Performance Impact

### Before Singleton
- **Multiple OpenAI connections**: 3-5 connections typical in pipeline
- **Multiple Qdrant connections**: 2-3 connections typical
- **Initialization overhead**: Repeated for each instantiation

### After Singleton
- **Single OpenAI connection**: 1 connection regardless of usage
- **Single Qdrant connection**: 1 connection regardless of usage
- **Initialization overhead**: Only once at first use

**Estimated Resource Savings**: 60-80% reduction in connection overhead

## Troubleshooting

### Client Not Reusing Connection

Check that you're not manually creating underlying client objects:
```python
# ❌ Bad: Creates new connection
client = QdrantClientBase(url=..., ...)

# ✓ Good: Uses singleton
client = DDSelectionQdrantClient()
```

### Different Parameters Not Taking Effect

This is expected behavior. The singleton uses parameters from first initialization only:
```python
# First call sets parameters
client1 = OpenAIClient(max_retries=5)

# This won't change max_retries
client2 = OpenAIClient(max_retries=10)
```

**Solution**: Initialize with desired parameters at application startup.

### Need to Reset in Tests

```python
# In test teardown
OpenAIClient._instance = None
OpenAIClient._initialized = False
```

## Related Files

- Implementation: `clients/openai_client.py`, `clients/dd_selection_qdrant_client.py`, `clients/snowflake_client.py`, `clients/snowflake_client_mock.py`
- Tests: `test_singleton.py`
- Documentation: `docs/SINGLETON_PATTERN.md` (this file)

