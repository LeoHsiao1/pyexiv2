import os
import re
import subprocess
import shlex


p = subprocess.Popen(shlex.split('python -m pip show pyexiv2'), stdout=subprocess.PIPE)
stdout, stderr = p.communicate()
site_packages_path = re.findall(r'Location: ([^\r\n]*)', stdout.decode())[0]
pyexiv2_dir = os.path.join(site_packages_path, 'pyexiv2')

p = subprocess.Popen(shlex.split('pytest -v'), stdout=subprocess.PIPE, cwd=pyexiv2_dir)
for i in p.communicate():
    if i:
        print(i.decode())

exit(p.returncode)
