# Web Writeup

Name: Daniel Kelly
Section: 0101

I pledge on my honor that I have not given or received any unauthorized
assistance on this assignment or examination.

Digital acknowledgement: Daniel Kelly

## Assignment Writeup

### Part 1 (40 Pts)

Upon inspecting the website provided, I noticed that the URLs for each item page take the form `http://1337bank.money:5000/item?id=N` for some number N.
The `?id=N` part of the string is a query string used to retrieve the data for each specific item.
I first attempted an XSS attack with the URL `http://1337bank.money:5000/item?id=<script>alert('hi');</script>`, but it had no effect.

After rereading the assignment, I decided to try a SQL injection attack instead, suspecting that the number passed as the query argument might be used in a SQL statement to retrieve the item data.
Initially, I tried `http://1337bank.money:5000/item?id=0' or 1=1;--`, but this tripped a SQL injection detector.
After some testing, I determined that it was the keyword `or` that was causing problems, so I replaced it with the double pipe or, `||`, yielding `http://1337bank.money:5000/item?id=0' || 1=1;--`.

Having done this, I recieved an Internal Server Error, which was determined with TA guidance to be the result of premature termination of the statement due to the semicolon.
With this removed, my URL became `http://1337bank.money:5000/item?id=0' || 1=1--`.

I continued to recieve errors, however, and I eventually discovered that MySQL requires at least one character of whitespace after the double dash for a comment.
I added a space to the end of the URL, but this was stripped before being passed on.
To prevent this, another non-whitespace character must be added.

My final URL for the SQL injection attack was `http://1337bank.money:5000/item?id=0' || 1=1-- -`.
This revealed the hidden flag, `CMSC389R-{y0u_ar3_th3_SQ1_ninj@}`.

### Part 2 (60 Pts)

For the first level of the XSS game, I entered the query `<script>alert('hello');</script>`, which caused an alert popup to appear.

In the second level, the `<script>` tag does not work.
Instead, the code is embedded in an image element as `<img src="" onerror="alert('XSS');">`, which is entered as the body of the post.

The third level is solved similarly.
The URL contains a query, which follows the `#` symbol.
In typical usage, this is a number which is inserted inro a string representing an image path.
For my attack, I instead use the string `1.jpg'><img src="" onerror='alert("hi");'><!--`.
The first part, `1.jpg'>`, terminates the original image element, while the second part, `<img src="" onerror='alert("hi");'>`, is the injection itself.
The final part makes the remainder of the string a comment, which resolves the trailing `.jpg' />`.
This is particularly nice in that it makes the injection more covert, since the page renders the same as if `1` were passed as the query.

For the fourth level, the contents of the `timer` variable are directly inserted into a javascript string as the argument of the startTimer function.
As such, I am easily able to inject an additional statement with the entry `1'); alert('hi`.
The single quote, parenthesis, and semicolon close off the startTimer function call.

The fifth level leverages the javascript resource identifier scheme, which allows one to embed javascript code where a resource identifier would be expected.
Thus, by setting the value of the `next` argument in the URL query to `javascript:alert('hi');`, I was able to inject javascript into the page.

In the sixth level, I used the recommended api from Google, `google.com/jsapi?callback=foo`.
The value of the callback argument is the callback that is executed at the end of the script, so by replacing foo with alert, the script will end with `alert();`.
The "sanitation" only checks for instances of http or https in lowercase letters specifically, so by using the uppercase instead, I was able to bypass it.
Thus the correct value for the argument is `HTTPS://google.com/jsapi?callback=alert`.
