# -*- coding: UTF-8 -*-

# Dr. Hendrik Bunke <h.bunke@zbw.eu>
# German National Library of Economics (ZBW)
# http://zbw.eu/

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SearchView(BrowserView):
    """custom search for ejournal papers. For custom search of
    plone types see search.SearchView"""

    template = ViewPageTemplateFile("search.pt")

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()


    def results_sorted(self, results):
        return sorted(results, key=lambda result: result.created, reverse=True)
