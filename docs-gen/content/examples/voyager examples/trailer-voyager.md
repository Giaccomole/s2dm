---
title: "Trailer GraphQL Voyager Visualization"
description: "Explore the seat capabilities domain model through an interactive GraphQL Voyager visualization"
layout: fullwidth
weight: 12
---

# Interactive GraphQL Schema Visualization

Explore the trailer domain model through an interactive [GraphQL Voyager](https://github.com/graphql-kit/graphql-voyager) visualization. This comprehensive schema, is derived from the [Vehicle Signal Specification (VSS)](https://covesa.github.io/vehicle_signal_specification/) `Trailer` branch.

{{< callout type="tip" >}}
**Usage:** Click and drag to navigate • Click types for details • Use the sidebar to search and explore documentation • Zoom with mouse wheel for different perspectives.
{{< /callout >}}

---

{{< graphql-voyager-builtin schema="/examples/trailer/full_schema.graphql" height="1000px" title="Trailer Capabilities Domain Model" hideDocs="false" hideSettings="false" hideVoyagerLogo="true" showLeafFields="true" skipRelay="true" skipDeprecated="true" >}}

