# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .models import Notes, PYQ  # अपने Models के हिसाब से Import करें

class StaticSitemap(Sitemap):
    """यह आपके स्टैटिक पेजेज (जो Menu में हैं) को Handle करेगा"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # ये 'name' आपके urls.py में दिए गए 'name=' पैरामीटर के हिसाब से हैं
        return [
            'home',       # मान लिया '/' का name='home' है
            'notes_list', # '/notes/' 
            'syllabus',   # '/syllabus/'
            'books',      # '/books/'
            'pyq_list',   # '/pyq/'
            'doubts',     # '/doubts/'
            'profile',    # '/profile/'
            'search'      # '/search/'
        ]

    def location(self, item):
        return reverse(item)  # Django खुद URL बना देगा


class DynamicFilterSitemap(Sitemap):
    """यह आपके Dynamic Filters (Branch + Semester) को Handle करेगा"""
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        # Database से सारी Unique Branches और Semesters निकालें
        # अगर Notes Model में 'branch' और 'semester' फील्ड हैं
        combos = Notes.objects.values('branch', 'semester').distinct().order_by('branch')
        return combos  # ये एक List of Dictionaries वापस आएगी

    def location(self, item):
        # item = {'branch': 'CS', 'semester': 5}
        return f"/notes/?branch={item['branch']}&semester={item['semester']}"

    # अगर आप PYQ के लिए अलग से चाहते हैं, तो एक और Class बना सकते हैं
    # या इसमें ही दोनों जोड़ दें।


class DetailSitemap(Sitemap):
    """अगर आपके पास नोट्स के Detail पेज हैं (जैसे /notes/1/) तो यह Use करें"""
    priority = 0.5
    changefreq = 'monthly'

    def items(self): 
        # सिर्फ 500 नोट्स तक सीमित रखें ताकि Sitemap बहुत बड़ा न हो
        return Notes.objects.all()[:500]

    def location(self, item):
        return f"/notes/{item.id}/"  # आपके URL Pattern के हिसाब से बदलें
    
    def lastmod(self, item):
        # अगर आपके पास 'updated_at' फील्ड है
        return item.updated_at