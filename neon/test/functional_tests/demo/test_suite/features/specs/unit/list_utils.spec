# List Utilities
============================

## Find partial text inside a list
-----------------------------------
tags: ListUtils.contains_partial_text

   |text     |list     |matched|
   |---------|---------|-------|
   |search   |search,me|True   |
   |search_me|search,me|False  |

* Search all <list> items matching the <text>
* Got the list <matched>

## Is any item on list is present in the text
-----------------------------------
tags: ListUtils.is_any_present

   |list     |text     |matched|
   |---------|---------|-------|
   |search,me|search   |True   |
   |search,me|serach_m|False  |

* Search any <list> items matching in <text>
* Got the result <matched>

## Is all item on list is present in the text
-----------------------------------
tags: ListUtils.is_all_present

   |list     |text     |matched|
   |---------|---------|-------|
   |search,me|search   |False  |
   |search,me|search_me|True   |

* Search all <list> items matching in <text>
* Got the result <matched>
