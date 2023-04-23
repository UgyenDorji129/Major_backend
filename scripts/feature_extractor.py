from scripts import content_features as ctnfe
from scripts import url_features as urlfe
from scripts import external_features as trdfe
import urllib.parse
import tldextract
import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

key = 'wg8g8csw8csg8oog8osokk00s4oc84woockgow0k'

import signal

# class TimedOutExc(Exception):
#     pass

# def deadline(timeout, *args):
#     def decorate(f):
#         def handler(signum, frame):
#             raise TimedOutExc()

#         def new_f(*args):
#             signal.signal(signal.SIGALRM, handler)
#             signal.alarm(timeout)
#             return f(*args)
#             signal.alarm(0)

#         new_f.__name__ = f.__name__
#         return new_f
#     return decorate


def is_URL_accessible(url):
    print(url)
    page = None
    print(url)
    try:
        page =  requests.get(url, timeout=5) 
        print("Page: ",page)  
    except:
        parsed = urlparse(url)
        url = parsed.scheme+'://'+parsed.netloc
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme+'://www.'+parsed.netloc
            try:
                page =  requests.get(url, timeout=5)
            except:
                page = None
                pass
    if page and page.status_code == 200 and page.content not in ["b''", "b' '"]:
        return True, url, page
    else:
        return False, None, None

def get_domain(url):
    o =urllib.parse.urlsplit(url)
    return o.hostname, tldextract.extract(url).domain, o.path


def getPageContent(url):
    # parsed = urlparse(url)
    # url = parsed.scheme+'://'+parsed.netloc
    # try:
    #     page = requests.get(url)
    # except:
    #     if not parsed.netloc.startswith('www'):
    #         url = parsed.scheme+'://www.'+parsed.netloc
    #         page = requests.get(url)
    # if page.status_code != 200:
    #     return None, None
    # else:    
    #     return url, page.content
    parsed = urlparse(url)
    url = f"{parsed.scheme}://{parsed.netloc}"
    try:
        page = requests.get(url)
        if not page.ok and not parsed.netloc.startswith('www'):
            url = f"{parsed.scheme}://www.{parsed.netloc}"
            page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

    if not page.ok:
        return None, None
    else:
        return url, page.content
 
    
    
#################################################################################################################################
#              Data Extraction Process
#################################################################################################################################

