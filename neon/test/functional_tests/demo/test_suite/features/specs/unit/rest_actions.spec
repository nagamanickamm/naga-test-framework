# Rest Actions
========================

## Upload Image files
-----------------------
tags: sanity

* Upload Image file "input.jpg"
* Upload should be successful

## Download Image files
-----------------------
tags: sanity

   |inputfile|outputfile |result|
   |---------|-----------|------|
   |input.jpg|output.jpg |true  |
   |input.jpg|output2.jpg|false |

* Download Image <inputfile>
* Compare image <inputfile> with <outputfile> and expect <result>

