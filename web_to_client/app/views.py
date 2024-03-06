from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import json
import time
from zapv2 import ZAPv2


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')  # Assuming you have 'home.html'

    def post(self, request):
        # Get target URL and API key (modify as needed)
        target_url = request.POST.get('target_url')
       
        zap_api_url = 'http://127.0.0.1:8080/'  # Assuming ZAP is running on localhost:8080

        # Initialize ZAPv2 client
        try:
            zap = ZAPv2(apikey='u7dl5crb9gu8dhpesd7ue6htl', proxies={'http': zap_api_url, 'https': zap_api_url})
        except Exception as e:
            return HttpResponse(f'Error connecting to ZAP: {str(e)}')

        try:
            # Start active scanning
            print('Active Scanning target {}'.format(target_url))
            scan_id = zap.ascan.scan(target_url)

            while True:
                scan_status = zap.ascan.status(scan_id)

                if scan_status == '100':
                    # Scan completed successfully
                    print('Active scanning completed.')
                    break
                elif scan_status.isdigit():
                    # Convert to integer if possible (handle unexpected values gracefully)
                    scan_progress = int(scan_status)
                    print('Scan progress %: {}'.format(scan_progress))
                else:
                    # Handle unexpected status values (log, display appropriate message to user)
                    print(f"Unexpected scan status: {scan_status}")
                    # ... consider logging or displaying an informative message to the user

                time.sleep(5)  # Adjust sleep time as needed

            # Generate the JSON report (modify as needed)
            print('Generating JSON report...')
            report_json = zap.core.jsonreport()

            # Choose appropriate output format based on your needs

            # Option 1: Save report to a file (modify as needed)
            # with open('zap_report.json', 'w') as f:
            #     f.write(json.dumps(report_json))
            # print('Report saved as zap_report.json')

            # Option 2: Return report data in the response (modify as needed)
            # return HttpResponse(json.dumps(report_json), content_type='application/json')

            return HttpResponse('Scan completed successfully. Check the generated report.')  # Adjust message as needed

        except Exception as e:
            # Handle and log exceptions using proper logging practices (e.g., Django logging)
            # and provide user-friendly error messages
            print(f'Error during scanning: {str(e)}')
            return HttpResponse('An error occurred during scanning. Please check the server logs for details.')

        return render(request, 'home.html')  # Adjust return value based on chosen reporting approach
