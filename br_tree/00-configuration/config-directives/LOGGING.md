---
title: LOGGING
file: LOGGING.md
source: https://brulescorp.com/brwiki2/index.php?title=Logging
category: 00-configuration
subcategory: 00-configuration/config-directives
kind: config-directive
related: [config, BRConfig.sys, commands, BR program, PRINT, TRACE, DISPLAY, 4.3, GUI, MyEditBR]
---
As of 4.3, the debug versions of BR now expect you to use a LOGGING configuration statement. This enables BR to post exit messages during unexpected terminations.

The **Logging** `config` statement is provided for logging configuration errors, and should be placed in `BRConfig.sys`:

 LOGGING <loglevel>, <native-OS-logfile-name> [, UNATTENDED] [, DEBUG_LOG_LEVEL=<integer>] [, +CONSOLE]

`IMAGE:Logging.png|700px`

**Loglevel**  is the maximum level of detail to be logged. The Logging Level is meant to specify the level of detail to be logged, with greater detail logged at higher log levels:

{|Border=1
|-
|0
|MAJOR_ERROR
|causes major problems during execution
|-
|1
|NOTABLE_ERROR
|unexpected error likely to cause problems
System generated warning messages such as OS failures and abnormal exits.
|-
|2
|MINOR_ERROR
||unexpected error that can be ignored
System generated warning messages such as OS failures and abnormal exits.
|-
|3
|MAJOR_EVENT
|starting program, exiting, shelling ...
System generated warning messages such as OS failures and abnormal exits.
|-
|4
|SECURITY_EVENT
|logons, logon attempts etc
|-
|5
|MINOR_EVENT
|individual `commands` ...
User Logon data, including any attempts.
|-
|6
|
|Starting a `BR program`, exiting.
|-
|8
|
|`Commands` such as COPY plus shell calls with parameters.
|-
|9
|DEBUGGING_EVENT
|added for debugging purposes
|-
|11
|
|Any `PRINT` output that goes to the console is also logged (GUI ON only).
|-
|12
|
|`TRACE`, and `DISPLAY` messages.
|-
|13
|
|Lots of what the system is doing now messages.
|-
|}

**Logfile** denotes where the logging records will be kept. **Note that Logfile is a native OS filename.** Second and subsequent occurrences of the LOGGING statement may omit loglevel and logfile.

The **UNATTENDED** keyword will cause BR to run in unattended mode, without a startup screen and until a program begins to await operator input, when it will exit. Config LOGGING loglevel logfile [UNATTENDED] is now supported on linux (4.2) and this will exit BR if the program starts to wait for keyboard entry. 

**DEBUG_LOG_LEVEL** (available as of `4.3`) specifies the log level for debugging log messages independently of the standard log level. If not specified, the Debug_Log_Level is set to the standard loglevel.

**+CONSOLE** (4.3) applies only when `GUI` is ON and specifies that all logging messages also go to the console and the console is to be left visible when not attached to `MyEditBR`. (Console logging output is supressed when GUI is OFF.)

====Examples====
 LOGGING 2, logfile
shows unsupported escape sequences encountered.

 LOGGING 5, logfile
shows unsupported escape sequences encountered plus intentionally ignored escape sequences.

 LOGGING 2, logfile ,UNATTENDED
shows unsupported escape sequences encountered, and runs BR in 'Unattended' mode, bypassing start-up screen and terminating BR at the end of processing or when input is required.  Supported in 4.18 in Windows and 4.20 under Linux.

  LOGGING ,,UNATTENDED
runs in `Unattended mode` without log file.

Any config messages that occur after this config statement will be sent only to the logfile, mostly with NOTABLE_ERROR.  It avoids displaying those REMed out statements in front of operators.

Any config messages that occur before the config statement logging will be sent only to the screen.  These will cause BR to pause a few seconds so that the messages can be viewed.

===Logging Messages (4.3)===

Message Levels are compared with Log Levels during the filtering process. Like log levels, there is greater detail logged at higher log levels:

The following types of messages are written to the LOGGING file:

1. Config error messages based on their assigned level of importance.

2. DEBUG_STR() messages where message-level is equal to or less than the DEBUG_LOG_LEVEL:

{|
|- valign="top"
| width="20%" | **Log levels 0, 1, 2 and 3** 
| System generated warning messages such as OS failures and abnormal exits.
|
|- valign="top"
| width="20%" | **Log level 5 or above** 
| User Logon data, including any logon attempts.
|
|- valign="top"
| width="20%" | **Log level 6 or above** 
| Starting a BR program, exiting.
|
|}
Any DEBUG_STR() calls with a level >10 are deemed to be message level 10.

Commands such as COPY plus shell calls with parameters are logged with system generated warning messages such as OS failures and abnormal exits.

====LOGGING PDF printing events====

Logging was added to PDF creation. Logging of minor events that happen during the printing process are logged at log level 8.  Errors are logged at a lower level. Logging was also improved with respect to loading older versions of pdflib.
Note- As a diagnostic, the following command is quite useful: 
DIR >PDF:/READER

The following messages are written to the LOGFILE:

{|
|- valign="top"
| width="20%" | **Log level 11 or above** 
| Any PRINT output that goes to the console is also logged (GUI ON only).
|
|- valign="top"
| width="20%" | **Log level 12 or above** 
| TRACE, and DISPLAY messages.
|
|- valign="top"
| width="20%" | **Log level 13 or above** 
| Lots of what the system is doing now messages.
|}

;Examples:
Log Level Indication is given in Log Messages The (6) here is the log level:
  (6) - 08/25/2011 11:33:53
Setting logging to log file logfile.txt log level 10.
  (6) - 08/25/2011 11:33:53
The BRConfig.sys file is C:\Users\dan\programs\cygwin\home\dan\br-wx\br\winbuild\dllbuild\output\brconfig.sys

====See Also====
*`Debug_Str` 

====Logging Abnormal Termination====
A logging capability is provided for handling `BRServer` failures. An error log file in the BRServer directory is appended to when a BRServer process is abnormally ended. Also, a `client` `msgbox` is displayed when an `assertion failure` or program crash occurs. On `Unix` systems, the system error log is also updated. `Keepalive` failures are also logged here.
