# Data Security – Class Work3  
Team: עבד אבו עצבה 324277581 
Project link: https://github.com/Abedasbe/Data_Security_classwork

# 1 Overview
classwork1 encoding the passwords using sha256
Classwork2 delivered a working Flask login/sign‑up system.  
Classwork3 hardens that system against SQL‑Injection.

# 2 Practical Mitigation Implemented

| Technique | Implementation | Why It Stops SQL‑Injection |
|-----------|----------------|----------------------------|
| 1. Parameterised Queries | `db.execute("… WHERE username = ?", (u,))` | DB engine treats user input as literal data– no chance to alter query logic. |
| 2. Password Hashing (SHA‑256) | Stored and compared as `<hex‑digest>` | Eliminates plaintext leakage; prevents attacker re‑using injected passwords. |
| 3. Illegal‑Character Filter| Regex`[\'\";#\-]` on username & password fields | Blocks classic payload building blocks (`' OR 1=1 --`). |

# Evidence
1. Normal login → success.  
2. Attempt payload in password field: `' OR 1=1 --` → fails with Illegal characters* flash.  
3. No table alteration is possible; the schema is intact.

# 3 Three Additional Mitigations (Not in Moodle Doc)

# 3.1 Stored Procedures
SQL logic is pre‑compiled inside the DB; the application only supplies parameters.  
*Attack surface*: user input never concatenated into SQL text.

# 3.2 Least‑Privilege DB Accounts
The web app uses an account without `DROP`, `ALTER`, or other DDL rights.  
Even if injection succeeds, the attacker cannot modify the schema or access other tables.

# 3.3 Web Application Firewall (WAF)
Layer‑7 proxy that inspects traffic for SQL‑Injection signatures (`UNION SELECT` etc.) and blocks before reaching the server.  
Provides zero‑code protection and real‑time alerts.

## 4 Conclusion
Combining parameterized queries with input validation and hashed credentials eliminates practical SQL‑Injection in our Flask project. Additional defence‑in‑depth measures (stored procedures, least‑privilege, WAF) further reduce residual risk.



