import os
import subprocess
import re


p = subprocess.Popen('python -m pip show pyexiv2', stdout=subprocess.PIPE)
stdout, stderr = p.communicate()
site_packages_path = re.findall(r'Location: ([^\r\n]*)', stdout.decode())[0]
pyexiv2_dir = os.path.join(site_packages_path, 'pyexiv2')

p = subprocess.Popen('pytest -v', stdout=subprocess.PIPE, cwd=pyexiv2_dir)
for i in p.communicate():
    if i:
        print(i.decode())

exit(p.returncode)
