# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
import re
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1


# TODO: NewsStory-- write a class Newstory containing various given methods
class NewsStory():
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_subject(self):
        return self.subject
    def get_summary(self):
        return self.summary
    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word.lower()
    def is_word_in(self, text):
        wordList = re.split('\W+', text.lower())
        if self.word in wordList:
            return True
        else:
            return False
    

# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.title.lower())

# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.subject.lower())

# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.summary.lower())


# Filter stories: Problem 6
# TODO: filter_stories
def filter_stories(stories, triggerlist):
    """Take a list of triggers, apply them to the stories, and return a list where each 
    element corresponds to a story that matches at least one trigger (OR the triggers).
    Each element of the output list should be a string containing the story title and story
    summary separated by a colon: i.e. format:
    story.title: story.summary
    """
    ## Write the code here
    outL = []
    for story in stories: 
        for trigger in triggerlist: 
            if trigger.evaluate(story):
                outL.append('%s: %s' % (story.title, story.summary))
    return outL
