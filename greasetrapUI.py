from webapp import GreaseTrapUI
import httplib2

def checkRoush(url=None):
    conn = httplib2.Http()
    resp,content = conn.request(url, "GET") 
    return resp.status

if __name__ == '__main__':
    foo = GreaseTrapUI("greasetrapUI", configFile="greasetrapUI.conf", debug=True)

    try:
        checkRoush(foo.base_url)
        foo.run()
    except:
        print "Roush API is not available. Please try again."

