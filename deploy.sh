#!/bin/bash
sudo echo "#!/bin/bash">/usr/bin/wccmd
sudo echo "cd $PWD"' && python3 -m wechatCMD "$@"'>>/usr/bin/wccmd
sudo chmod +x /usr/bin/wccmd

sudo echo "#!/bin/bash">/usr/bin/wcdaemon
sudo echo "cd $PWD"' && python3 -m wechatDaemon'>>/usr/bin/wcdaemon
sudo chmod +x /usr/bin/wcdaemon