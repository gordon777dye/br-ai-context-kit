---
title: DEBUG_PROFILE
file: DEBUG_PROFILE.md
source: https://brulescorp.com/brwiki2/index.php?title=DEBUG
category: 90-reference
subcategory: 90-reference/error-codes
kind: error-code
related: [Profiler File Layout]
---
= BR Profiler Main Page =

Use **PROFILER.EXE** to translate the BR Profiler output file into readable text.

== Generating profiler output ==

<pre>
DEBUG PROFILE SAMPLED filename
DEBUG PROFILE TIMED filename
DEBUG PROFILE STOP
</pre>

== Viewing profiler output ==
Use **profiler.exe** to view the contents of a log file:

<pre>
profiler.exe filename
profiler.exe filename raw
</pre>

== Additional resources ==

* See the FTP site: *Dll_Distr/Profiler* for samples and documentation.
* `Profiler File Layout` — Detailed description of the profiler log file format.