def extract_data_from_URL(hostname, content, domain, Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text):
    Null_format = ["", "#", "#nothing", "#doesnotexist", "#null", "#void", "#whatever",
               "#content", "javascript::void(0)", "javascript::void(0);", "javascript::;", "javascript"]

    soup = BeautifulSoup(content, 'html.parser', from_encoding='iso-8859-1')

    # collect all external and internal hrefs from url
    for href in soup.find_all('a', href=True):
        dots = [x.start(0) for x in re.finditer('\.', href['href'])]
        if hostname in href['href'] or domain in href['href'] or len(dots) == 1 or not href['href'].startswith('http'):
            if "#" in href['href'] or "javascript" in href['href'].lower() or "mailto" in href['href'].lower():
                 Anchor['unsafe'].append(href['href']) 
            if not href['href'].startswith('http'):
                if not href['href'].startswith('/'):
                    Href['internals'].append(hostname+'/'+href['href']) 
                elif href['href'] in Null_format:
                    Href['null'].append(href['href'])  
                else:
                    Href['internals'].append(hostname+href['href'])   
        else:
            Href['externals'].append(href['href'])
            Anchor['safe'].append(href['href'])

    # collect all media src tags
    for img in soup.find_all('img', src=True):
        dots = [x.start(0) for x in re.finditer('\.', img['src'])]
        if hostname in img['src'] or domain in img['src'] or len(dots) == 1 or not img['src'].startswith('http'):
            if not img['src'].startswith('http'):
                if not img['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+img['src']) 
                elif img['src'] in Null_format:
                    Media['null'].append(img['src'])  
                else:
                    Media['internals'].append(hostname+img['src'])   
        else:
            Media['externals'].append(img['src'])
           
    
    for audio in soup.find_all('audio', src=True):
        dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
        if hostname in audio['src'] or domain in audio['src'] or len(dots) == 1 or not audio['src'].startswith('http'):
             if not audio['src'].startswith('http'):
                if not audio['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+audio['src']) 
                elif audio['src'] in Null_format:
                    Media['null'].append(audio['src'])  
                else:
                    Media['internals'].append(hostname+audio['src'])   
        else:
            Media['externals'].append(audio['src'])
            
    for embed in soup.find_all('embed', src=True):
        dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
        if hostname in embed['src'] or domain in embed['src'] or len(dots) == 1 or not embed['src'].startswith('http'):
             if not embed['src'].startswith('http'):
                if not embed['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+embed['src']) 
                elif embed['src'] in Null_format:
                    Media['null'].append(embed['src'])  
                else:
                    Media['internals'].append(hostname+embed['src'])   
        else:
            Media['externals'].append(embed['src'])
           
    for i_frame in soup.find_all('iframe', src=True):
        dots = [x.start(0) for x in re.finditer('\.', i_frame['src'])]
        if hostname in i_frame['src'] or domain in i_frame['src'] or len(dots) == 1 or not i_frame['src'].startswith('http'):
            if not i_frame['src'].startswith('http'):
                if not i_frame['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+i_frame['src']) 
                elif i_frame['src'] in Null_format:
                    Media['null'].append(i_frame['src'])  
                else:
                    Media['internals'].append(hostname+i_frame['src'])   
        else: 
            Media['externals'].append(i_frame['src'])
           

    # collect all link tags
    for link in soup.findAll('link', href=True):
        dots = [x.start(0) for x in re.finditer('\.', link['href'])]
        if hostname in link['href'] or domain in link['href'] or len(dots) == 1 or not link['href'].startswith('http'):
            if not link['href'].startswith('http'):
                if not link['href'].startswith('/'):
                    Link['internals'].append(hostname+'/'+link['href']) 
                elif link['href'] in Null_format:
                    Link['null'].append(link['href'])  
                else:
                    Link['internals'].append(hostname+link['href'])   
        else:
            Link['externals'].append(link['href'])

    for script in soup.find_all('script', src=True):
        dots = [x.start(0) for x in re.finditer('\.', script['src'])]
        if hostname in script['src'] or domain in script['src'] or len(dots) == 1 or not script['src'].startswith('http'):
            if not script['src'].startswith('http'):
                if not script['src'].startswith('/'):
                    Link['internals'].append(hostname+'/'+script['src']) 
                elif script['src'] in Null_format:
                    Link['null'].append(script['src'])  
                else:
                    Link['internals'].append(hostname+script['src'])   
        else:
            Link['externals'].append(link['href'])
           
            
    # collect all css
    for link in soup.find_all('link', rel='stylesheet'):
        dots = [x.start(0) for x in re.finditer('\.', link['href'])]
        if hostname in link['href'] or domain in link['href'] or len(dots) == 1 or not link['href'].startswith('http'):
            if not link['href'].startswith('http'):
                if not link['href'].startswith('/'):
                    CSS['internals'].append(hostname+'/'+link['href']) 
                elif link['href'] in Null_format:
                    CSS['null'].append(link['href'])  
                else:
                    CSS['internals'].append(hostname+link['href'])   
        else:
            CSS['externals'].append(link['href'])
    
    for style in soup.find_all('style', type='text/css'):
        try: 
            start = str(style[0]).index('@import url(')
            end = str(style[0]).index(')')
            css = str(style[0])[start+12:end]
            dots = [x.start(0) for x in re.finditer('\.', css)]
            if hostname in css or domain in css or len(dots) == 1 or not css.startswith('http'):
                if not css.startswith('http'):
                    if not css.startswith('/'):
                        CSS['internals'].append(hostname+'/'+css) 
                    elif css in Null_format:
                        CSS['null'].append(css)  
                    else:
                        CSS['internals'].append(hostname+css)   
            else: 
                CSS['externals'].append(css)
        except:
            continue
            
    # collect all form actions
    for form in soup.findAll('form', action=True):
        dots = [x.start(0) for x in re.finditer('\.', form['action'])]
        if hostname in form['action'] or domain in form['action'] or len(dots) == 1 or not form['action'].startswith('http'):
            if not form['action'].startswith('http'):
                if not form['action'].startswith('/'):
                    Form['internals'].append(hostname+'/'+form['action']) 
                elif form['action'] in Null_format or form['action'] == 'about:blank':
                    Form['null'].append(form['action'])  
                else:
                    Form['internals'].append(hostname+form['action'])   
        else:
            Form['externals'].append(form['action'])
            

    # collect all link tags
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
            if hostname in head.link['href'] or len(dots) == 1 or domain in head.link['href'] or not head.link['href'].startswith('http'):
                if not head.link['href'].startswith('http'):
                    if not head.link['href'].startswith('/'):
                        Favicon['internals'].append(hostname+'/'+head.link['href']) 
                    elif head.link['href'] in Null_format:
                        Favicon['null'].append(head.link['href'])  
                    else:
                        Favicon['internals'].append(hostname+head.link['href'])   
            else:
                Favicon['externals'].append(head.link['href'])
                
        for head.link in soup.findAll('link', {'href': True, 'rel':True}):
            isicon = False
            if isinstance(head.link['rel'], list):
                for e_rel in head.link['rel']:
                    if (e_rel.endswith('icon')):
                        isicon = True
            else:
                if (head.link['rel'].endswith('icon')):
                    isicon = True
       
            if isicon:
                 dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                 if hostname in head.link['href'] or len(dots) == 1 or domain in head.link['href'] or not head.link['href'].startswith('http'):
                     if not head.link['href'].startswith('http'):
                        if not head.link['href'].startswith('/'):
                            Favicon['internals'].append(hostname+'/'+head.link['href']) 
                        elif head.link['href'] in Null_format:
                            Favicon['null'].append(head.link['href'])  
                        else:
                            Favicon['internals'].append(hostname+head.link['href'])   
                 else:
                     Favicon['externals'].append(head.link['href'])
                     
                    
    # collect i_frame
    for i_frame in soup.find_all('iframe', width=True, height=True, frameborder=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['frameborder'] == "0":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
    for i_frame in soup.find_all('iframe', width=True, height=True, border=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['border'] == "0":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
    for i_frame in soup.find_all('iframe', width=True, height=True, style=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['style'] == "border:none;":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
          
    # get page title
    try:
        Title = soup.title.string
        if(soup.title.string == None):
            Title = " "
        
    except:
        
        pass
    
    # get content text
    Text = soup.get_text()
    
    return Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text




#################################################################################################################################
#              Calculate features from extracted data
#################################################################################################################################


def extract_features(url):
    
    def words_raw_extraction(domain, subdomain, path):
        w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
        w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())   
        w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())
        raw_words = w_domain + w_path + w_subdomain
        w_host = w_domain + w_subdomain
        raw_words = list(filter(None,raw_words))
        return raw_words, list(filter(None,w_host)), list(filter(None,w_path))

    
    Href = {'internals':[], 'externals':[], 'null':[]}
    Link = {'internals':[], 'externals':[], 'null':[]}
    Anchor = {'safe':[], 'unsafe':[], 'null':[]}
    Media = {'internals':[], 'externals':[], 'null':[]}
    Form = {'internals':[], 'externals':[], 'null':[]}
    CSS = {'internals':[], 'externals':[], 'null':[]}
    Favicon = {'internals':[], 'externals':[], 'null':[]}
    IFrame = {'visible':[], 'invisible':[], 'null':[]}
    Title =''
    Text= ''
    state, iurl, page = is_URL_accessible(url)
    if state:
        content = page.content
        hostname, domain, path = get_domain(url)
        extracted_domain = tldextract.extract(url)
        domain = extracted_domain.domain+'.'+extracted_domain.suffix
        subdomain = extracted_domain.subdomain
        tmp = url[url.find(extracted_domain.suffix):len(url)]
        pth = tmp.partition("/")
        path = pth[1] + pth[2]
        words_raw, words_raw_host, words_raw_path= words_raw_extraction(extracted_domain.domain, subdomain, pth[2])
        tld = extracted_domain.suffix
        parsed = urlparse(url)
        scheme = parsed.scheme
        
        Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text = extract_data_from_URL(hostname, content, domain, Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text)

        row = [
               # url-based features
               urlfe.url_length(url),
               urlfe.url_length(hostname),
               urlfe.having_ip_address(url),
               urlfe.count_dots(url),
               urlfe.count_hyphens(url),
               urlfe.count_at(url),
               urlfe.count_exclamation(url),
               urlfe.count_and(url),
               urlfe.count_or(url),
               urlfe.count_equal(url),
               urlfe.count_underscore(url),
               urlfe.count_tilde(url),
               urlfe.count_percentage(url),
               urlfe.count_slash(url),
               urlfe.count_star(url),
               urlfe.count_colon(url),
               urlfe.count_comma(url),
               urlfe.count_semicolumn(url),
               urlfe.count_dollar(url),
               urlfe.count_space(url),
               
               urlfe.check_www(words_raw),
               urlfe.check_com(words_raw),
               urlfe.count_double_slash(url),
               urlfe.count_http_token(path),
               urlfe.https_token(scheme),
               
               urlfe.ratio_digits(url),
               urlfe.ratio_digits(hostname),
               urlfe.punycode(url),
               urlfe.port(url),
               urlfe.tld_in_path(tld, path),
               urlfe.tld_in_subdomain(tld, subdomain),
               urlfe.abnormal_subdomain(url),
               urlfe.count_subdomain(url),
               urlfe.prefix_suffix(url),
               urlfe.random_domain(domain),
               urlfe.shortening_service(url),
               
               
               urlfe.path_extension(path),
               urlfe.count_redirection(page),
               urlfe.count_external_redirection(page, domain),
               urlfe.length_word_raw(words_raw),
               urlfe.char_repeat(words_raw),
               urlfe.shortest_word_length(words_raw),
               urlfe.shortest_word_length(words_raw_host),
               urlfe.shortest_word_length(words_raw_path),
               urlfe.longest_word_length(words_raw),
               urlfe.longest_word_length(words_raw_host),
               urlfe.longest_word_length(words_raw_path),
               urlfe.average_word_length(words_raw),
               urlfe.average_word_length(words_raw_host),
               urlfe.average_word_length(words_raw_path),
               
               urlfe.phish_hints(url),  
               urlfe.domain_in_brand(extracted_domain),
               urlfe.brand_in_path(extracted_domain,subdomain),
               urlfe.brand_in_path(extracted_domain,path),
               urlfe.suspecious_tld(tld),
               urlfe.statistical_report(url, domain),

               
               # # # content-based features
                 ctnfe.nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon),
                 ctnfe.internal_hyperlinks(Href, Link, Media, Form, CSS, Favicon),
                 ctnfe.external_hyperlinks(Href, Link, Media, Form, CSS, Favicon),
                 ctnfe.null_hyperlinks(hostname, Href, Link, Media, Form, CSS, Favicon),
                 ctnfe.external_css(CSS),
                 ctnfe.internal_redirection(Href, Link, Media, Form, CSS, Favicon),
                 ctnfe.external_redirection(Href, Link, Media, Form, CSS, Favicon),
                 ctnfe.internal_errors(Href, Link, Media, Form, CSS, Favicon),
                 ctnfe.external_errors(Href, Link, Media, Form, CSS, Favicon),
                 ctnfe.login_form(Form),
                 ctnfe.external_favicon(Favicon),
                 ctnfe.links_in_tags(Link),
                 ctnfe.submitting_to_email(Form),
                 ctnfe.internal_media(Media),
                 ctnfe.external_media(Media),
               #  # additional content-based features
                 ctnfe.sfh(hostname,Form),
                 ctnfe.iframe(IFrame),
                 ctnfe.popup_window(Text),
                 ctnfe.safe_anchor(Anchor),
                 ctnfe.onmouseover(Text),
                 ctnfe.right_clic(Text),
                 ctnfe.empty_title(Title),
                 ctnfe.domain_in_title(extracted_domain, Title),
                 ctnfe.domain_with_copyright(extracted_domain, Text),
                 
                # # # thirs-party-based features
                 trdfe.whois_registered_domain(domain),
                 trdfe.domain_registration_length(domain),
                 trdfe.domain_age(domain),
                 trdfe.web_traffic(url),
                 trdfe.dns_record(domain),
                 trdfe.google_index(url),
                 trdfe.page_rank(key,domain),
               # status
               ]
        #print(row)
        return row
    return None



#################################################################################################################################
#             Intialization
#################################################################################################################################



ctn_headers = [
                   'nb_hyperlinks', 
                   'ratio_intHyperlinks',
                   'ratio_extHyperlinks', 
                   'ratio_nullHyperlinks',
                   'nb_extCSS',
                   'ratio_intRedirection',
                   'ratio_extRedirection',
                   'ratio_intErrors',
                   'ratio_extErrors',
                   'login_form', 
                   'external_favicon',
                   'links_in_tags',
                   'submit_email', 
                   'ratio_intMedia',
                   'ratio_extMedia',
                   'sfh',
                   'iframe',
                   'popup_window',
                   'safe_anchor', 
                   'onmouseover',
                   'right_clic',
                   'empty_title', 
                   'domain_in_title',
                   'domain_with_copyright',
                                       
                ]


    
url_headers = [    'length_url',                                  
                   'length_hostname',
                   'ip',
                   'nb_dots',
                   'nb_hyphens',
                   'nb_at',
                   'nb_qm',
                   'nb_and',
                   'nb_or',
                   'nb_eq',                  
                   'nb_underscore',
                   'nb_tilde',
                   'nb_percent',
                   'nb_slash',
                   'nb_star',
                   'nb_colon',
                   'nb_comma',
                   'nb_semicolumn',
                   'nb_dollar',
                   'nb_space',
                   'nb_www',
                   'nb_com',
                   'nb_dslash',
                   'http_in_path',
                   'https_token',
                   'ratio_digits_url',
                   'ratio_digits_host',
                   'punycode',
                   'port',
                   'tld_in_path',
                   'tld_in_subdomain',
                   'abnormal_subdomain',
                   'nb_subdomains',
                   'prefix_suffix',
                   'random_domain',
                   'shortening_service',
                   'path_extension',
                   
                   'nb_redirection',
                   'nb_external_redirection',
                   'length_words_raw',
                   'char_repeat',
                   'shortest_words_raw',
                   'shortest_word_host',
                   'shortest_word_path',
                   'longest_words_raw',
                   'longest_word_host',
                   'longest_word_path',
                   'avg_words_raw',
                   'avg_word_host',
                   'avg_word_path',
                   'phish_hints',
                   'domain_in_brand',
                   'brand_in_subdomain',
                   'brand_in_path',
                   'suspecious_tld',
                   'statistical_report'

                ]



tpt_headers = [
                   'whois_registered_domain',
                   'domain_registration_length',
                   'domain_age', 
                   'web_traffic',
                   'dns_record',
                   'google_index',
                   'page_rank'
                ]


headers = url_headers + ctn_headers + tpt_headers

