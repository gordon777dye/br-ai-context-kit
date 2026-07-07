---
title: NXTFLD
file: NXTFLD.md
source: https://brulescorp.com/brwiki2/index.php?title=Nxtfld
category: 10-language
subcategory: 10-language/data-manipulation/system-functions
kind: function
related: [internal function, Curfld, FKEY, cursor, INPUT FIELDS, RINPUT FIELDS, INPUT SELECT, RINPUT SELECT, attribute, Array]
---
The **NxtFld** `internal function` is similar to `Curfld` except that it  returns the relative position of the next control to be occupied during an INPUT operation (the one the user clicked on or attempted to move to). 

Two methods are used to identify clicked controls: Fkey numbers and NXTFLD. This will keep track of which control was clicked when a user clicks on a hot control (a control that has an Fkey assigned). If the control is a GRID or LIST then it keeps track of where the user clicked within the control. 

If a control that is part of an active Input Fields operation is double clicked, then NXTFLD will identify the relative position of the control within the Fields operation. However, for hot field identification it is necessary to use Fkey values to identify the respective controls. 

===Interrogating the Next Control===

It is desirable to know which control was clicked when a user clicks on a hot control (a control that has an Fkey assigned). Furthermore, if the control is a GRID or LIST then it can be useful to know where the user clicked within the control. Two methods are used to identify clicked controls: Fkey numbers and NXTFLD. 

The **NxtFld** `internal function`  has 4 possible combinations of syntax:

 NXTFLD
  
 NXTFLD([<New_current_field>] [,<attribute$>] [,`FKEY`])
 
 NXTFLD([<New_current_field>] [,<New_current_row>]) ! if the new current field is a ListView
 
 NXTFLD([<New_current_field>] [,<New_current_cell>])! if the new current field is a Grid

When used without parameters, the **NxtFld** function returns the number of the field containing the `cursor` from the last `INPUT FIELDS`, `RINPUT FIELDS`, `INPUT SELECT`, or `RINPUT SELECT` operation. With parameters, NxtFld can be used to record the field (same as the C control `attribute`) and/or an attribute for the last field. 

===Comments and Examples===

 00100 DIM SF$(3)
 00110 LET SF$(1)="10,30,c 10,r"
 00120 LET SF$(2)="12,30,c 10,r"
 00130 LET SF$(3)="14,30,c 10,r"
 00140 INPUT FIELDS MAT SF$: A$, B$, C$
 00150 PRINT "Cursor ended on FIELD"; NXTFLD
 00160 PRINT "Cursor ended on ROW"; NXTROW
 00170 PRINT "Cursor ended on COLUMN"; NXTCOL

In the sample program above, the there are three fields available for input. The operator can move the cursor in any direction, but only within these three fields. After the operator hits the <ENTER> key, line 150 will print the number 1, 2 or 3 depending on which field the operator left the cursor on. In addition, line 160 will print the row number (10, 12, or 14) containing the cursor when input was ended. Also, line 130 will print the column number (30 through 39).

NXTFLD provides valuable information when several fields are entered in one statement through an array, specifically, when `INPUT FIELDS`, `RINPUT FIELDS`, `INPUT SELECT`, or `RINPUT SELECT` is used with an `Array`.

As NXTFLD returns the subscript in the field definition array of the field containing the cursor from the last `INPUT FIELDS`, `RINPUT FIELDS`, `INPUT SELECT`, or `RINPUT SELECT`, NXTFLD can be especially useful with the on-line help facility. By using NXTFLD in the HELP$ function in line 990 for the value of the "mark", the operator can be directed to the most relevant portion of the text under the topic HOURS.ENTRY in the help file that explains the valid entries for that field. For example:

 00810 INPUT FIELDS MAT FLD$: HRS,OT,DT,SICK HELP 90
 00820 STOP
 00990 HELP$("HOURS.ENTRY", NXTFLD) : RETRY

===FKEY Parameter===

