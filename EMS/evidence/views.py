import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings


def formLoad(request):
    return render(request, 'index.html')

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

        # Save data to IPFS (using Pinata in this example)
        try:
            url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.PINATA_JWT_TOKEN}",
            }
            response = requests.post(url, json=data_to_save, headers=headers)

            if response.status_code == 200:
                ipfs_hash = response.json()["IpfsHash"]
                return JsonResponse({"success": True, "ipfs_hash": ipfs_hash})
            else:
                return JsonResponse({"success": False, "error": response.text}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)



