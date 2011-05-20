# -*- coding: UTF-8 -*-

# Dr. Hendrik Bunke <h.bunke@zbw.eu>
# German National Library of Economics (ZBW)
# http://zbw.eu/

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class SearchView(BrowserView):
    """custom search for ejournal papers. For custom search of
    plone types see search.SearchView"""

    template = ViewPageTemplateFile("search.pt")

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()

    
    def result_title(self, result):
        """
        returns better title for result
        """
        
        #import pdb; pdb.set_trace()
        if result.portal_type == 'eJFile':
            obj = result.getObject()

            paper = obj.aq_parent
            paper_view = getMultiAdapter((paper, self.request), name='paperView')
            text = "<em>%s</em>: %s" % (paper_view.getAuthorsForTitle(), paper.Title())
            
            return text

        if result.portal_type in ('JournalPaper', 'DiscussionPaper'):
            paper = result.getObject()
            paper_view = getMultiAdapter((paper, self.request), name='paperView')
            text = "<em>%s</em>: %s" % (paper_view.getAuthorsForTitle(), paper.Title())
            return text

        if result.portal_type == "Comment":
            title = result.getObject().getSubject()
            comment_view = getMultiAdapter((result.getObject(), self.request), name='commentView')
            author = comment_view.getFullname()
            text = "<em>%s</em>: %s" % (author, title)
            return text

        return result.pretty_title_or_id()

    def result_url(self, result):
        """
        """

        searchterm = self.request.SearchableText

        if result.portal_type == 'eJFile':
            url = "%s/count" %result.getURL()
            return url
        
        if result.portal_type == "Comment":
            comment_view =  getMultiAdapter((result.getObject(), self.request), name='commentView')
            url = comment_view.getCommentURL()
            
            #XXX searchterm funktioniert hier noch nicht (vermutlich wegen anchor in comment url)
            text = "%s?%s" %(url,searchterm)
            return url

        
        url = "%s?searchterm=%s" %(result.getURL(), searchterm)
        return url


    def result_text(self, result):
        """
        """
        pt = result.portal_type
        
        date = result.created.strftime("%B %d, %Y")
        text = "<strong>%s</strong> %s" %(pt, date)
        return text



   


    

