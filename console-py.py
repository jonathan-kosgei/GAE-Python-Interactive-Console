from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from code import InteractiveConsole
import sys

class FileCacher:
    """Cache stdout text so that we can analyze it"""
    def __init__(self): self.reset()
    def reset(self): self.out = []
    def write(self, line):self.out.append(line)
    def flush(self):
        output = '\n'.join(self.out)
        self.reset()
        return output
        
class Shell(InteractiveConsole):
    """Wrapper around Python that can filter input/output to the shell"""
    def __init__(self):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        InteractiveConsole.__init__(self)
        return
    def get_output(self):sys.stdout = self.cache
    def return_output(self):sys.stdout = self.stdout
    def push(self, line):
        self.get_output()
        #line = filter(line)
        InteractiveConsole.push(self, line)
        self.return_output()
        output = self.cache.flush()
        #output = filter(output)
        print output # or something else
        

class XMPPHandler(webapp.RequestHandler):
    def post(self):
    	message = xmpp.Message(self.request.POST)
    	message.reply(sh.push(message.body))

 

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("Working Awesomely Fine")

app = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler),('/',MainPage)],
                                     debug=True)
 
def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
    sh = Shell()
    sh.interact()
	
