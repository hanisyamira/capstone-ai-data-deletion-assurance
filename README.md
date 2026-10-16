# AI Data Deletion Assurance Engine — Capstone Demonstration

Streamlit read-only governance dashboard. No live deletion, Ollama, ChromaDB, or Microsoft Purview connection is included.

## Deploy
1. Upload these files to the root of a GitHub repository.
2. Visit https://share.streamlit.io and deploy the repository with entrypoint `dashboard.py`.
3. Open the resulting URL and test all eight modules.

## Evidence files
`data_lineage.json` and `audit_log.json` contain empty lists by default. This is intentional: no fabricated verification events or sensitive personal data are included. To show historical results, replace them with **sanitised synthetic/example** JSON arrays matching your local schema. Never publish actual personal information, secrets, or confidential audit records.

## Limitations
This is a publicly accessible, read-only evidence viewer when deployed publicly. It does not execute deletion or verify external systems in real time. Review hosting permissions before sharing.

## Public demo data
The included JSON records are based on supplied prototype evidence. Source hashes have been removed for safer public demonstration. Review all records for confidentiality and ensure all content is synthetic before publishing. Historical verification statuses are not live tests.
