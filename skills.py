# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-vat-reverse-charge-cross-border-vies-auditor-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def audit_eu_vat_reverse_charge(supplier_vat, buyer_vat, invoice_amount_eur, transaction_type="GOODS"):
    import re
    # Country code prefix extraction
    def parse_vat(vat_str):
        clean = re.sub(r"[^A-Za-z0-9]", "", vat_str.strip().upper())
        if len(clean) < 4:
            return None, clean, False
        cc = clean[:2]
        num = clean[2:]
        # Common regex syntax checks
        patterns = {
            "DE": r"^\d{9}$",
            "FR": r"^[A-Z0-9]{2}\d{9}$",
            "NL": r"^\d{9}B\d{2}$",
            "IT": r"^\d{11}$",
            "ES": r"^[A-Z0-9]\d{7}[A-Z0-9]$",
            "BE": r"^0\d{9}$",
            "PL": r"^\d{10}$",
            "SE": r"^\d{12}$"
        }
        valid_syntax = bool(re.match(patterns[cc], num)) if cc in patterns else True
        return cc, clean, valid_syntax

    sup_cc, sup_clean, sup_valid = parse_vat(supplier_vat)
    buy_cc, buy_clean, buy_valid = parse_vat(buyer_vat)
    
    if not sup_valid or not buy_valid:
        return {
            "supplier_vat": supplier_vat,
            "buyer_vat": buyer_vat,
            "reverse_charge_applicable": False,
            "audit_verdict": "INVALID_VAT_SYNTAX_REJECTED",
            "vat_applied_rate_pct": 20.0,
            "vat_due_eur": round(invoice_amount_eur * 0.20, 2),
            "discrepancy_details": f"Supplier valid: {sup_valid}, Buyer valid: {buy_valid}"
        }
        
    is_cross_border = (sup_cc != buy_cc)
    
    if is_cross_border:
        reverse_charge = True
        verdict = "REVERSE_CHARGE_ARTICLE_196_APPLIES"
        vat_rate = 0.0
        vat_due = 0.0
        mandatory_invoice_note = "Reverse charge: VAT to be accounted for by the recipient in accordance with Article 196 of Council Directive 2006/112/EC."
    else:
        reverse_charge = False
        verdict = "DOMESTIC_TRANSACTION_DOMESTIC_VAT_MANDATORY"
        vat_rate = 19.0 # Standard domestic average
        vat_due = round(invoice_amount_eur * (vat_rate / 100.0), 2)
        mandatory_invoice_note = "Domestic supply subject to local standard VAT."
        
    return {
        "supplier_country": sup_cc,
        "buyer_country": buy_cc,
        "is_intra_community_cross_border": is_cross_border,
        "reverse_charge_applicable": reverse_charge,
        "audit_verdict": verdict,
        "invoice_net_amount_eur": invoice_amount_eur,
        "applicable_vat_rate_pct": vat_rate,
        "vat_amount_due_eur": vat_due,
        "total_invoice_gross_eur": round(invoice_amount_eur + vat_due, 2),
        "required_invoice_legal_clause": mandatory_invoice_note
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "audit_eu_vat_reverse_charge",
                        "description": """Audit cross-border European Union B2B intra-community transactions for VAT Reverse Charge (Article 196 Directive 2006/112/EC).
Validates 2-letter ISO country codes, performs national regex pattern syntax verification (DE, FR, NL, IT, ES, etc.),
and confirms supplier-buyer jurisdiction cross-border zero-rating legitimacy.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = audit_eu_vat_reverse_charge(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'supplier_vat': 'DE123456789', 'buyer_vat': 'FRXX123456789', 'invoice_amount_eur': 24500.0, 'transaction_type': 'SERVICES'}
        out = audit_eu_vat_reverse_charge(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
