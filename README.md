# genpark-agentic-commerce-vat-reverse-charge-cross-border-vies-auditor-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

EU VAT reverse charge compliance, real-time VIES VAT number syntax and validity batch verification engine.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `audit_eu_vat_reverse_charge`
- **Category**: `agentic_commerce`

### Method Documentation
Audit cross-border European Union B2B intra-community transactions for VAT Reverse Charge (Article 196 Directive 2006/112/EC).
Validates 2-letter ISO country codes, performs national regex pattern syntax verification (DE, FR, NL, IT, ES, etc.),
and confirms supplier-buyer jurisdiction cross-border zero-rating legitimacy.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "audit_eu_vat_reverse_charge",
    "arguments": {
    "supplier_vat": "DE123456789",
    "buyer_vat": "FRXX123456789",
    "invoice_amount_eur": 24500.0,
    "transaction_type": "SERVICES"
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
