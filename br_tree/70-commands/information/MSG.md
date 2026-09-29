---
title: MSG
file: MSG.md
category: 70-commands
subcategory: 70-commands/information
kind: command
related: [string, internal function, Msg$, 0412, 0413, 0414, 0415, 0416, 0417, 0418]
corrections:
  - "MSG(\"sleeptime\",n) takes milliseconds, not centiseconds (line 14) or seconds (the closing paragraph); the two statements also contradicted each other. BR 4.4 brmsg.cpp BrMsg_SleeptimeObjCmd stores `sleeptime = (*num) * 1000` and hands it to wb_sleepex, which sleeps in microseconds (common.cpp); the default is `static DWORD sleeptime = 200000` µs = 0.2 s, i.e. 200. Confirmed empirically: a pacing test written to the documented 100 = 1 second ran ten times fast. Reported in context/ERRORS.md 2026-09-28."
  - "Special-character table listed F14 between F9 and F11; the key table in brmsg.cpp defines |F1| through |F12| only, so the row is F10 (there is no F13 or F14)."
  - "Special-character table completed from brmsg.cpp's SpecialChar[] table, which has 20 names the page omitted: CLR, SPACE, SEL, PRINT, EXEC, SNAP, LWIN, RWIN, APPS, NUM#, and the ALTL/ALTR, CTRLL/CTRLR and SHIFTL/SHIFTR press/release pairs. Each description is the entry's Windows VK_ code. The L variants are byte-for-byte the same event as the plain modifier; the R variants add KEYEVENTF_EXTENDEDKEY. NUM, was described as the key pad comma; it sends VK_SEPARATOR."
---
MSG("<KB>",<`string`>) ! send string to keyboard

The **MSG** `internal function` (without the dollar sign) is only available for Windows & CS versions.  This should not be confused with `Msg$`.
For example:

 MSG("sleeptime",milliseconds) ! specify MSG keystroke time interval (1000 = 1 Second)

With the Msg internal function you can directly control the keyboard under the Windows client from within a BR program by issuing a function call to MSG.

Msg is useful for redisplaying Windows menus upon returning to a menu program from an application program. MSG has no effect on Unix or Linux **terminal** sessions, but works under Client / Server with Unix the same as WINDOWS.

The first parameter ("KB" or "kb") is case insensitive.

Two new Error Codes are defined in support of this function:

*`0412` Invalid Action Code - The first parameter is not recognized.
*`0413` Window Not On Top - A KB message was sent to a task which is different from the one that currently owns the keyboard.

**Note** that the following error codes may be related to this function:

*`0414` Wrong number of arguments passed
*`0415` Some error that has err message
*`0416` Not enough elements in dimensioned array
*`0417` Dimensioned string length is not big enough
*`0418` Unknown
*`0419` Error in special char spec

====Special Keystroke Values====

This facility operates through the operating system, so it does not utilize BR scancodes. If you need to send a special character (which in turn may cause BR to generate its scancodes), you will need to emulate the corresponding keyboard activity. Special characters need to be enclosed in pipes **|**.

=====Examples=====

If you want to send ctrl+c, you must send the following string:

 00010 MSG("KB","|CTRL+|c|CTRL-|")

This says that you want depress the "CTRL" key, type "c", and then release "CTRL".

Example:

 MSG("KB","|CTRL+|p|CTRL-|")

Will input the CTRL-P character, which causes BR to perform a printscreen operation.

=====Special Character List=====

**Each char must be enclosed in pipes**

