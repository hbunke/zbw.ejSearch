# -*- coding: UTF-8 -*-

# Dr. Hendrik Bunke <h.bunke@zbw.eu>
# German National Library of Economics (ZBW)
# http://zbw.eu/

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import Interface
from Products.AdvancedQuery import In, Eq, And, Or, Between
from zope.component import getMultiAdapter


class AdvancedSearchView(BrowserView):
    """custom search for ejournal papers. For custom search of
    plone types see search.SearchView"""

    template = ViewPageTemplateFile("advanced_search_results.pt")

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()

    
    def search(self, request):
        """
        """
        # get serchterms
        searchable = request.form.get("SearchableText", None)
        fulltext   = request.form.get("SearchableText", "")
        authors    = request.form.get("authors", "")
        #author_id  = request.form.get("author_id", "")
        abstract   = request.form.get("abstract", "")
        title      = request.form.get("title", "")        
        jel        = request.form.get("jel", "")
        papers     = request.form.get("papers", [])
        #year       = request.form.get("year", "all")
        #period     = request.form.get("period", "all")        
        
        query = ""
                
        #import pdb; pdb.set_trace()
        if "discussion" in papers:

            query = Or(Eq('portal_type', 'File'),
                        And(Eq('portal_type', "DiscussionPaper"), 
                        In('review_state', ("rejected", "discussible"))
                        )
                        )

        if "journal" in papers:
            query_jp = Or(Eq("portal_type", "JournalPaper"), Eq('portal_type', 'eJFile'))
            
            if query == "":
                query = query_jp
            else:
                query = Or(query, query_jp)   

        #if "comment" in papers:
        #    query = And(Eq('portal_type', "Comment"))

        if query == "":
            return []

        if searchable is not None:
            if searchable == "":
                return []
                
            query = And(query,
                        Eq("SearchableText", searchable))
        
            
      # if year != "all":
      #     year_start, year_end = _createYearRange(year)
      #     query = And(query,
      #                 Between("created", year_start, year_end))

      # elif period != "all":
      #     period_start, period_end = _createPeriod(period)
      #     query = And(query,
      #                 Between("created", period_start, period_end))
                                       
        if fulltext != "":
            #query_fulltext = In("eJFulltext", fulltext)

            query_fulltext = In("SearchableText", fulltext)            
            query = And(query, query_fulltext)


#### XXX getAuthorsForTitle nicht mehr existent. refactoren!
        if authors != "":
            query_author = In("getAuthorsForTitle", authors)            
            query = And(query, query_author)
            
        if abstract != "":
            query_abstract = Eq("getAbstract", abstract)            
            query = And(query, query_abstract)

        if title != "":
            query_title = In("Title", title)            
            query = And(query, query_title)

        if jel != "":            
            query_jel = Eq("getJelAsString", jel)
            query = And(query, query_jel)

        # search        

        brains = self.context.portal_catalog.evalAdvancedQuery(query)                
        
        return brains
        #return [brain.getObject() for brain in brains]
    
