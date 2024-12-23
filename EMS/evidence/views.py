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

# Function to retrieve data from Pinata using IPFS hash
def get_data_from_ipfs(ipfs_hash):
    headers = {
        'Authorization': f"Bearer {settings.PINATA_JWT_TOKEN}",
    }
    url = f'https://gateway.pinata.cloud/ipfs/{ipfs_hash}'  
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching IPFS data: {e}")
        return None

def home(request):
    return render(request, 'index.html')

def add(request):
    return render(request, 'Form.html')

def view(request):
    return render(request, 'view.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import requests
from django.conf import settings

@csrf_exempt
def save_to_ipfs(request):
    if request.method == "POST":
        # Extract form data
        form_data = request.POST.dict()
        files = request.FILES.getlist('evidence')

        upload_dir = os.path.join(settings.BASE_DIR, 'media')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        evidence_data = []
        for file in files:
            file_path = os.path.join(upload_dir, file.name)

            # Save the file locally
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # Upload the file to IPFS using Pinata
            try:
                with open(file_path, 'rb') as f:
                    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
                    headers = {
                        "Authorization": f"Bearer {settings.PINATA_JWT_TOKEN}",
                    }
                    files_data = {"file": (file.name, f)}
                    response = requests.post(url, files=files_data, headers=headers)

                    if response.status_code == 200:
                        ipfs_hash = response.json()["IpfsHash"]
                        evidence_data.append({
                            "file_name": file.name,
                            "ipfs_hash": ipfs_hash,
                        })
                    else:
                        return render(request, "Form.html", {
                            "alert_message": f"Failed to upload {file.name}: {response.text}"
                        })
            except Exception as e:
                return render(request, "Form.html", {
                    "alert_message": f"An error occurred with file {file.name}: {str(e)}"
                })

        # Combine form data and evidence information
        data_to_save = {
            "name": form_data.get("name"),
            "crime": form_data.get("crime"),
            "nationality": form_data.get("nationality"),
            "nationalId": form_data.get("nationalId"),
            "description": form_data.get("description"),
            "evidence_files": evidence_data,
        }

        # Save the consolidated data to IPFS
        try:
            url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.PINATA_JWT_TOKEN}",
            }
            response = requests.post(url, json=data_to_save, headers=headers)

            if response.status_code == 200:
                ipfs_hash = response.json()["IpfsHash"]
                return JsonResponse({'ipfs_hash': ipfs_hash, 'evidence_data': evidence_data})
            else:
                return render(request, "Form.html", {
                    "alert_message": f"Failed to save evidence data: {response.text}"
                })
        except Exception as e:
            return render(request, "Form.html", {
                "alert_message": f"An error occurred while saving evidence data: {str(e)}"
            })

    return render(request, "Form.html")


@csrf_exempt   
def process_ipfs(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  
            ipfs_hash = data.get('ipfsHash', '')
            
            ipfs_data = get_data_from_ipfs(ipfs_hash)
            print(ipfs_data)

            if ipfs_data:
                crime_data = {
                    'name': ipfs_data.get('name', ''),
                    'crime': ipfs_data.get('crime', ''),
                    'nationality': ipfs_data.get('nationality', ''),
                    'nationalId': ipfs_data.get('nationalId', ''),
                    'description': ipfs_data.get('description', ''),
                }
                # Extract evidence files from the IPFS data
                evidence_files = ipfs_data.get('evidence_files', [])

                # Render the template with crime data and evidence files
                return JsonResponse({
                    'crime_data': crime_data,
                    'evidence_files': evidence_files
                })
            
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Failed to fetch data from IPFS."
                }, status=400)

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