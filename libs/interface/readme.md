# @r2d2/interface

## Overview

This library contains shared TypeScript interfaces, types, and constants used across our mobile, web, desktop, and IoT applications. By centralizing these definitions, we ensure consistent data structures and type safety throughout the R2D2 ecosystem.

## Purpose

- **Consistency**: Maintain uniform data structures across all platforms
- **Type Safety**: Prevent type-related bugs through shared interface definitions
- **DRY Principle**: Define once, use everywhere
- **Interoperability**: Ensure seamless communication between different application layers

## Key Components

- **API Models**: Request/response interfaces for backend communication
- **Entity Interfaces**: Core business objects definitions
- **Event Types**: Standardized event payload structures
- **Config Interfaces**: Configuration options for various services
- **Utility Types**: Shared utility types and type helpers

## Installation

```bash
npm install @r2d2/interface
```

## Usage

```typescript
import { UserProfile, AuthResponse } from '@r2d2/interface';

// Type-safe function using shared interfaces
function processUserData(user: UserProfile): AuthResponse {
    // Implementation
}
```

## Contributing

When adding new interfaces or modifying existing ones, ensure they're:
- Well-documented with JSDoc comments
- Platform-agnostic when possible
- Properly exported from the index file

See the [contribution guidelines](../CONTRIBUTING.md) for more information.