NxtFld has been extended to allow an additional numeric parameter, an `FKey` value, that causes FIELDS and SELECT statements to execute the specified keystroke before requesting operator input. NXTFLD ignores FKEY values of 100 or less and of 114 or greater. The following code uses NXTFLD and FKEY to trap the operator's field exit keystroke and execute it after verifying the data just entered. NOTE that the AE control attributes are used to interrupt execution of the INPUT FIELDS statement upon field exit.

 00010 PRINT NEWPAGE
 00020 INPUT FIELDS "10,10,C 10,AEU:R;11,10,C10,U": X$,Y$ HELP 41
 00030 IF CURFLD=1 THEN PRINT FIELDS "10,22,C": X$
 00040 IF FKEY>100 THEN LET NXTFLD(NXTFLD,FKEY) : GOTO 20
 00041 PRINT FKEY
 00050 STOP

As soon as the operator attempts to exit the first input field, line 30 verifies the entered data by redisplaying it to the right of the field. The CURFLD function in line 40 is then used to reenact the operator's field exit operation: the field just verified is set to the current field, and the operator's attempted exit keystroke (the value of FKEY) is executed. Operator input is then allowed for the next field.

NOTE: If the up arrow was the last key used, the cursor will return to the previous field. If the tab key was used, the cursor will position to the next field with a T (tab stop) attribute.

NOTE that the NXTFLD function in line 40 is executed only if the value of FKEY is greater than 100. Values of 100 or less are ignored, as are interpreted as an attempt to enter the entire screen.

NXTFLD processes field control attributes such as AEP and #. These control attributes are ADDED to the control attributes that are specified for a field. Also, the attributes that are specified with NXTFLD will OVERRIDE (be used instead of) a floating attribute specified with ATTR. The NXTFLD attributes will remain in effect only during the next execution of an INPUT FIELDS or INPUT SELECT statement. Line 20 in the following example uses the X control attribute (see the "X control attribute" discussion in the `BRConfig.sys` Specifications section for more information).

 00010 INPUT FIELDS "10,10,V 10,U;11,10,V 10,U;12,10,V 10,U",attr "HU":X$,Y$,Z$
 00020 IF X$="" THEN LET NXTFLD(1,"RX") : GOTO 10
 00030 !.. other editing
 00040 IF FKEY>100 THEN LET NXTFLD(NXTFLD,FKEY) : GOTO 10
 00050 !.. output

If the first field displayed by the above code is left blank, the NXTFLD function in line 20 will reposition the cursor to that field and display it in reverse video. The NXTFLD function's X attribute will additionally cause an auto-enter to occur when the operator attempts to re-exit the field. If the field passes the test on line 20, and the enter key or a function key was not pressed, the field attribute will resume as an underline and the cursor will be positioned at the next field the operator was trying to move to.

`ADS` expects that line 40 will become a standard line of code in all programs that use input fields and validate data.

Previously, the NxtFld statement supported 3 parameters:

#  The relative field number.
#  Optional additional field attributes.
#  An optional `FKEY` value to be applied for cursor positioning before processing the INPUT.

In the event the first parameter points to a `2D field/control` then instead of the FKEY value, the third (or second numeric) parameter is interpreted as the subscript of the item within the 2D control.  For LISTs, this is a row value. For GRIDs this is a Cell Subscript Value. For TOOLBARs, it is the icon subscript value (relative position in toolbar).  

Also, in the event the first parameter points to a 2D field/control then the NXTFLD function returns the subscript of the current item within the 2D control.

The NXTFLD system function has been extended to support the current selection upon entry to a multi-field control. The first parameter specifies which field/control is to be affected and the second parameter is the subscript of the cursor upon entry to that control. In the event the first parameter points to a 2D field/control then instead of the FKEY value, the third (or second numeric) parameter is interpreted as the subscript of the item within the 2D control.
*For LISTviews this is a row value.
*For GRIDs this is a Cell Subscript Value.
*For TOOLBARs it is the icon subscript value (relative position in toolbar).

Note that NXTFLD with 2 parameters does not set the initial position of the cursor until the respective control is entered. Also if the mouse is used to enter a control, that will override the specified NXTFLD value.

`Option` 43 Use old style Input Select with respect to setting CURFLD to the `NXTFLD` value when a selection is made.
