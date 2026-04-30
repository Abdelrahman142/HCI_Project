# HCI_Project

1. Problem Definition & Objectives
Problem: Many small businesses struggle with managing customer/product records without a user-friendly, secure, and visually comfortable interface. Existing solutions often have poor HCI design (harsh colors, small fonts, confusing workflows) and weak data security.

Objectives:

Design an intuitive GUI with eye-friendly colors (soft blues, greens, and neutral backgrounds)

Implement secure SQLite database with password hashing

Provide search functionality by name, code, and date

Display searched data in an editable data grid

Create insert forms for all database tables

Implement deletion confirmation dialogs

Show attention alerts for critical actions
```
2. Programming Languages & IDE
Component----->	Technology
Language------>	Python 3.11+
GUI Framework---> Tkinter + ttk (Themed Tkinter)
Database------->	SQLite3
IDE-------->      VS Code / PyCharm
Additional Libraries-------> hashlib (for password hashing), datetime

```
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
