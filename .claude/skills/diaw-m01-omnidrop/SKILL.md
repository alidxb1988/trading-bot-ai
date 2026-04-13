---
name: diaw-m01-omnidrop
description: >
  OMNI-DROP: AI-powered e-commerce and dropshipping module. Builds complete
  online stores with product sourcing, store design, SEO optimization,
  inventory management, order fulfillment automation, A/B testing, and
  conversion optimization. Activates on OMNI-DROP, e-commerce, dropshipping,
  Shopify, WooCommerce, online store, product sourcing, store builder.
user-invocable: true
context: fork
effort: high
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__ruflo__*
  - mcp__firecrawl__*
  - mcp__stripe__*
---

# OMNI-DROP: E-Commerce Module v3.0

## Agent Swarm Configuration
- **Topology**: Hierarchical | **Max Agents**: 5 | **Quality Gate**: 0.95
- **Agents**: Coordinator, Product Researcher, Store Designer, SEO Specialist, Fulfillment Manager

## Store Building Workflow

| Phase | Agent | Activities |
|-------|-------|------------|
| 1. Niche Research | Product Researcher | Market sizing, competitor analysis, trend identification, margin analysis |
| 2. Product Sourcing | Product Researcher | Supplier identification (AliExpress, CJ, Spocket), quality assessment, cost/margin calc |
| 3. Store Design | Store Designer | Theme selection, homepage/collection/product pages, mobile-first, brand identity |
| 4. SEO Setup | SEO Specialist | Keyword mapping, meta tags, product schema, blog content plan, internal linking |
| 5. Launch | Coordinator | Payment (Stripe), shipping rules, email automation, GA4 setup, QA |
| 6. Growth | All agents | A/B testing, retargeting setup, email sequences, social storefronts |

## Revenue Model
- **Subscription**: $97-$997/mo based on tier
- **Setup Fee**: $500-$2,000 per store
- **Transaction Fee**: 1-2% of GMV
- **Credits**: 15-50 per store build

## Example Invocations
- "Launch OMNI-DROP for a pet accessories Shopify store targeting dog owners in the US"
- "Use OMNI-DROP to analyze the top 10 competitors in sustainable fashion"
- "OMNI-DROP: Optimize my existing store's product pages for higher conversion"
- "Build a complete dropshipping store for home office equipment under $500 budget"
