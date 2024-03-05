from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import json
import time
from zapv2 import ZAPv2

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        # Define the target URL to scan
        target_url = request.POST.get('target_url')

        # Define the path to ZAP API
        zap_api_url = 'http://localhost:8080/'

        # Initialize ZAP API client
        zap = ZAPv2(apikey='t5n473k4kjn9lbtv9b6b4tpur0', proxies={'http': zap_api_url, 'https': zap_api_url})

        try:
            # Start active scanning
            print('Active Scanning target {}'.format(target_url))
            scanID = zap.ascan.scan(target_url)
            while int(zap.ascan.status(scanID)) < 100:
                # Loop until the scanner has finished
                print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
                time.sleep(5)

            print('Active scanning completed.')

            # Generate the JSON report
            print('Generating JSON report...')
            report_json = zap.core.jsonreport()
            with open('zap_report.json', 'w') as f:
                f.write(json.dumps(report_json))

            print('Report saved as zap_report.json')

            return HttpResponse('Scan completed successfully. Check the generated report.')

        except Exception as e:
            # Handle any exceptions that might occur during scanning
            return HttpResponse(f'Error occurred: {str(e)}')

        return render(request, 'home.html')
