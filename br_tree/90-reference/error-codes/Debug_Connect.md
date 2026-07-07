---
title: Debug_Connect
file: Debug_Connect.md
source: https://brulescorp.com/brwiki2/index.php?title=Debug
category: 90-reference
subcategory: 90-reference/error-codes
kind: error-code
related: [command, debugger]
---
The **debug connect** `command` is used to connect a `debugger` for the `editor|editor's` debugging purposes.

* debug connect localhost
* debug connect 127.0.0.1
* debug connect

The debug connect command tries to establish a TCP connection on a specific port where it starts listening for commands from the debugger. Once a connection is established the BR console is disabled and made non-visible.

Properly formatted commands from the debugger are treated exactly as if they were typed in on the standard BR console window.

===Syntax===

 DEBUG CONNECT {[LOCALHOST]|[<ip address>]}
`IMAGE:DebugConnect.png`
