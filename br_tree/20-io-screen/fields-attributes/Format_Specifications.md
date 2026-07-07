---
title: Format_Specifications
file: Format_Specifications.md
source: https://brulescorp.com/brwiki2/index.php?title=Format
category: 20-io-screen
subcategory: 20-io-screen/fields-attributes
kind: statement
related: [File I/O, Business Rules!, string, numeric, internal, external, READ, REREAD, statements, WRITE]
---
The page presents a summary chart of format specifications. Also see `:Category:Format Specifications` and `File I/O`  for detailed descriptions of each format.

The following table shows where and how each of `Business Rules!` **format specifications** may be used. 

"S", "N" and "I" indicate whether the specification is a `string`, `numeric` or internal format spec.

The next two columns show what happens when the format specification is used with `internal` or `external` files, either for input (with the `READ`/`REREAD` `statements`) or for output (with the `WRITE`/`REWRITE` statements).

The column labeled "PRINT (Output)"Print shows what happens when the format specification is used with display files.

The last two columns show what happens when the format specification is used with full screen processing, either for input (with the `INPUT FIELDS` statement) or for output (with the `PRINT FIELDS` statement). Note that the information marked for INPUT FIELDS applies to `RINPUT FIELDS` when RINPUT FIELDS is used for input. Likewise, the information marked for PRINT FIELDS applies to RINPUT FIELDS when RINPUT FIELDS is used for output.

If there is an X in any of the last five columns, the format specification operates according to its intended purpose when it is used as indicated. If there is an error code number in the column, the format specification cannot be used with this type of file (the specified error will occur if usage is attempted). 

The phrase "Treat as " means that the specification is accepted when used as indicated, but treated as if it were a different format specification.

{| border="1" style="border-collapse:collapse;"
! style="background:#a5c7ff;" colspan="5" rowspan="2"|Type
! style="background:#a5c7ff;" colspan="2" | Internal
! style="background:#a5c7ff;" | Display
! style="background:#a5c7ff;" colspan="2" |Full Screen
|-style="background:#a5c7ff;"
! Read/Reread
! Write/Rewrite
! Print
! Input Fields
! Print Fields
|-style="background:#a5c7ff;"
! Format
! Description
! S
! N
! I
! (Input)
! (Output)
! (Output)
! (Input)
! (Output)
|-style="background:#ddeaff;"
|`B`||Binary|| || ||X||X||X||Error 0816||Error 0816||Error 0816
|-
|`BL`||Binary Low|| || ||X||X||X||Error 0816||Error 0816||Error 0816
|-style="background:#ddeaff;"
|`BH`||Binary High|| || ||X||X||X||Error 0816||Error 0816||Error 0816
|-
|`C`||Character||X|| || ||X||X||X||X||X
|-style="background:#ddeaff;"
|`CC`||C Centered||X|| || ||Treat as C||X||X||Treat as C||X
|-
|`CR`||C Right Justified||X|| || ||Treat as C||X||X||Treat as C||X
|-style="background:#ddeaff;"
|`CL`||C Lowercase||X|| || ||Err 1006||Err 1006||Err 1006||X||Treat as C
|-
|`CU`||C Uppercase||X|| || ||Err 1006||Err 1006||Err 1006||X||Treat as C
|-style="background:#ddeaff;"
|`D`|| Double Precision Floating Point|| || ||X||X||X||Err 801||Err 0861||Err 0861
|-
|`DH`||Date Binary|| ||X|| ||X||X|| || ||
|-style="background:#ddeaff;"
|DL||Date Binary Low|| ||X|| ||X||X|| || ||
|-
|`DT`||Date Binary High|| ||X|| ||X||X|| || ||
|-style="background:#ddeaff;"
|`FMT`||Masked (Formatted) Input||X||X|| || || || ||X||X
|-
|`G`||Generic||X||X|| ||X||X||X||X||X
|-
|`GF`||G Floating Point||X||X|| ||X||X||X|| ||
|-style="background:#ddeaff;"
|`GL`||G Lowercase||X||X|| ||Err 1006||Err 1006||Err 1006||X||Treat as G
|-
|`GU`||G Uppercase||X||X|| ||Err 1006||Err 1006||Err 1006||X||Treat as G
|-style="background:#ddeaff;"
|`GZ`||G Zero Suppress||X||X|| ||Treat as G||X||X||Treat as G||X
|-
|L||Long Numeric|| || ||X||X||X||Err 0801||X||X
|-style="background:#ddeaff;"
|L||Leave Decimal|| ||X|| ||Err 1006||Err 1006||Err 1006||X||X
|-
|N||Numeric|| ||X|| ||X||X||X||X||X
|-style="background:#ddeaff;"
|`NZ`||N Display Zero|| ||X|| ||Treat as N||X||X||Treat as N||X
|-
|`Picture|P`||Picture|| || ||X|| || || ||X||X
|-style="background:#ddeaff;"
|`PD`||Packed Decimal|| || ||X||X||X||Err 0816||Err 0816||Err 0816
|-style="background:#ddeaff;"
|`PIC`||Masked (Pic Spec) Input||X||X|| ||X|| ||X||X||X
|-
|S||Single Precision Floating Point|| || ||X||X||X||X||X
|-style="background:#ddeaff;"
|V||String||X|| || ||X||X||X||X||X
|-
|`VL`||S Lowercase||X|| || ||Err 1006||Err 1006||Err 1006||X||Treat as V
|-style="background:#ddeaff;"
|`VU`||S Lowercase||X|| || ||Err 1006||Err 1006||Err 1006||X||Treat as V
|-
|`ZD`||Zoned Decimal|| || ||X||X||X||Err 0816||Err 0861||Err 0861
|-
|}

===See Also===
*Error `1006`
*Error `0816`
*Error `0862`
