
# ProofChain


## Project Description
ProofChain is a decentralized, web-based Evidence Management System (EMS) designed to securely store and retrieve criminal data. It leverages blockchain technology, IPFS (InterPlanetary File System), and MetaMask to ensure the immutability and security of evidence. 
## Features
* **User Authentication and Authorization:** Users log in using MetaMask wallet for secure access and role-based access control.
* **Evidence Submission:** Admins add evidence by submitting criminal data, metadata, and files through the "Add Evidence" page.
* **Transaction Signing via MetaMask:** Evidence submissions and data transactions are securely signed through MetaMask.
* **Evidence Retrieval:** Users search and view stored evidence by entering the unique hash ID on the "View Evidence" page.
* **Role-Based Access Control:** Admins can add evidence, while general users can only view evidence.
* **Immutable Data Storage:** Once added, evidence cannot be altered, ensuring the integrity and authenticity of data.
* **Blockchain Integration:** Evidence is securely stored on the blockchain with a unique hash ID for verification.
* **Unique Hash ID Generation:** Each piece of evidence is assigned a unique hash ID for secure retrieval and reference.
## Tech Stack
**Frontend:** HTML, CSS, Bootstrap, JavaScript, Web3.js

**Backend:** Python, Django

**Blockchain & Storage:** Ethereum, InterPlanetary File System (IPFS), MetaMask

**Database:** PostgreSQL

**Development Tools:** Ganache, Truffle, Metamask
## Get Started

1. Clone the repository:

```bash
  git clone https://github.com/aneetan/Evidence-Management-System.git
```
2. Navigate to project directory:

```bash
 cd Evidence-Management-System\EMS
```

3. Install the required dependencies:

```bash
 pip install -r requirements.txt
```
4. Migrate the database:

```bash
 python manage.py migrate
```
5. Run the Development Server:

```bash
 python manage.py runserver
```
6. Access the application in your browser at http://127.0.0.1:8000/ 
## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