{|
|-valign="top"
|**ALT+ ||width="75%"| press ALT - see note below
|-valign="top"
|**ALT- || release ALT
|-valign="top"|**
|-valign="top"
|**CTRL+ || press CTRL
|-valign="top"
|**CTRL- || release CTRL
|-valign="top"
|**
|-valign="top"
|**SHIFT+ || press SHIFT
|-valign="top"
|**SHIFT- || release SHIFT
|-valign="top"
|**
|-valign="top"
|**ALTL+ ALTL- || press / release ALT — the same key event as ALT+ / ALT-
|-valign="top"
|**ALTR+ ALTR- || press / release ALT with the Windows extended-key flag set
|-valign="top"
|**CTRLL+ CTRLL- || press / release CTRL — the same key event as CTRL+ / CTRL-
|-valign="top"
|**CTRLR+ CTRLR- || press / release CTRL with the Windows extended-key flag set
|-valign="top"
|**SHIFTL+ SHIFTL- || press / release SHIFT — the same key event as SHIFT+ / SHIFT-
|-valign="top"
|**SHIFTR+ SHIFTR- || press / release SHIFT with the Windows extended-key flag set
|-valign="top"
|**
|-valign="top"
|**TAB || press the tabulation key
|-valign="top"
|**RET || press the return key
|-valign="top"
|**ESC || press the escape key
|-valign="top"
|**SPACE || press the space bar
|-valign="top"
|**CLR || press the Clear key (VK_CLEAR)
|-valign="top"
|**
|-valign="top"
|**BACK || press the backward key
|-valign="top"
|**DEL || press the delete key
|-valign="top"
|**INS || press the insert key
|-valign="top"
|**HELP || press the help key
|-valign="top"
|**
|-valign="top"
|**LEFT || send the cursor to the left (left arrow)
|-valign="top"
|**RIGHT || send the cursor to the right (right arrow)
|-valign="top"
|**UP || send the cursor up (up arrow)
|-valign="top"
|**DOWN || send the cursor down (down arrow)
|-valign="top"
|**
|-valign="top"
|**PGUP || press the page up key
|-valign="top"
|**PGDN || press the page down key
|-valign="top"
|**HOME || press the home key
|-valign="top"
|**END || press the end key
|-valign="top"
|**
|-valign="top"
|**SNAP || press the Print Screen key (VK_SNAPSHOT)
|-valign="top"
|**PRINT || press the Print key (VK_PRINT — not Print Screen)
|-valign="top"
|**SEL || press the Select key (VK_SELECT)
|-valign="top"
|**EXEC || press the Execute key (VK_EXECUTE)
|-valign="top"
|**LWIN || press the left Windows key
|-valign="top"
|**RWIN || press the right Windows key
|-valign="top"
|**APPS || press the Applications (context menu) key
|-valign="top"
|**
|-valign="top"
|**F1 || press the function key F1
|-valign="top"
|**F2 || press the function key F2
|-valign="top"
|**F3 || press the function key F3
|-valign="top"
|**F4 || press the function key F4
|-valign="top"
|**F5 || press the function key F5
|-valign="top"
|**F6 || press the function key F6
|-valign="top"
|**F7 || press the function key F7
|-valign="top"
|**F8 || press the function key F8
|-valign="top"
|**F9 || press the function key F9
|-valign="top"
|**F10 || press the function key F10
|-valign="top"
|**F11 || press the function key F11
|-valign="top"
|**F12 || press the function key F12
|-valign="top"
|**
|-valign="top"
|**NUM0 || press the 0 on the key pad
|-valign="top"
|**NUM1 || press the 1 on the key pad
|-valign="top"
|**NUM2 || press the 2 on the key pad
|-valign="top"
|**NUM3 || press the 3 on the key pad
|-valign="top"
|**NUM4 || press the 4 on the key pad
|-valign="top"
|**NUM5 || press the 5 on the key pad
|-valign="top"
|**NUM6 || press the 6 on the key pad
|-valign="top"
|**NUM7 || press the 7 on the key pad
|-valign="top"
|**NUM8 || press the 8 on the key pad
|-valign="top"
|**NUM9 || press the 9 on the key pad
|-valign="top"
|**
|-valign="top"
|**NUM* || press the * on the key pad
|-valign="top"
|**NUM+ || press the + on the key pad
|-valign="top"
|**NUM- || press the - on the key pad
|-valign="top"
|**NUM, || press the key pad separator key (VK_SEPARATOR)
|-valign="top"
|**NUM# || press the key pad decimal point (VK_DECIMAL)
|-valign="top"
|**NUM/ || press the / on the key pad
|-valign="top"
|**
|-valign="top"
|}
To send the pipe character specify <nowiki>|||</nowiki>.

MSG("sleeptime",milliseconds) specifies the number of milliseconds to wait before issuing each string and each control character (`1000` = one second). The default is 200 (0.2 seconds).

Please note that the ALT key needs to be depressed and released (ALT+ and ALT-) for every Alt-character specified.

 |alt+|m|alt-||alt+|b|alt-| works
 
 |alt+|mb|alt-| fails
 
 |alt+|m|down||alt-| works
 
This is because keyboard entries don't interpret more than one keystroke as an alt value except when using the numeric keypad. However Windows will honor arrow keys while the alt key is held down.
