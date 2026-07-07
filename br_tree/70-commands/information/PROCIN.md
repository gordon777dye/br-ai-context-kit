---
title: PROCIN
file: PROCIN.md
source: https://brulescorp.com/brwiki2/index.php?title=ProcIn
category: 70-commands
subcategory: 70-commands/information
kind: command
related: [internal function, procedure file]
---
PROCIN

The **ProcIn** `internal function` returns 0 if input is from the screen. Returns 1 if input is from a `procedure file`.

====Comments and Examples====
When RUN PROC is used to change programs to accept input from a procedure file instead of the screen, no code changes to the program are required. However, the input from the procedure is not echoed on the screen. The ProcIn variable can be tested in a program to provide this echo if desired.

 00010 PRINT "Enter T for totals or D for detail"
 00020 LINPUT A$
 00030 IF PROCIN=1 THEN PRINT A$
