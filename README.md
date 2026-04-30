# HCI_Project

``` erd ```
```
┌─────────────────┐     ┌─────────────────┐
│     Client      │     │     Product     │
├─────────────────┤     ├─────────────────┤
│ PK │ client_id  │     │ PK │ product_id │
│    │ name       │     │    │ code       │
│    │ email      │     │    │ name       │
│    │ phone      │     │    │ price      │
│    │ created_at │     │    │ stock      │
└────────┬────────┘     │    │ created_at │
         │              └────────┬────────┘
         │                       │
         │    ┌──────────────────┘
         │    │
         ▼    ▼
┌─────────────────────────────────┐
│           Transaction           │
├─────────────────────────────────┤
│ PK │ transaction_id             │
│ FK │ client_id                  │
│ FK │ product_id                 │
│    │ transaction_code           │
│    │ quantity                   │
│    │ total_price                │
│    │ transaction_date           │
└─────────────────────────────────┘
```
