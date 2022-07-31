import socket
import os
from pathlib import Path
def getip(ipv6):
    if ipv6:
        afi = socket.AF_INET6
        ip8 = '2001:4860:4860::8888'
    else:
        afi = socket.AF_INET
        ip8 = '8.8.8.8'
    
    try:
        s=socket.socket(afi,socket.SOCK_DGRAM)
        s.connect((ip8,80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip
def generate_str(url):
    srep = '.replace(/{idinfo}/g,"{char_info}")'
    m = [(str(ord(i)+631)+'_',i) for i in url]
    x = set(m)
    print(len(x),len(m))
    stt = ''.join([i[0] for i in m])
    rr = [srep.format(idinfo=idinfo,char_info=char_info) for idinfo,char_info in x]
    rr = ''.join(rr)
    return "'"+stt+"'"+rr
    
def main():
    git = '/usr/bin/git'
    h5_name = 'bsg.html'
    html = '''<!DOCTYPE html>
<html lang="en">
    <head>
        <script language="javascript" type="text/javascript"> 
            window.location.href=__url__;
        </script>
    </head>
</html>'''
    ipf = Path().home()/'.ipv6_addr.log'
    if ipf.is_file():
        ipv6_addr = ipf.read_text().strip()
    else:
        open(ipf,'w').close()
        ipv6_addr = ''
    print(ipv6_addr)
    new6 = getip(True)
    if new6 != ipv6_addr or True:
        print('write new addr,',new6)
        fp = open(ipf,'w')
        fp.write(new6)
        fp.close()
        url = f'https://[{new6}]:8086'
        js_str = generate_str(url)
        html = html.replace('__url__',js_str)
        fp = open(h5_name,'w')
        fp.write(html)
        fp.close()

        os.system(f'{git} add -u')
        os.system(f'{git} commit -m "update"')
        os.system(f'{git} push')
        print("更新ip")




if __name__=='__main__':
    import time
    for i in range(10000):
        time.sleep(10)
        main()