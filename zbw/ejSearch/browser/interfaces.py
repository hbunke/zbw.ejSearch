from zope.interface import Interface


class ISearchView(Interface):
    """
    standard search for ejournal
    """


class IAdvancedSearchView(Interface):
    """
    advanced search for ejournal content types
    """

    def search():
        """
        custom search method for ejournal content types
        """


class ISearchResults(Interface):
    """
    common methods for search results
    """
    
    def result_title():
        """
        returns better title for result
        """

    def result_url():
        """
        returns url for result object; eventually with searchterm
        """

    def result_text():
        """
        returns content type and creation date of result object
        """

    def result_quote():
        """
        returns quotes in result object with searchterm
        """




