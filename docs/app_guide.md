## Requirements
- Integrate user inputs and make it work with main.py

Details about this:
I need you to make the user inputs be connected to main.
Below you can find user inputs we need in webapp.
Can have a modern looking frontend for the webapp called Fetch Fund in its own folder that you need to create. It can be made to follow the colour scheme in fetch_fund_logo.png.
On the webapp, the only functionality needed is: 
- Take the below mentioned inputs from the user 
- An approptiately named button to submit the inputs from user
- The submit button passes the inputs to the main agent (main agent in turn depends on different agents)
- Main.py will run correctly and do it's job, this will take some time. 
- Output on the webapp the final decision from the main agent: hold/sell/buy etc. (You need to figure out how to do this correctly, this might need you to parse some information, think about how you would do this)

## User inputs:
Topup wallet ( You would need at least 6 FET to run this application?) - str - [yes/no]

Amount to top up with - float-

EVM private key - str -

network - str - (bitcoin/ethereum/base/polygon)

investor type - str - (long-term/short-term/speculative)

risk strategy - str - (conservative/balanced/aggressive/speculative)

Any particular reason why you would like to perform Buy/Sell/Hold action? - str -


Currently these values might be hardcoded in the main.py code. 
Examples of lines where information has been hardcoded in main.py:
- Line 277 Network = "base"
- Line 34 METAMASK_PRIVATE_KEY
- Line 343 investor = "speculate"
- Line 357 USERREASON = "..."


Useful information:
- On line 485: the msg.message outputs the status of swap transaction usdcTOeth or ethTOusdc, you can use it as a success message for output.

- Around Line 389: you can use msg.decision to output reasoning of asi1 prompt. there will be few, since it iterates over multiple prompting requests.