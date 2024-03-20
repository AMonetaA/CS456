#  CS456 Assignment 2

  

Moneta Wang

  

20885892

  

  

This server program was built and tested on **ubuntu2204-002**， **ubuntu2204-006**， **ubuntu2204-010**.

  

##  Instructions

1. Open a terminal and navigate to the directory containing the server program files.
2. Create an Input file.

3. Run the emulator program using the following command:

```bash

python3 network_emulator.py 11191 ubuntu2204-006 11194 11193 ubuntu2204-002 11192 1 0.2 0

```

4. Run the receiver program using the following command:

```bash

python receiver.py ubuntu2204-010 11193 11194 output.txt

```
5. Run the sender program using the following command:

```bash

python sender.py ubuntu2204-010 11191 11192 50 input.txt

```

  
