## Shipment

### Shipment Creation

createShipment.py creates a shipment with dewars, containers, and samples. 

### Requirements

1.- Protein acronym should exist within the proposal
2.- credentials.properties file should exist within the folder and should contain:
```
[Credential]
user=mx415	
password=******
site=ESRF

[Proposal]
type=mx
number=415

```

### Run

You would need python >2.6 and some dependencies like suds

```
python createShipment.py
```

### Result

This web method will return the shipment created in the database.
