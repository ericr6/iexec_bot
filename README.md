# iexec_bot

Required: 
python3 
iexec SDK
Follow https://github.com/iExecBlockchainComputing/iexec-sdk


  
the program manages task submission in iExec marketplace 
Tested on kovan 

Exemple of use:

1. Install iExec SDK:

Make sure iExec SDK is installed, and has been tested.
you should have your wallet, you account
make sure you get enough RLC and few ether

2. Set up your app:

Define the price, the name of your dapp and the name of your image from docker hub.
The app deployed for the tutorial is a zcash minning software but it can be any applications. 
The process is the same since you get a docker image.   
  
Edit iexec.json
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
 
Deploy you dapp 
```
iexec app deploy
```     
```
ℹ using chain [kovan]
✔ Deployed new app at address 0xb6801d904a022c248f422132009ed430c79cbcd5
```     

3. Set up the work to submit: set the description of the work in iexec.json in the working directory. 

Edit iexec.json 
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
 
./iexecbot --nbtasks 1 --cat_5   

./iexecbot --help for more details 

5. Validation
TBD
      


