# QCoin

QCoin is the worlds FIRST qapp!  A qapp is a full-stack quantum application that interfaces directly with the IBMQ Research HQ at the Thomas J. Watson Research Center in the cloud.  QCoin is a heads or tails game to which the user chooses either heads or tails when the game begins.  The application then connects to a REAL IBMQ quantum computer to which it will put qubit 1 into superposition and then entangle two qubits and finally measure the qubits, irrevocably disturbing the superposition state and forcing a classical 0 or 1 as output to determine the games result.

## OFFICIAL PRODUCT DEMO VIDEO

[youtube.com](https://youtu.be/BB7TDDKb-F4/)

## OFFICIAL PRODUCT TUTORIAL

[medium.com](https://medium.com/@mytechnotalent/quantum-computing-1-qcoin-the-birth-of-the-qapp-88103f3921be/)

## Installation

Navigate to [python.org](https://www.python.org/downloads/) to install Python 3+.

Navigate to [git-scm.com](https://git-scm.com/book/en/v1/Getting-Started-Installing-Git) to install Git.

Open a terminal window and type the below command to clone the GitHub QApp repo.

```bash
git clone https://github.com/mytechnotalent/qapp.git
cd qapp
```

With the terminal window open, type the below command to install all of the dependencies.

```bash
pip3 install -r requirements.txt
```

## Create and IBM Q Experience Account

Navigate to [quantum-computing.ibm.com](https://quantum-computing.ibm.com/) and create a new account.

Navigate to [quantum-computing.ibm.com/account](https://quantum-computing.ibm.com/account) and click the 'Copy token' button in blue to obtain your API.  Open up a text editor and paste in the token temporarily.

Open a terminal window and type the below command to setup your API key with your software.  Make sure you replace the 'MY_API_TOKEN' below with your API key you have stored in your text editor.  Be sure to paste the API key between the single quotes as shown below.

```python
python3
>>> from qiskit import IBMQ
>>> IBMQ.save_account('MY_API_TOKEN')
>>> quit()
```

## Run Application

With the terminal window open, type the below command to run your qapp.

```bash
python app.py
```

Navigate to [localhost:5000](http://localhost:5000) to launch your qapp in your default web browser.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0/)
