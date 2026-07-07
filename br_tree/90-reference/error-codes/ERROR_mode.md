---
title: ERROR_mode
file: ERROR_mode.md
source: https://brulescorp.com/brwiki2/index.php?title=ERROR
category: 90-reference
subcategory: 90-reference/error-codes
kind: error-code
related: [Error Handling Statements, END, STOP, CLEAR, READY mode, ATTN mode, STEP mode, PAUSE mode]
---
When entering a program line or running a program without error handling statements (see `:Category:Error Conditions` and `Error Handling Statements`), and BR encounters an error, it will beep, stop, and display "ERROR" and the error code in the bottom line. This allows you to take steps towards debugging the problem, however, note that the program must be stopped in order to make changes or add new lines.

From ERROR mode, the program can continue by typing GO, or end using `END`, `STOP` or `CLEAR`. It is possible to execute most Business Rules instructions, including LIST (to see the program) and PRINT (to test the value of variables).

See also:

`READY mode`

`ATTN mode`

`STEP mode`

`PAUSE mode`
