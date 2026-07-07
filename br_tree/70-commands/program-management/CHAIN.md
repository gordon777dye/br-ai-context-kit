---
title: CHAIN
file: CHAIN.md
source: https://brulescorp.com/brwiki2/index.php?title=Chain
category: 70-commands
subcategory: 70-commands/program-management
kind: command
related: [statement]
---
The **Chain** (CH) `statement` ends the current program and starts execution of another program, procedure, or sub-procedure.

===Comments and Examples===
CHAIN is most often used to chain from one program to another. To do this you just type CHAIN and indicate the name of the desired program.

The statement in the following example causes the system to end the current program and load the program MENU.BR (or MENU.BRO) from a subdirectory called MAIN:

 00350 CHAIN "MAIN\MENU"

The next example loads and runs the program GLEDIT.BR (or GLEDIT.BRO) from the subdirectory GLPROG (a subdirectory of the root directory). All files stay open at their current positions. The variable D$ retains its current value at the start of the new program; all other variables return to zeros or null strings.

 00900 CHAIN "C:\GLPROG\GLEDIT" ,FILES,D$

To chain from a program to a procedure or sub-procedure (rather than another program), you must have either "PROC=" or "SUBPROC=" immediately before the name of the desired file, as in the following two examples:

 00900 CHAIN "PROC=GLPOST"

 00080 NAME$="EDITLIST.PRC"
 00090 X$="SUBPROC=GLPROG\"&NAME$
 00100 CHAIN X$

When a program chains to a procedure (PROC or SUBPROC), the procedure acts much like the operator stopped the program and started entering commands. A procedure is a set of commands. (However a procedure can skip forward or backward within itself.) While it is emulating a series of commands, the program that initiated the procedure is retained in memory even though the CHAIN statement terminated it. Therefore its variable contents are accessible to the procedure. 

The following example specifies that the string array A$ and the numeric variables B and C are to retain their values in the chained-to program:

 60000 CHAIN PROG$,MAT A$,B,C

===Syntax===
 CHAIN {"<program name>"|”PROC=<name>”|”SUPROC=<name>”|”<path>\<name>”} [,FILES] [,MAT<array name>][,...] [,<variable name>][,...]

`file:Chain.png|700px`

===Defaults===
# Load and run a program.
# Close all open files (except procedure files).
# Set all variables in the chained-to program to blanks or zeros.

===Parameters===
The only required parameter of the CHAIN statement is the "file-ref", which specifies the program, procedure, or sub-procedure to be executed. This name and subdirectory information may be specified as a quoted literal string or as a string variable. 

If the file-ref is preceded with the string "PROC=", the CHAIN initiates a procedure. If the file-ref is preceded with the string "SUBPROC=", the CHAIN initiates a sub-procedure. If neither of these keywords is present, the CHAIN statement attempts to load and run a program.

The differtence between PROC and SUBPROC is that PROC will close the current (lowest level) PROC file (if one is running) before starting the specifified procedure, whereas SUBPROC will not affect a currently running PROC file. 

The parameters following the file-ref apply only to programs and not procedures.

Following the file-ref information, CHAIN can take three optional parameters, but these parameters should be included only when chaining to a program.

"FILES" indicates that all files are to remain open and at their current positions. If you do not specify "FILES", the CHAIN statement closes all files except procedure files.

The "MAT array-name" and "variables" parameters allow the specified arrays or variables to retain their current values in the chained-to program. If several are used they are seperated by commas.

===Technical Considerations===
# Array variables and string variables passed between programs by a CHAIN statement, are not required to be dimensioned the same way in both programs. If dimensions do not match, the dimensions in the first program will override those in the DIM statements of the second program. However, it is recommended for improved readability that dimensions should match in both programs. Arrays may be re-dimensioned in the second program.
# Options selected in an OPTION statement are not required to be the same in both programs. However, it is strongly recommended that these options be the same. For example, if the first program uses BASE 1 and the second program uses BASE 0, confusing results could "run rampant" because the last element of a 10-element array would have a subscript of 10 in the first program and 9 in the second program.
# RUN command options, which are active in the initial program, will remain active in the chained program. These options include RUN PROC and output redirected to a file (see the RUN command for more information).
# In Business Rules, there is no need for a USE statement in the program being chained. USE is treated as a comment and is maintained only for compatibility with IBM Business BASIC.
# Although Business Rules checks most statements for proper syntax as they are entered, the file-ref parameter of the CHAIN statement is not checked until execution (this is also true in the OPEN statement). In this case, variables and quoted strings cannot be checked until execution.  # IBM Business BASIC restricted the use of CHAIN statements within IF statements; if the THEN clause was a CHAIN statement, the ELSE clause was not permitted. This restriction does not apply to Business Rules. The following statement is allowed: 90 IF X=0 THEN CHAIN "MENU" ELSE CHAIN "PR2"
# The rules for the default extension of a program name, which is specified in a CHAIN statement, are the same as the rules for the LOAD command. In short, the system first looks for an extension of .BR; if that is not present, the system then looks for .BRO. You can change these defaults with the CHAINDFLT specification in the BRConfig.sys file. You can also override the defaults from within the CHAIN statement by specifying your own extension, as in the following example:900 CHAIN "C:\MAIN\MENU.OLD"
# The ability to pass specified variables from a program to a procedure is not explicitly supported in Business Rules because the values of all variables are available at the end of a program. These variables retain their values until a SORT, INDEX, CLEAR, or LOAD command is encountered from the keyboard or from a procedure file. This means that any variable from the calling program could be tested by a SKIP command (or therwise used) in a procedure file. (Notice that this also means those values of all variables are available to an opertor after program termination for interrogation [displaying contents] and debugging.)
# Like most Business Rules statements, CHAIN may be used in immediate mode like a command (except with the EXECUTE statement, where commands may not terminate a program.) Within a procedure, the following two commands are equivalent: PROC EOM - CHAIN "PROC=EOM". The next two commands would also be equivalent within a procedure: SUBPROC EOM - CHAIN "SUBPROC=EOM". Although using CHAIN, as a command may not seem very useful because the simpler PROC and SUBPROC alternatives exist, CHAIN allows a procedure to pass variables from it's parent or itself to a program. For example, a procedure file might start a program to print designated messages for certain completion codes as follows: LOAD PROG1 - RUN - X=CODE - SKIP 1 IF X=0 - CHAIN "MESSAGE", X. This passes the variable X (created by PROG1 or the procedure) to be passed to the program named MESSAGE. The same is true if a program CHAINS to a procedure and the procedure simply forwards variables from the chaining program to anotherr program.
# CHAIN "PROC=XYZ" is similar to EXECUTE "PROC XYZ", except EXECUTE does not end the program. That being said, the procedure has the authority to end the program that called it via EXECUTE. 
# If the FILES keyword is used to keep files open, file pointers are not moved. Thus, pointers, which were at the end of the file in the first program, will also be at the end of the file in the second program; you may use a RESTORE statement to reposition a file pointer.
