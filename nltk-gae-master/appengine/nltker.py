import webapp2
import logging

import nltk

# Test project for NLTK for app engine
# copyright (c) 2012 Client Side Web
# for the public domain.
# NOTE: prior to running, download NLTK for App Engine and PyYAML libs and place in project root.

class nltkTestPage(webapp2.RequestHandler):
	def get(self):
		
		text = nltk.word_tokenize("And now for something completely different")
		tags = nltk.pos_tag(text)
		
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('hello world, len(tags):%s' % len(tags))
		for token in tags:
			self.response.out.write('\r\ntoken: %s tags: %s' % (token[0], token[1]))
		
app = webapp2.WSGIApplication([('/nltk', nltkTestPage)], debug=True)