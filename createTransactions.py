import iota
import random

import seedGenerator
import adc1115
from datetime import datetime

def main():
    DevnetNode = "https://nodes.devnet.iota.org:443"

    seed_vendor = seedGenerator.generateSeed()
    seed_investor = seedGenerator.generateSeed()

    api_vendor = iota.Iota(DevnetNode,
              seed = seed_vendor)

    api_investor = iota.Iota(DevnetNode,
              seed = seed_investor)
    readings1 = adc1115.main()
    readings2 = adc1115.main()
    
    result,address = performTransactions(api_vendor, api_investor, readings1, readings2)
    return (result,address)

def generateInvestorAddresses(api_investor):
    addresses_investor = api_investor.get_new_addresses(index=0, count = 1, security_level = 2)
    return address_investor

def generateVendorAddresses(api_vendor):
    addresses_vendor = api_vendor.get_new_addresses(index = 0, count = 2, security_level = 2)
    return addresses_vendor


def performTransactions(api_vendor, api_investor, readings1, readings2):
    
    #Extracting addresses from the generated vendor addresses 
    vendorAddress = generateVendorAddresses(api_vendor)
    address_available = vendorAddress['addresses']
    targetAddress1 = address_available[0]
    targetAddress2 = address_available[1]
  	
    print(targetAddress1)
    print(targetAddress2)
     
    #Preparing the message, converting the values received into a string to send as a message 
    readings_str1 = [str(i) for i in readings1] 
    readings_str2 = [str(i) for i in readings2] 
    message1 = ",".join(readings_str1)
    message2 = ",".join(readings_str2)
   
    NowIs = datetime.now() # get a actual date & time - just to have some meaningfull info
    message1 = message1 +": " + str(NowIs)
 
    pt = iota.ProposedTransaction(address = iota.Address(targetAddress1), # 81 trytes long address
                              message = iota.TryteString.from_unicode('Values and TimeStamp are %s.'% (message1)),
                              tag     = iota.Tag(b'HRIBEK999IOTA999TUTORIAL'), # Up to 27 trytes
                              value   = 0)
    
    NowIs = datetime.now() # get a actual date & time - just to have some meaningfull info
    message2 = message2 +": " + str(NowIs)
 
    pt2 = iota.ProposedTransaction(address = iota.Address(targetAddress2), # 81 trytes long address
                               message = iota.TryteString.from_unicode('Values and TimeStamp are %s.'% (message2)),
                               tag     = iota.Tag(b'HRIBEK999IOTA999TUTORIAL'), # Up to 27 trytes
                               value   = 0)

    # preparing bundle that consists of both transactions prepared in the previous example
    pb = iota.ProposedBundle(transactions=[pt,pt2]) # list of prepared transactions is needed at least
    
    pb.finalize()
    Trytes = pb.as_tryte_strings() # bundle as trytes
    
    gta = api_vendor.get_transactions_to_approve(depth=3) # get tips to be approved by your bundle
    att = api_vendor.attach_to_tangle(trunk_transaction=gta['trunkTransaction'], # first tip selected
                           branch_transaction=gta['branchTransaction'], # second tip selected
                           trytes=Trytes, # our finalized bundle in Trytes
                           min_weight_magnitude=14) # MWMN
    
    print("Broadcasting transaction...")
    res = api_vendor.broadcast_and_store(att['trytes'])
    return (res,targetAddress1)
