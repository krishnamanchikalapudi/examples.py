# Architecture Documentation

## Design Principles

### DRY (Don't Repeat Yourself)
- **Configuration Management**: Centralized in `src/config.py` with environment variable support
- **Logging**: Single logger setup in `src/logger.py` used throughout
- **Error Handling**: Global error handling middleware
- **Security**: Reusable security service and dependencies

### KISS (Keep It Simple, Stupid)
- **Clear Separation**: Each module has a single, clear purpose
- **Minimal Dependencies**: Only essential production dependencies
- **Straightforward API**: Simple, intuitive MCP protocol implementation
- **No Over-Engineering**: Solutions match the problem complexity

### SOLID Principles

#### Single Responsibility Principle (SRP)
- `MCPProtocolHandler`: Only handles protocol message routing
- `CacheService`: Only manages caching operations
- `CircuitBreaker`: Only implements circuit breaker pattern
- `SecurityService`: Only handles authentication/authorization

#### Open/Closed Principle (OCP)
- Middleware system allows extension without modification
- Handler registry allows adding new MCP methods without changing core
- Configuration system extensible via environment variables

#### Liskov Substitution Principle (LSP)
- All handlers implement consistent interface
- Cache implementations can be swapped (Redis, in-memory, etc.)

#### Interface Segregation Principle (ISP)
- Small, focused interfaces (dependencies)
- Handlers only receive what they need

#### Dependency Inversion Principle (DIP)
- Dependencies injected via FastAPI's dependency system
- Configuration accessed via `get_settings()` function
- Services depend on abstractions, not concrete implementations

## Component Architecture

### 1. Application Layer (`src/server.py`)
- FastAPI application setup
- Middleware configuration
- Route definitions
- Lifecycle management

### 2. Protocol Layer (`src/mcp/`)
- **protocol.py**: MCP protocol message models and handler
- **handlers.py**: Implementation of MCP methods (tools, resources, prompts)

### 3. Infrastructure Layer

#### Configuration (`src/config.py`)
- Environment-based configuration
- Type validation with Pydantic
- Cached settings for performance

#### Logging (`src/logger.py`)
- Structured JSON logging
- Configurable log levels and formats
- Correlation ID support

#### Security (`src/security.py`)
- JWT token management
- API key validation
- Rate limiting integration

#### Caching (`src/cache.py`)
- Redis-backed caching
- Graceful degradation if Redis unavailable
- TTL support

#### Resilience (`src/circuit_breaker.py`, `src/retry.py`)
- Circuit breaker pattern for fault tolerance
- Retry with exponential backoff
- Configurable thresholds

### 4. Middleware Layer (`src/middleware.py`)
- Correlation ID tracking
- Request/response logging
- Security headers
- Global error handling

## Data Flow

### Request Flow
```
Client Request
    ↓
FastAPI Middleware Stack
    ├─ SecurityHeadersMiddleware
    ├─ ErrorHandlingMiddleware
    ├─ CorrelationIDMiddleware
    └─ LoggingMiddleware
    ↓
Rate Limiting (SlowAPI)
    ↓
Route Handler (/mcp)
    ↓
MCPProtocolHandler
    ├─ Parse Request
    ├─ Find Handler
    └─ Execute Handler
        ├─ Circuit Breaker Check
        ├─ Cache Check (if applicable)
        ├─ Retry Logic (if applicable)
        └─ Execute Business Logic
    ↓
Build Response
    ↓
Log Response
    ↓
Return to Client
```

### Error Flow
```
Exception Raised
    ↓
Circuit Breaker (if applicable)
    ├─ Record Failure
    └─ Open Circuit (if threshold reached)
    ↓
Retry Logic (if applicable)
    ├─ Wait (exponential backoff)
    └─ Retry
    ↓
Error Handling Middleware
    ├─ Log Error
    ├─ Format Error Response
    └─ Return Error
```

## Scalability Design

### Horizontal Scaling
- **Stateless Design**: No session state, all requests independent
- **Kubernetes HPA**: Auto-scaling based on CPU/memory
- **Load Balancing**: Works behind any load balancer
- **Shared Cache**: Redis enables shared state across instances

