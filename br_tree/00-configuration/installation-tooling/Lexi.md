---
title: Lexi
file: Lexi.md
source: https://brulescorp.com/brwiki2/index.php?title=Lexi
category: 00-configuration
subcategory: 00-configuration/installation-tooling
kind: reference
related: [BR, third party editor, MyEdit, BR Programs, line numbers, brserial.dat]
---
**Lexi**, the **BR! Lexical Preprocessor** is a system for integrating `BR` with your favorite `third party editor`. Initially Lexi only supported only `MyEdit`, but it is also being used successfully with `Notepad++` and is very likely to work with any text editor that supports customizable user tools.

If you use Lexi, you can edit your `BR Programs` `#No Line Numbers|Without Line Numbers`. This frees you up to copy and paste code, rearrange code, and add and edit code without having to worry about or manually change any line numbers.  Lexi adds and changes and manages your `line numbers` for you automatically, when you "compile" your programs into .BR files.

But Lexi also does a lot more.  By preprocessing your `source code|code` before it is passed on to BR, Lexi gives you, the programmer, access to many useful features not normally found in BR.

Lexi also gives you access to the `#SELECT CASE|SELECT CASE` statement and the `#DEFINE` statement, common in other languages.

==Installation==
===MyEdit (BR Edition)===
Lexi can be used to automatically convert between BRS and BR files from within MyEdit. This can make your Editing life much easier. Lexi works with ALL versions of BR. However it requires a version of MyEdit dated `October 20`, `2006` or later.

