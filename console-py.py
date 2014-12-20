from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
       

class XMPPHandler(webapp.RequestHandler):
    def post(self):
			message = xmpp.Message(self.request.POST)
			message.reply('test')   	
 

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
