# Filter

**Source:** https://brulescorp.com/brwiki2/index.php?title=Filter

---

Grid and list '''filter''' search fields are available as of BR! [[4.3]] for [[grids and lists]].

A new field type is defined (similar to [[SEARCH]]):

[[image:Filter.png|900px]]

 RINPUT FIELDS "nn,nn,15/FILTER 10,leading-attributes,row,col,grid column to search [, filter-type] [, CASE]": string-value

For example: 

 RINPUT FIELDS "4,50,15/FILTER 10,,10,10,2,ALL": Findfield$

This example combines a filter box (which will search everything in the list) and the rinput fields for a list selection:

 rinput fields "4,8,78/FILTER 30,/w:w,5,6,Fullrow,all;5,6,list 21/80,rowsub,selone": foundvar$,selection

===Parameters===

'''nn and nn''' are the row and column to position the field on the screen.

'''Size/''' and '''Characters''' signifies how large the filter field will be in columns, and how many characters can be entered into it. In the example, '''15/ and 10''' provide a 15 column field where the operator can enter 10 characters. 

'''Leading attributes''' can be any attributes desired (optional). 

'''Row and col''' are the starting row and column of the grid or list you wish to search.

'''Grid column to search''' is the number of the grid column the filter will test against. FULLROW can be used here to searchall the columns in each row. 

====Filter Types====
*LEADING - Filter searching is done left justified using only leading characters (default).
*WORD - Each word is leading matched.
*ALL - The entire string is searched for a match (similar to [[POS]]).


'''CASE''' may optionally be used to make all searching case sensitive. Case insensitivity is the default.

'''String-value''' is the variable name which will apply to whatever the operator enters into the field for searching. 

For both FILTER and [[Srch]], the up and down arrows now affect only the selection bar in the grid/list being presented.

====Note====

* MASK can be used to query the Filter display, with a value of 1.

====See Also====

* [[Filter_Delimiters]]

<noinclude>
[[Category:Widget]]
[[Category:Grid and List]]
</noinclude>

<!-- br_tree-audit -->
> **br_tree audit:** Folded into br_tree spec → [20-io-screen/fields-attributes/spec.md](<../br_tree/20-io-screen/fields-attributes/spec.md>).