### Vertical Scaling
- **Async I/O**: Non-blocking operations maximize throughput
- **Connection Pooling**: Efficient resource usage
- **Resource Limits**: Configurable in K8s deployment

## Security Architecture

### Authentication Flow
```
Request with API Key
    ↓
API Key Header Extraction
    ↓
SecurityService.verify_api_key()
    ↓
HMAC Comparison
    ↓
Authorized/Unauthorized
```

### JWT Token Flow
```
Request with Bearer Token
    ↓
Token Extraction
    ↓
SecurityService.verify_token()
    ↓
JWT Decode & Validation
    ↓
User Payload Extraction
    ↓
Authorized Request
```

## Observability Architecture

### Logging
- **Format**: JSON for machine parsing
- **Correlation IDs**: Track requests across services
- **Structured Fields**: Consistent log structure
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Metrics
- **Prometheus Format**: Standard metrics endpoint
- **Custom Metrics**: Request counts, error rates, latency
- **Integration**: Ready for Prometheus scraping

### Tracing
- **OpenTelemetry**: Distributed tracing support
- **Correlation**: Correlation IDs link logs and traces
- **Integration**: Ready for Jaeger, Zipkin, etc.

## Deployment Architecture

### Container Strategy
- **Multi-stage Build**: Smaller production image
- **Non-root User**: Security best practice
- **Health Checks**: Built-in container health checks
- **Read-only Filesystem**: Enhanced security

### Kubernetes Strategy
- **Deployment**: Stateless deployment with replicas
- **Service**: ClusterIP for internal access
- **HPA**: Auto-scaling based on metrics
- **ConfigMap**: Configuration management
- **Secrets**: Secure secret management

### Docker Compose Strategy
- **Development**: Local development with Redis
- **Networking**: Isolated network for services
- **Volumes**: Persistent Redis data
- **Health Checks**: Service health monitoring

## Integration Patterns

### API Gateway Integration
- Works behind Kong, AWS API Gateway, etc.
- Standard HTTP/HTTPS protocol
- Health checks for gateway routing

### Service Mesh Integration
- Compatible with Istio, Linkerd
- mTLS support ready
- Traffic management compatible

### Message Queue Integration (Future)
- Can be extended for async processing
- Circuit breakers protect queue operations
- Retry logic for queue failures

## Performance Optimizations

### Caching Strategy
- **Cache-Aside Pattern**: Check cache, then source
- **TTL Management**: Configurable expiration
- **Graceful Degradation**: Works without cache

### Connection Management
- **Connection Pooling**: Redis connection reuse
- **Async Operations**: Non-blocking I/O
- **Resource Cleanup**: Proper connection closing

### Response Optimization
- **Compression**: Can be added via middleware
- **Pagination**: For large result sets
- **Selective Fields**: Return only needed data

## Failure Modes & Recovery

### Circuit Breaker States
1. **CLOSED**: Normal operation
2. **OPEN**: Failing, reject requests immediately
3. **HALF_OPEN**: Testing recovery, allow limited requests

### Retry Strategy
- **Exponential Backoff**: Increasing delays between retries
- **Max Retries**: Configurable limit
- **Exception Filtering**: Only retry specific exceptions

### Error Handling
- **Graceful Degradation**: Continue operating with reduced functionality
- **Error Responses**: Consistent error format
- **Logging**: All errors logged with context

## Cost Optimization Strategies

### Resource Efficiency
- **Right-sizing**: Appropriate resource requests/limits
- **Scale-to-Zero**: Can scale down when idle
- **Efficient Algorithms**: Optimized code paths

### Infrastructure Costs
- **Container Efficiency**: Small image size
- **Shared Resources**: Redis shared across services
- **Auto-scaling**: Pay only for what you use

## Future Enhancements

### Potential Additions
- Database persistence layer
- Message queue integration
- Advanced caching strategies
- GraphQL support
- WebSocket support for real-time updates
- Advanced metrics and dashboards
- Multi-region deployment support

