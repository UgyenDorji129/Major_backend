import re
import urllib.parse
import tldextract

def length_url(url):
    return len(url) 

def length_hostname(url):
    parsed_url = urllib.parse.urlparse(url)
    length = len(parsed_url.netloc)
    return length

def ip(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)|'  # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '[0-9a-fA-F]{7}', url)  # Ipv6
    if match:
        return 1
    else:
        return 0

def nb_dots(url):
    return url.count(".")

def nb_hyphens(url):
    return url.count("-")

def nb_at(url):
    return url.count("@")

def nb_qm(url):
    return url.count("?")

def nb_and(url):
    return url.count("&")

def nb_and(url):
    return url.count("|")

def nb_eq(url):
    return url.count("=")

def nb_underscore(url):
    return url.count("_")

def nb_tilde(url):
    return url.count("~")

def nb_percent(url):
    return url.count("%")

def nb_slash(url):
    return url.count("/")

def nb_star(url):
    return url.count("*")

def nb_colon(url):
    return url.count(":")

def nb_comma(url):
    return url.count(",")

def nb_semicolumn(url):
    return url.count(";")

def nb_dollar(url):
    return url.count("$")

def nb_space(url):
    return url.count(" ")

def nb_www(url):
    return url.count("www")

def nb_com(url):
    return url.count("com")

def nb_dslash(url):
    return url.count("//")

def http_in_path(url):
    return url.count("http")

def https_token(url):
    return url.count("https")

def ratio_digits_url(url):
    return len(re.sub("[^0-9]", "", url))/len(url)

def ratio_digits_host(url):
    return len(re.sub("[^0-9]", "", url))/len(urllib.parse.urlparse(url).netloc)

def punycode(url):
    if url.startswith("http://xn--") or url.startswith("http://xn--"):
        return 1
    else:
        return 0

def port(url):
    if re.search("^[a-z][a-z0-9+\-.]*://([a-z0-9\-._~%!$&'()*+,;=]+@)?([a-z0-9\-._~%]+|\[[a-z0-9\-._~%!$&'()*+,;=:]+\]):([0-9]+)",url):
        return 1
    return 0
   
def tld_in_path(url):
    tld = tldextract.extract(url).suffix
    delimiters = "/:?&=#@;-_@."
    for delimiter in delimiters:
        url = url.replace(delimiter, ",")
    new = url.split(",")
    if(new.count(tld) >= 2):
        return 0
    return 1

def tld_in_subdomain(url):
    subdomain = tldextract.extract(url).subdomain
    if '.' in subdomain:
        subdomains = subdomain.split('.')
        for sub in subdomains:
            tld = tldextract.extract(sub).suffix
            if tld is not None and tld != '':
                return 1
    else:
        tld = tldextract.extract(subdomain).suffix
        if tld is not None and tld != '':
            return 1

    return 0

def abnormal_subdomain(url):
    if tld_in_path(url)== 1 or tld_in_subdomain(url)==1:
        return 1
    return 0

def nb_subdomains(url):
    if len(re.findall("\.", url)) == 1:
        return 1
    elif len(re.findall("\.", url)) == 2:
        return 2
    else:
        return 3
    
def prefix_suffix(url):
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        return 1
    else:
        return 0 
    
def random_domain(url):
    pattern = r'^[a-z0-9]{10,}$' # matches any string of at least 10 lowercase letters or digits
    ans =  bool(re.match(pattern, url))
    if(ans):
        return 1
    return 0

def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0

def path_extension(url):
    if url.endswith('.txt'):
        return 1
    return 0

import urllib.request
def nb_redirection(url):
    
    response = urllib.request.urlopen(url)
    return len(response.geturl().split('https://example.com')) - 1

print(nb_redirection("http://www.crestonwood.com/router.php"))