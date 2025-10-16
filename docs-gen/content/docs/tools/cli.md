---
title: Command Line Interface (CLI)
weight: 1
chapter: false
---

## Export Commands

### Naming Configuration

All export commands support a global naming configuration feature that allows you to transform element names during the export process using the `[--naming-config | -n]` flag.

Apply naming configuration to any export command:

```bash
s2dm export [--naming-config | -n] naming.yaml ...
```

#### Configuration Format

The naming configuration is defined in a YAML file with the following structure:

```yaml
# Transform type names by type context
type:
  object: PascalCase
  interface: PascalCase
  input: PascalCase
  enum: PascalCase
  union: PascalCase
  scalar: PascalCase

# Transform field names by type context
field:
  object: camelCase
  interface: camelCase
  input: snake_case

# Transform enum values (no context needed)
enumValue: MACROCASE

# Transform instanceTag field names (no context needed)
instanceTag: COBOL-CASE

# Transform argument names by context
argument:
  field: camelCase
```

#### Supported Case Formats

The naming configuration supports the following case conversion formats:

- **camelCase**: `myVariableName`
- **PascalCase**: `MyVariableName`
- **snake_case**: `my_variable_name`
- **kebab-case**: `my-variable-name`
- **MACROCASE**: `MY_VARIABLE_NAME`
- **COBOL-CASE**: `MY-VARIABLE-NAME`
- **flatcase**: `myvariablename`
- **TitleCase**: `My Variable Name`

#### Example Conversion

Given this GraphQL schema:

```graphql
type vehicle_info {
  avg_speed: Float
  fuel_type: fuel_type_enum
}

enum fuel_type_enum {
  GASOLINE_TYPE
  DIESEL_TYPE
}
```

And this naming configuration:

```yaml
type:
  object: PascalCase
  enum: PascalCase
field:
  object: camelCase
enumValue: PascalCase
```

The exported schema will transform names as follows:

- Type: `vehicle_info` → `VehicleInfo`
- Field: `avg_speed` → `avgSpeed`
- Field: `fuel_type` → `fuelType`
- Enum type: `fuel_type_enum` → `FuelTypeEnum`
- Enum values: `GASOLINE_TYPE` → `GasolineType`, `DIESEL_TYPE` → `DieselType`

#### Validation Rules

The naming configuration system enforces several validation rules to ensure consistency and correctness:

**Element Type Validation:**

- **Valid element types**: Only `type`, `field`, `argument`, `enumValue`, and `instanceTag` are allowed
- **Context restrictions**: Some element types cannot have context-specific configurations:
  - `enumValue` and `instanceTag` are contextless and use a single case format
  - `argument` can only have `field` context
- **Value type validation**: Element values must be either strings (case formats) or dictionaries (for context-specific configurations)

**Context Validation:**

- **Type contexts**: `object`, `interface`, `input`, `scalar`, `union`, `enum`
- **Field contexts**: `object`, `interface`, `input`
- **Argument contexts**: `field`

**Case Format Validation:**

- **Valid case formats**: `camelCase`, `PascalCase`, `snake_case`, `kebab-case`, `MACROCASE`, `COBOL-CASE`, `flatcase`, `TitleCase`
- **Format enforcement**: Only recognized case formats are accepted; invalid formats will cause validation errors

**Special Rules:**

- **EnumValue-InstanceTag pairing**: If `enumValue` is present in the configuration, `instanceTag` must also be present
- **InstanceTag preservation**: The literal field name `instanceTag` is never transformed, regardless of naming configuration, to preserve its semantic meaning

#### Notes

- Built-in GraphQL types (`String`, `Int`, `Float`, `Boolean`, `ID`, `Query`, `Mutation`, `Subscription`) are never transformed
- If a configuration is not provided for an element type, the original names are preserved
- Configuration is loaded once at the command level and applied consistently across the entire export process
