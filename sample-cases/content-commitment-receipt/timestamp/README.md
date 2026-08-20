# External Timestamp Hook

The synthetic receipt has no independent timestamp and therefore records:

```json
"external_anchor": null
```

## RFC 3161 request example

After creating a receipt, an operator could generate a timestamp query over its exact bytes:

```bash
openssl ts -query \
  -data lifecycle/02-public-commitment/receipt.json \
  -sha256 \
  -cert \
  -out timestamp/receipt.tsq
```

The query would then need to be submitted to an independently selected timestamp authority according to that provider's documented interface.

A `.tsq` request alone proves nothing about time. The relevant evidence would be the authority's signed response, an accepted trust chain, provider policy, and reproducible verification output.

## Typical response verification shape

Provider requirements vary, but an OpenSSL command commonly resembles:

```bash
openssl ts -verify \
  -queryfile timestamp/receipt.tsq \
  -in timestamp/receipt.tsr \
  -CAfile timestamp/tsa-trust-chain.pem
```

Successful execution would support only that the response validates under the supplied trust chain and corresponds to the query. It would not independently establish that the trust chain or authority should be accepted.

## Byte-preservation warning

Do not modify the receipt after creating the timestamp request. Anchor metadata should be preserved as a separate sidecar unless a separately defined envelope format covers it.
