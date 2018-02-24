import urllib.parse as parser
import urllib.request as req
from bs4 import BeautifulSoup as BS
import abc

class SearchEngine:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.base = ""
        self.search_path = ""

    @abc.abstractmethod
    def search(self, searchfor=""):
        '''
            :param: searchfor Search for "searchfor" into the searchengine.
            :return: The return is a tuple of two elements, the links found on the search and the nextPage of results.
        '''
        return

    @abc.abstractmethod
    def linkSearch(self, link):
        '''
        Used to search with the same query params but on the next page of the searchengine.
        :param link:
        :return: A tuple of two elements, the next page of the search engine and a list of links found on that page
        '''
        return



class GoogleSearchEngine(SearchEngine):

    def __init__(self):
        self.base = "http://www.google.com"
        self.search_path = "/search"

    def search(self, searchfor=""):
        queryparams = None
        if len(searchfor) > 0:
            params = {"q": searchfor}
            queryparams = parser.urlencode(params)

        if queryparams is not None:
            get_request = self.base+self.search_path+"?"+queryparams
        else:
            get_request = self.base+self.search_path
        return self.googleExtract(get_request)

    def linkSearch(self, link):
        print(link)
        print(self.base+link)
        return self.googleExtract(self.base+link)

    def googleExtract(self, complete_link):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = req.Request(complete_link, headers=hdr)
        value = req.urlopen(request)
        content = BS(value)
        return [self.extractLinks(content), self.extractNextPage(content)]

    def extractLinks(self, google_response):
        links = []
        for element in google_response.findAll("a"):
            if element["href"][:4] == "/url":
                links.append(element["href"])
        return links

    def extractPages(self, google_response):
        foot_element = None
        for element in google_response.findAll("div"):
            if 'id' in element.attrs and element.attrs["id"] == "foot":
                foot_element = element

        pages = []
        print("Scan possible pages")
        for element in foot_element.findAll("a"):
            if "class" in element.attrs and "style" not in element.attrs:
                pages.append(element.attrs["href"])

        return pages

    def extractNextPage(self, google_response):
        foot_element = None
        for element in google_response.findAll("div"):
            if 'id' in element.attrs and element.attrs["id"] == "foot":
                foot_element = element

        pages = []
        print("Scan possible pages")
        for element in foot_element.findAll("a"):
            if "class" in element.attrs and "style" not in element.attrs:
                pages.append(element.attrs["href"])

        return (pages[-1:])[0]

    def extractLastPage(self, pages):
        return pages[-1:]