# 30-io-file/database

SQL / ODBC database access: connecting BR as a SQL client, opening SQL channels, and reading/writing result rows.

**📄 Guide → [spec.md](spec.md)** _(status: draft)_ — How a BR program connects to an external SQL database over ODBC (CONFIG DATABASE), binds a statement to a channel (OPEN…SQL, OUTIN), executes it (WRITE), fetches rows (READ USING a FORM), and closes.

_New leaf synthesized from the BR SQL example set; pending 2b verification._
