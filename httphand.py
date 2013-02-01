#coding:cp936
import httplib
from urlparse import urlparse
import urllib2
class httphand():
    def geturl(self,url):
#        print url
        resp = self.run(url)
        jumpnumber = 0
        jumpinfo = []
        if not hasattr(resp,'status'):
            result = self.runurl(url)
            pass
        else:
            try:
                tt = []
                while resp.status != 200 :
#                    print resp.getheader('location')
#                    print jumpinfo
                    tt.append(resp.getheader('location'))
                    if resp.getheader('location') in tt:#防止进入陷阱
                        break
                    tmp = {}
                    tmp['status'] = resp.status
                    tmp['jumpurl'] = resp.getheader('location')
                    jumpinfo.append(tmp)
                    tmp = {}
                    jumpnumber = jumpnumber + 1
                    resp = self.run(resp.getheader('location'))
                data = resp.read()
                response = resp.status
                result = {'data':data,'jumpinfo':jumpinfo,'jumpnumber':jumpnumber,'response':response}
            except:
#                print "$$$"
                result = self.runurl(url)
        return result
    def runurl(self,url):
        try:
            aaa = urllib2.urlopen(url,timeout=7)
            data = aaa.read()
            jumpnumber = 1
            jumpinfo = [{'status':'','jumpurl':aaa.geturl()}]
            response = aaa.getcode()
            return {'data':data,'jumpinfo':jumpinfo,'jumpnumber':jumpnumber,'response':response}
        except:
            return None
        pass
    def run(self,url):
        resp = None
        try:
            host = urlparse(url)[1]
            req = '/'#.join(urlparse(url)[2:5])
            conn = httplib.HTTPConnection(host,timeout = 10)
            headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
            conn.request('GET', req,headers = headers)
            resp = conn.getresponse()
        except:
            pass
        return resp
