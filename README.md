# DataLeak Detector

**DataLeak Detector** - project for preventing unauthorized access to information at critical infrastructure objects. This project written in "pure" Python using different open-source libraries. This project contain three parts: [DataLeak Control Panel](https://github.com/1Lorde/dataleak_detector/tree/master/control_panel) and [DataLeak Agent](https://github.com/1Lorde/dataleak_detector/tree/master/agent) and deployed ELK Stack, which aggregate data from our agents. Also we use DSTU 9041:2020 Elliptic curves [parameters](https://github.com/1Lorde/dataleak_detector/blob/master/openSSL/ec_custom.asn1) for generating OpenSSL cerificates.


## Demo videos:
 1. ![Demo video (EN)](/demo/demo_en.mp4)
 2. ![Demo video (UKR)](/demo/demo_ukr.mp4)


## DataLeak Agent Build
![DataLeak Agent screenshot](/img/agent.png)

### Prerequisites
 1. Python 3.9 - [Download](https://www.python.org/downloads/release/python-390/).

### Instruction for Windows

 1. Open command line (or terminal).
 2. Navigate to agent directory `cd dataleak_detector\\agent`.
 2. Run  `pip install -r requirements.win.txt`.
 4. Execute command `python main.py`.

### Instruction for Linux

 1. Open command line (or terminal).
 2. Navigate to agent directory `cd dataleak_detector/agent`.
 2. Run  `pip install -r requirements.linux.txt`.
 4. Execute command `python main.py`.


## DataLeak Control Panel Build

![DataLeak Control Panel screenshot](/img/control_panel3.png)

 ### Prerequisites
 1. Python 3.9 - [Download](https://www.python.org/downloads/release/python-390/).

 ### Instruction
 1. Open command line (or terminal).
 2. Navigate to agent directory `cd dataleak_detector/control_panel`.
 2. Run  `pip install -r requirements.txt`.
 4. Execute command `python main.py`.

## Kibana Dashboard
![Kibana Dashboard screenshot](/img/kibana.png)
