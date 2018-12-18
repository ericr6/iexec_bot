# iexec_bot

The program manages task submission in iExec marketplace
It allows to submit many tasks, you can easily submit and monitor hundreds of tasks 
This wrapper is written in python to allowed future prototype for more advanced usage, 
as brokering computing resources.
     
Requirements: 
- python 3 
- iexec SDK: go to https://github.com/iExecBlockchainComputing/iexec-sdk,
- Alls version 2.x should be supported, tested on 2.2.31 
- Tested and valideted on Ethereum kovan testnet


# Installation and test

1. Install iExec SDK:

Make sure iExec SDK is installed and ready to use .
you should have prepared your wallet, your account and be sure to get enough RLC and ether to 
Go to docs.iex.ec for more details.

2. Set up your app:

Define the price, the name of your dapp and the name of your image from docker hub.
The app deployed for the tutorial is a zcash minning software but it can be any applications. 
You can use your own docker image from dockerhub, built with the few iExec requirements.   

  
Edit **iexec.json** to define the work   
{
  "app": {
    "name": "zcash_nicehash",
    "price": 2,
    "params": {
      "type": "DOCKER",
      "envvars": "XWDOCKERIMAGE=ericro/equinicehash"
    }
  }
} 
 
Deploy your decentralized application. 
```
iexec app deploy
```     
```
ℹ using chain [kovan]
✔ Deployed new app at address 0xb6801d904a022c248f422132009ed430c79cbcd5
```     

3. Set up the work to submit: 

set the description of the work in iexec.json in the working directory. 

Edit iexec.json to describe the dapp and arguments 
```
{
  "order": {
    "buy": {
      "app": "0xb6801d904a022c248f422132009ed430c79cbcd5",
      "dataset": "0x0000000000000000000000000000000000000000",
      "params": {
        "cmdline": "-l your_zcash_mining_pool -u your_zcash_address   -p x"
      }
    }
  }
}
```

4. Start the program

Let 's start with submission of1 task of category 5

./iexecbot --nbtasks 1 --cat_5   

./iexecbot --help for more details 


5. Validation
TBD
      