The latest version of Lexi can be found at [http://www.sageax.com/downloads/Lexi.zip SageAX]

====Instructions====

To install Lexi, follow the following steps.

=====Automatic Installation=====

*The Automatic Installation process requires a version of MyEdit dated `March 5`, `2010` or later.

#) Unzip Lexi.zip into "C:\Lexi". You must use this directory in order for the automatic installation to work.
#) Copy your personal `brserial.dat` file into this directory (C:\Lexi).
#) Launch MyEdit.
#) Select Tools / Configure User Tools / Import Tools. Select the "Lexi.mut" file that came in Lexi.zip.

That's all there is to it.

=====Manual Installation=====

#) Unzip Lexi.zip into its own directory.
#) Copy your personal BRSerial.dat file into this directory.
#) Launch MyEdit.
#) Go to the Tools Menu, and then select "Configure User Tools".
#) Select "Add"
#) Enter the following information (Replace C:\Lexi\ with the appropriate folder), and Click OK to add the "Compile" tool.

  Menu Item Name: Compile BR Program
  Application/Command: C:\Lexi\ConvStoO.cmd
  Working Folder: C:\Lexi\
  Command Line Parameters: %%np_name %%npne_name "%%name" "%%folder"

There are six other Tools you can add to the MyEdit user tools menu that give you additional abilities for working with BR Source code. To add additional tools, repeat steps 5 and 6 above substituting information from the "Available Functions" table below.

That's all there is to it. Now, if you load a .BR file in MyEdit, you can select the "Extract Source" tool.
The file will be converted to a .BRS file and the new one will be loaded in MyEdit. If you
load a .BRS file, you can select the "Compile" tool, and the file will automatically be
"compiled" into a .BR file for you. Then simply load BR and test your new program.

This works with all versions of BR.

====Available Functions====

{| border=0
!Menu Item
!Application
!Parameters
|-
|Compile BR Program
|ConvStoO.cmd
|%%np_name %%npne_name "%%name" "%%folder"
|-
|Extract Source Code
|ConvOtoS.cmd
|%%np_name %%npne_name "%%name" "%%folder"
|-
|Debug BR Program*
|DebugBR.cmd
|%%np_name %%npne_name "%%name" "%%folder"
|-
|Extract Source Code and Strip Line Numbers
|ConvOSNL.cmd
|%%np_name %%npne_name "%%name" "%%folder"
|-
|Add Line Numbers
|AddLN.cmd
|%%np_name %%npne_name "%%name" "%%folder"
|-
|Strip Line Numbers
|StripLN.cmd
|%%np_name %%npne_name "%%name" "%%folder"
|-
|Run BR Program
|RunBR.cmd
|%%np_name %%npne_name "%%name" "%%folder"
|-
|}

* Debug BR Program requires that you have a copy of `brnative.exe` in the appropriate version sitting in your application folder. This may not be possible in all situations. Use Compile BR Program in situations where you cannot use Debug BR Program.

===Notepad++===
Users such as `User:Bowman` are currently using Lexi from within `Notepad++`.  However he has not yet been kind enough to share his setup process.  If you implement Lexi into your Notepad++ installation please add some instructions here.  If you can't figure it out I'd suggest contacting `User:Bowman` for assistance.

====Instructions====
These instructions assume Lexi 

=====Automatic Installation=====
Probably the easiest way to install Lexi tools into Notepad++ is to add the following lines to your shortcuts.xml (generally located in <nowiki>%appdata%\Roaming\Notepad++</nowiki>) file.

<nowiki>
<Command name="BR!s - Compile" Ctrl="yes" Alt="yes" Shift="yes" Key="73">C:\Lexi\ConvStoO.cmd &quot;$(FULL_CURRENT_PATH)&quot;</Command>
</nowiki>

<nowiki>
<Command name="BR!s - Stip line numbers" Ctrl="yes" Alt="yes" Shift="yes" Key="73">C:\Lexi\StripLN.cmd &quot;$(FULL_CURRENT_PATH)&quot;</Command>
</nowiki>

<nowiki>
<Command name="BR!s - Add line numbers" Ctrl="yes" Alt="yes" Shift="yes" Key="73">C:\Lexi\AddLN.cmd &quot;$(FULL_CURRENT_PATH)&quot;</Command>
</nowiki>

=====Manual Installation=====

Add three user controls by choosing Run>Run... (enter the first line) and click Save, then select the remaining two lines.  Do these steps for each of the Lexi utilities listed here.

 BRS - Line numbers - Remove
 C:\Lexi\StripLN.cmd "$(FULL_CURRENT_PATH)"
 Alt+8

 BRS - Line numbers - Add
 C:\Lexi\AddLN.cmd "$(FULL_CURRENT_PATH)"
 Alt+Shift+8

 BR!s - Compile
 C:\Lexi\ConvStoO.cmd "$(FULL_CURRENT_PATH)"

====Available Functions====
{| border=0
!Menu Item
!The Program To Run
|-
|BRS - Compile
|C:\Lexi\ConvStoO.cmd "$(FULL_CURRENT_PATH)"
|-
|BRS - Line numbers - Add
|C:\Lexi\AddLN.cmd "$(FULL_CURRENT_PATH)"
|-
|BRS - Line numbers - Remove
|C:\Lexi\StripLN.cmd "$(FULL_CURRENT_PATH)"
|-
|}

Potentially other functions could be made available but have not yet been enhanced to work with the single full path parameter.  The enhanced batch files (listed above) could serve as an example of how this is done - If you're feeling spunky.

* These installation instructions assumes the enhancement of 1 parameter passing (as opposed to 4) was included in your distribution.

===Sublime Text===

===All Third Party Editors===

====Tips====
*Inside the \Lexi\ folder you will find a copy of BR renamed to brnative.exe. It works better if this brnative.exe is the same version of BR that you are using in your programs. So copy your BR to this folder and replace brnative.exe with it.
*If you are having some trouble "Extracting Source" and you installed MyEdit to a custom location you will need to modify the file ConvOtoS.cmd to point to the proper location of MyEdit.exe. Load it in a text editor and you'll see what I mean.
*There is an additional tool called DebugBR.cmd. This only works if there is a working BR file called brnative.exe in the same folder as your program files. You add it to the list the same way as you did the other tools above.

== Function Reference ==

Lexi gives you access to a number of different abilities from other programs, designed to make your source code editing life easier. When you send a source file to BR using Lexi, Lexi preprocesses your source code, adding line numbers, and interpreting other "precompiler directives"

=== No Line Numbers ===

Working with No `Line Numbers` is easy, when you have Lexi to help.

You load your files using MyEdit, and you work with them as Source Code files. If you are editing a file in MyEdit that has line numbers in it, you can save the document and select the "Strip Line Numbers" user tool. This will launch BR, use it to strip out the line numbers, and reload your program in MyEdit. You make the changes you want while the line numbers are gone, and when you choose the "Compile" user tool or the "Add Line Numbers" user tool, the line numbers are added back to your program. If you choose the "Compile" tool, the line numbers are added, and your source code file is saved as a .BR file.

  43900  ! #Autonumber# 43900,10
  43910  DoesLayoutExist: ! Return true if layout exists in the layouts folder
  43920        def library FnDoesLayoutExist(layout$;LayoutPath$*255)
  43930           let Fnsettings(Layoutpath$) !:
                  fnDoesLayoutExist = exists(LayoutPath$&Filename$)
  43940        fnend

The above code gets turned into the following code when line numbers are stripped. When they are added back in, it gets turned back into the code above again.

  ! #Autonumber# 43900,10
  DoesLayoutExist: ! Return true if layout exists in the layouts folder
        def library FnDoesLayoutExist(layout$;LayoutPath$*255)
           let Fnsettings(Layoutpath$) !:
           fnDoesLayoutExist = exists(LayoutPath$&Filename$)
        fnend

=== AutoNumber ===

The #AutoNumber# precompiler directive directs the Line Number Add routine to use certian line numbers in your code.

Without the #AutoNumber# precompiler directive, Lexi adds line numbers starting with line number 00001 and counting by 1s.

  ! This Example Is Quite Simple:
     let Fnupdatefiledropdown ! We Run This No Matter What Happens. It Builds The Combo Box Dropdown List
  !
     if Trim$(_Post$(1))="" then ! If The User Did Not Select A File Layout From The List Then
        let Fnreadlayoutfolder ! Display The File Layout List In A Table
     else
        let Fnreadfileio(Trim$(_Post$(1))) ! But If They Did Select A File, Then Show It
     end if
     stop

becomes

  00001 ! This Example Is Quite Simple:
  00002    let Fnupdatefiledropdown ! We Run This No Matter What Happens. It Builds The Combo Box Dropdown List
  00003 !
  00004    if Trim$(_Post$(1))="" then ! If The User Did Not Select A File Layout From The List Then
  00005       let Fnreadlayoutfolder ! Display The File Layout List In A Table
  00006    else
  00007       let Fnreadfileio(Trim$(_Post$(1))) ! But If They Did Select A File, Then Show It
  00008    end if
  00009    stop

The idea is that you maintain your programs in source files, and so it doesn't matter what your line numbers are.

However, most BR Vendors do not maintain their programs as source files. They maintain them as .BR or .WB files, and the line numbers are important.

To use the #AutoNumber# precompiler directive, all you have to do is place simple comments in your code that say:

  ! #AutoNumber# LineNum,Increment

Then, when Lexi is adding line numbers, and it finds one of these lines, Lexi tries to set the line number of the current line to the line number you specified. Thereafter, until it reaches the next #AutoNumber# statement, it counts by the Increment you gave it.

In this way, its easy to give your functions each their own line number space, and still retain the ability to edit without having to worry about line numbers.

With the #AutoNumber# statement,

  ! #Autonumber# 16000,10
  DefineModes: ! Define the input spec modes
  def fnDefineInputModes
     dim InputAttributesMode
     dim InputFieldlistMode
     dim InputEditorMode
     dim InputEditorMoveMode
     dim InputDebugMode
  
     let InputAttributesMode=1
     let InputFieldlistMode=2
     let InputEditorMode=3
     let InputEditorMoveMode=4
     let InputDebugMode=5
  fnend

becomes

  16000 ! #Autonumber# 16000,10
  16010 DefineModes: ! Define the input spec modes
  16020 def fnDefineInputModes
  16030    dim InputAttributesMode
  16040    dim InputFieldlistMode
  16050    dim InputEditorMode
  16060    dim InputEditorMoveMode
  16070    dim InputDebugMode
  16080 !
  16090    let InputAttributesMode=1
  16100    let InputFieldlistMode=2
  16110    let InputEditorMode=3
  16120    let InputEditorMoveMode=4
  16130    let InputDebugMode=5
  16140 fnend

For this reason, when you are removing line numbers from your programs, it is sometimes a good idea to populate them with #AutoNumber# comments first, to preserve your original line number structure as much as possible.

If the line numbers program detects that your #AutoNumber# comments are not in numerical order, or if there is not enough numbers between them to accomodate all your lines, it will generate an error and stop processing your program. At that time you should type clear, and then system to return to your editor, and fix the #AutoNumber# statements there. After you fix the problem, Save your source code again, and compile.

=== DEFINE ===

The #DEFINE# Precompiler Directive will tell The Line Number generation system that you have made a constant.

  !. "#Define# <nowiki>`ScreenControls`</nowiki> = "mat ControlName$, mat FieldName$, mat Description$, mat VPosition, mat HPosition, mat FieldType$"

The above example will set up a precompiler Constant called <nowiki>`ScreenControls`</nowiki>. Now, everywhere in your program that you use the text <nowiki>`ScreenControls`</nowiki> will be replaced by "mat ControlName$, mat FieldName$, mat Description$, mat VPosition, mat HPosition, mat FieldType$".

The "." will force BR to not change the capitalization of your comments.

   ! #AutoNumber# 14000,10
   EditScreen: ! Main Screen Designer
   def fnEditScreen(fScreenIO, fScreenFld, ScreenName$, mat ScreenIO$, mat ScreenIO,<nowiki>`ScreenControls`</nowiki>)

This function definition changes to contain the full list of arrays that are responsible for Screen Control information in the ScreenIO library, each time the program is compiled.

When the source code is pulled back out and the line numbers are stripped, the substitute statements revert back to their original values.

=== SELECT CASE ===

We have implemented SELECT CASE as a precompiler directive. This means, when editing your programs with no line numbers, you can write SELECT CASE (SWITCH in C/C++) statements using the following syntax, and it will automatically be turned into IF THEN ELSEIF statements when it gets to BR.

  ! #Autonumber# 16000,10
  PreformInput: ! Preform main input operation
  def fnPreformInput(&Mode,Control,mat ScreenIO$,mat ScreenIO;___,Window)
     #SELECT# Mode #CASE# InputAttributesMode
        let Window=fnGetAttributesWindow
        let fnGetAttributeSpec(mat InputSpec$,mat InputData$,mat InputSubs)
        rinput #Window, fields mat InputSpec$ : mat InputData$
  
     #CASE# InputFieldlistMode
        let Window=fnGetFieldsWindow
        let fnGetFieldsSpec(InputSpec$)
        rinput #Window, fields InputSpec$ : InputData
  
     #CASE# InputDebugMode
        let Window=fnGetDebugWindow
        let fnGetFieldsSpec(InputSpec$)
        rinput #Window, fields InputSpec$ : InputData
  
     #End Select#
  fnend

Gets translated into this:

  16000  ! #Autonumber# 16000,10
  16010  PreformInput: ! Preform main input operation
  16020  def fnPreformInput(&Mode,Control,mat ScreenIO$,mat ScreenIO;___,Window)
  16030     IF  Mode  =  InputAttributesMode THEN  ! #SELECT# Mode #CASE# InputAttributesMode
  16040        let Window=fnGetAttributesWindow
  16050        let fnGetAttributeSpec(mat InputSpec$,mat InputData$,mat InputSubs)
  16060        rinput #Window, fields mat InputSpec$ : mat InputData$
  16070  !
  16080     ELSE IF  Mode  =  InputFieldlistMode THEN  ! #CASE# InputFieldlistMode
  16090        let Window=fnGetFieldsWindow
  16100        let fnGetFieldsSpec(InputSpec$)
  16110        rinput #Window, fields InputSpec$ : InputData
  16120  !
  16130     ELSE IF  Mode  =  InputDebugMode THEN  ! #CASE# InputDebugMode
  16140        let Window=fnGetDebugWindow
  16150        let fnGetFieldsSpec(InputSpec$)
  16160        rinput #Window, fields InputSpec$ : InputData
  16170  !
  16180     END IF  ! #End Select#
  16190  fnend

You may notice the comments that appear at the end of your IF THEN statements. The comments are created automatically by the "Add Line Numbers" routine when it translates the SELECT CASE statement into IF THEN ELSEIF statements. The purpose of the comments is so that the "Strip Line Numbers" routine can change them back into a SELECT CASE statement so that your code appears correct on the editor/line-number-free side.

=== Spacing ===

As you can see from the above examples, any blank spaces you insert into your programs are turned automatically into blank comment lines. This is to preserve the spacing and look and feel of your program on the editor/line-number-free side.

== Considerations ==

=== L##### labels ===
Because Lexi strips the line numbers before you edit your document, it would easily cause a problem if you had any hard coded line number references, because your line numbers change all the time and those references aren't automatically updated. Therefore, before it strips line numbers from any BR program, Lexi loads the program in BR and executes the `RENUM` LABELS_ONLY command. This command replaces all your hard coded goto references with labels that are L##### where ##### is the line number.

That way you are free to edit your document without worrying about the line numbers, and later, when you add in new line numbers, your program still works.

If you have accidentally placed L##### labels in your code and you need them removed, contact `mailto:gabriel.bakker@gmail.com Gabriel`.  He has written a program to remove them.

The L##### labels do not harm your code - it will work exactly as before. However, I understand sometimes it can be confusing if something like this happens to your code and there is a tool to change them back.

One other note about L##### labels: If the "Add Line Numbers" routine detects any of these labels in your code, it will use them as clues as to what your original line numbers were, and it will match the new line numbers as closely as possible to the old one. This is done for your comfort as you edit your programs, just in case you still edit them in BR and use the line numbers. I wanted your programs to remain as unchanged by the linkage as possible.

=== Save Source Code ===
It is of vital importance that you save your source code before executing any of the user tools. If you fail to save your source code before using a user tool, the tool will operate on the old version of the file that it finds on the disk, and when the conversion is complete and the new file is reloaded in MyEdit, all your changes will be lost. You can't undo it because MyEdit thinks you have loaded a whole new file.

Please be careful when using this.

=== PROC NOECHO ===
For anyone who has used Lexi in the past, it used to scroll through the contents of your program as it was adding or removing line numbers, due to the process of converting your source file into a compiled BR program. Depending on the size of the program and the speed of your system, this process may have taken a long time.

The latest version of Lexi has been updated with PROC NOECHO to disable this printout and greatly improve the speed of compiling your programs. As a result of PROC NOECHO, if there are any compile time errors in your code, you will not be able to see the line that caused the problem, until you press F2. Just remember, if you run into a problem compiling your screen, press F2 to see the offending line.

==Disclaimer==

`User:Gabriel|Gabriel Bakker` and `Sage AX` are not responsible for anything that happens to your BR programs or data as a result of using this or any other tool we create.
