import json
import os
import requests
import sys

def send_sonarcloud_to_defectdojo(project_key, token, defectdojo_api_url, defectdojo_api_key):
    print("Starting send_sonarcloud_to_defectdojo")
    sonar_host_url = os.environ.get("SONAR_HOST_URL")
    print(f"Sonar Host URL: {sonar_host_url}")
    url = f"{sonar_host_url}/api/issues/search?componentKeys={project_key}&resolved=false"
    headers = {"Authorization": f"Basic {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("SonarCloud API call successful.")
        issues = response.json().get("issues", [])
    except requests.exceptions.RequestException as e:
        print(f"Error calling SonarCloud API: {e}")
        return

    defectdojo_findings = []
    for issue in issues:
        defectdojo_findings.append({
            "title": f"SonarCloud: {issue.get('message')}",
            "description": issue.get('message'),
            "severity": issue.get('severity', 'Info').capitalize(),
            "file_path": issue.get('component'),
            "line_number": issue.get('line'),
            "scanner": "SonarCloud",
            "active": True,
            "verified": False,
            "false_p": False,
            "duplicate": False,
            "out_of_scope": False,
            "cwe": [],
            "tags": [],
            "date": issue.get('creationDate')
        })

    defectdojo_payload = defectdojo_findings
    if defectdojo_payload:
        try:
            curl_command = f'curl -X POST "{defectdojo_api_url}/api/v2/findings/" -H "Authorization: Token {defectdojo_api_key}" -H "Content-Type: application/json" -d \'{json.dumps(defectdojo_payload)}\''
            os.system(curl_command)
            print("DefectDojo API call successful.")
        except Exception as e:
            print(f"Error calling DefectDojo API: {e}")

if __name__ == "__main__":
    project_key = "circlecicd1_circlecicd0123"
    token = os.environ.get("SONAR_TOKEN")
    defectdojo_api_url = os.environ.get("DEFECTDOJO_API_URL")
    defectdojo_api_key = os.environ.get("DEFECTDOJO_API_KEY")
    send_sonarcloud_to_defectdojo(project_key, token, defectdojo_api_url, defectdojo_api_key)