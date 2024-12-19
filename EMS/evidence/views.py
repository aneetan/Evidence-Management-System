import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from web3 import Web3


def home(request):
    return render(request, 'index.html')

def add(request):
    return render(request, 'Form.html')

def view(request):
    return render(request, 'view.html')

def save_to_blockchain(ipfs_hash, case_id):
    


@csrf_exempt
def save_to_ipfs(request):
    if request.method == "POST":
        # Extract form data
        form_data = request.POST.dict()
        files = request.FILES.getlist('evidence')

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
                return render(request, "index.html", {
                    "alert_message": f"Evidence added successfully! IPFS Hash: {ipfs_hash}"
                })
            else:
                return render(request, "Form.html", {
                    "alert_message": f"Failed to save evidence: {response.text}"
                })
        except Exception as e:
            return render(request, "Form.html", {
                "alert_message": f"An error occurred: {str(e)}"
            }) 

    return render(request, "Form.html")



