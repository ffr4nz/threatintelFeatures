import subprocess
import json
out = subprocess.Popen(['docker', 'run', '--rm', 'lirantal/is-website-vulnerable:latest', 'https://www.elmundo.es', '--json'],
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT)
stdout,stderr = out.communicate()
result = json.loads(stdout)
print(len(result['vulnerabilities']))
