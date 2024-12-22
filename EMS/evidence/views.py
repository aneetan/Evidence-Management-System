import requests
import os
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime
from django.http import JsonResponse

load_dotenv()

WEB3_PROVIDER = "https://mainnet.infura.io/v3/2c97cd49958246ea81484b7873bf1bc6"  
# CONTRACT_ADDRESS = {settings.CONTRACT_ADDRESS}
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_ipfsHash", "type": "string"},
            {"internalType": "address", "name": "_walletAddress", "type": "address"},
            {"internalType": "uint256", "name": "_timestamp", "type": "uint256"}
        ],
        "name": "saveEvidence",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "evidenceCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
# contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def home(request):
    return render(request, 'index.html')

def add(request):
    return render(request, 'Form.html')

def view(request):
    return render(request, 'view.html')


@csrf_exempt
def save_to_ipfs(request):
    if request.method == "POST":
        # Extract form data
        form_data = request.POST.dict()
        wallet_address = form_data.get("wallet_address")
        files = request.FILES.getlist('evidence')

        upload_dir = os.path.join(settings.BASE_DIR, 'uploaded_files') 
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        for file in files:
            file_path = os.path.join(upload_dir, file.name)
            
            # Save the file locally
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

        # Process uploaded files (optional)
        evidence_data = []
        for file in files:
            evidence_data.append(file.name)

        # Combine form data and evidence information
        data_to_save = {
            "name": form_data.get("name"),
            "crime": form_data.get("crime"),
            "nationality": form_data.get("nationality"),
            "nationalId": form_data.get("nationalId"),
            "description": form_data.get("description"),
            "evidence_files": evidence_data,
        }

        # Save data to IPFS using Pinata
        try:
            url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.PINATA_JWT_TOKEN}",
            }
            response = requests.post(url, json=data_to_save, headers=headers)

            if response.status_code == 200:
                ipfs_hash = response.json()["IpfsHash"]
                return JsonResponse({'ipfs_hash': ipfs_hash})
            
            else:
                return render(request, "Form.html", {
                    "alert_message": f"Failed to save evidence: {response.text}"
                })
        except Exception as e:
            return render(request, "Form.html", {
                "alert_message": f"An error occurred: {str(e)}"
            }) 

    return render(request, "Form.html")
#0xc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b

@csrf_exempt   
def process_ipfs(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Get the JSON data from the request
            ipfs_hash = data.get('ipfsHash') 
            
             
            print(f"Received IPFS Hash: {ipfs_hash}")
            
             
            return JsonResponse({
                "status": "success",
                "message": "IPFS hash processed successfully.",
                "hash": ipfs_hash
            })

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "status": "error",
                "message": "Failed to process IPFS hash."
            }, status=400)
    else:
        return JsonResponse({
            "status": "error",
            "message": "Only POST method is allowed."
        }, status=405)