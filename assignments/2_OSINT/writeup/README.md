# Writeup 2 - OSINT

Name: Daniel Kelly
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examniation.

Digital acknowledgement: Daniel Kelly

## Assignment Writeup

### Part 1 (45 pts)


#### 1.
Using `https://usersearch.org/`, I found a Twitter account with the username `v0idcache`. The account belongs to Elizabeth Moffet, the CEO of 13/37th National Bank.



#### 2.
She works at 13/37th National Bank, who's url is `1337bank.money`.



#### 3.
As stated before, I found a twitter account associated with the `v0idcache` username using `https://usersearch.org/`. Looking through her twitter page, we find that she is located in the Netherlands.

Many websites format the urls of a user's page by directly embedding the username in the url. As such, one can often find a user by simply inserting the username in the proper place in the url. Doing this, I was able to determine that she also has a github account.

Searching Google for `v0idcache` returns three hits. The first is a reddit post, showing that she has a reddit account. Her reddit account public info reveals that `v0idcache`'s birthday is `Feb. 21, 2019`.

The second is a link to the webpage, `1337bank.money`, for the bank at which `v0idcache` works. This also includes her email, `v0idcache@protonmail.com.`

The last page is a pastebin file showing a chatroom conversation between `v0idcache` and `fl1nch`. This outlines some sort of meeting or transaction between the two which was scheduled tto occur at 1400. The conversation also seems to indicate the transfer of a file, `AB4300.txt`, from `v0idcache` to `fl1nch`, who seems to be acting on behalf of another group of people.



#### 4.
Executing `ping 1337bank.money` reveals that one ip address associated with the website is `142.93.136.81`. Using this ip on `censys.io` reveals that the server is located in North Holland, Amsterdam, Metherlands. Using `securitytrails.com` we see that the hosting provider is DigitalOcean, LLC.



#### 5.
By reading the page's robot.txt page at `1337bank.money/robots.txt`, we find the secret page `1337bank.money/secret_directory`, containing the flag `CMSC389R-{h1ding_fil3s_in_r0bots_L0L}`. By viewing the page source for the homepage, `1337bank.money`, we find the flag `CMSC389R-{h1dd3n_1n_plain_5ight}`.



#### 6.
There are three open ports on this website: `ssh` is running on `port 22`, `http` is on `port 80`, and waste is on `port 1337`. This was discovered using nmap on the previously discovered ip address.



#### 7.
Using the website `cencys.io` with the discovered ip, the os was determined to be Ubuntu.



#### 8.
The reddit post mentioned previously contains a flag, `CMSC389R-{0M3G4LUL_G3T_pWN3d_N00b}`. Also, `dnsdumpster.com` revealed an additional flag of `CMSC389R-{h0w_2_iNt0_DNS_r3c0Rd5}`.



### Part 2 (75 pts)

A list of the million most commonly used passwords was found at `https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt`.

The basic approach is read the password file line by line. For each line, write out the test username and password, then read the response. If the response is 'Fail', which is the usual response, then continue. Otherwise, print the successful password and exit. This on its own is fairly slow, but using the Poll library in python, it can be sped up dramatically, able to test over 40 passwords per second. A shared variable is used to terminate the program once a password has been found.

After logging in and inspecting the `/home` directory, we find the `flag.txt` file, whose contents are `CMSC389R-{brut3_f0rce_m4ster}`.

There is also the interesting file `AB4300.txt` referenced in the pastebin chatroom file. I don't know whether or not it's relevant, but using the command `find . -type f | grep 'AB4300.txt`, this file is quickly located under `/home/files/AB4300.txt`. Its contents are `CMSC389R-{YWX4H3d3Bz6dx9lG32Odv0JZh}`.
