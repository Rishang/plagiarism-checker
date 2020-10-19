# A python snippet script based on selenium to check plagiarism

it contains Two functions 
1. googleSearch() to perform google search
2. compareStr() to compare two strings

**Use case:**
`googleSearch("hello")`

It works by searching on google the string we gave in argument and collect following items of each result.
*  link Title
* description
* link
* domain name

This items of each search result are returned if form of dictionary.

`compareStr("hello world","hello you")`
output: `70.0`

This function returns percentage of match between 2 strings given in arguments.