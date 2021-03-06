# -*- coding: UTF-8 -*-

# Dr. Hendrik Bunke <h.bunke@zbw.eu>
# German National Library of Economics (ZBW)
# http://zbw.eu/


import re
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from stripogram import html2text


class SearchResults(BrowserView):
    """
    """

    def title(self, result):
        """
        returns better title for result
        """
        
        if result.portal_type == 'eJFile':
            obj = result.getObject()

            paper = obj.aq_parent
            paper_view = getMultiAdapter(
                    (paper, self.request), name='paperView')
            text = "<em>%s</em>: %s" % (paper_view.authors_as_string(),
                    paper.Title())
            
            return text

        if result.portal_type in ('JournalPaper', 'DiscussionPaper'):
            paper = result.getObject()
            paper_view = getMultiAdapter((paper, self.request), 
                    name='paperView')
            text = "<em>%s</em>: %s" % (paper_view.authors_as_string(), 
                    paper.Title())
            return text

        if result.portal_type == "Comment":
            title = result.getObject().getSubject()
            comment_view = getMultiAdapter((result.getObject(), self.request),
                    name='commentView')
            author = comment_view.getFullname()
            text = "<em>%s</em>: %s" % (author, title)
            return text

        return result.pretty_title_or_id()


    def url(self, result):
        """
        """
        searchterm = self.request.SearchableText

        if result.portal_type == 'eJFile':
            url = "%s/count" %result.getURL()
            return url
        
        if result.portal_type == "Comment":
            comment_view =  getMultiAdapter((result.getObject(), self.request),
                    name='commentView')
            url = comment_view.getCommentURL()
            
            #XXX searchterm funktioniert hier noch nicht (vermutlich wegen 
            #anchor in comment url)
            text = "%s?%s" %(url,searchterm)
            return url

 #       import pdb; pdb.set_trace()
        url = "%s?searchterm=%s" %(result.getURL(), searchterm)
        return url


    def text(self, result):
        """
        """
        mapping = {'DiscussionPaper' : 'Discussionpaper', 
                   'JournalPaper' : 'Journalarticle', 
                   'eJFile' : 'Journalarticle (PDF)',
                   'SpecialIssue' : 'Specialissue', }

        pt = result.portal_type
        if mapping.has_key(pt):
            pt_text = mapping[pt]
        else:
            pt_text = pt
        
        date = result.created.strftime("%B %d, %Y")
        text = "<strong>%s</strong> %s" %(pt_text, date)
        return text

    
    def quote(self, result):
        """
        """
        #TODO: only return quotes when searchterm is not in Title

        search = self.request.SearchableText
        
        if result.portal_type in ('JournalPaper'):
            result_text = html2text(result.getAbstract, 
                    ignore_tags=('a','span','br','p'))

        else:
            #Due to catalog out of sync, result.SearchableText sometimes returns
            #'Missing.Value', while result.getObject().SearchableText returns
            #as expected. So in that case we must get the object. We test this
            #with basestring (True for str and unicode)
            
            if hasattr(result, 'SearchableText'):
                if isinstance(result.SearchableText, basestring):
                    result_text = result.SearchableText
                else:
                    result_text = result.getObject().SearchableText()
            else:
                result_text = result.getObject().SearchableText()
                #TODO catch errors
                

        quotes = []
        quotes = set(quotes)
        search_text = self.request.SearchableText.split()
        
        for t in search_text:
            t = t.lower()
            t = t.replace('"', '')
            if t in result_text.lower():
                lines = re.split(r'\s*[!?.]\s*', result_text)
                for line in lines:
                    if t in line.lower() and len(quotes) < 3:
                        quotes.add(line)
        return quotes



   


    

    
