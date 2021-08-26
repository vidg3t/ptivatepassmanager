import subprocess
MyOut = subprocess.Popen(['pwd	'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
stdout,stderr = MyOut.communicate()
print(stdout)
print(stderr)