import os

out = os.popen("ps aux | grep python | grep Users/sreenath/Documents/bitcoin_code").read()
import re
cmds = out.split('\n')
print(len(cmds))

# for i in cmds:
#     l = re.sub(' +', ' ', i)
#     pid = l.split(' ')
#     print(pid[1])

#     out2 = os.popen("kill "+pid[1]).read()
