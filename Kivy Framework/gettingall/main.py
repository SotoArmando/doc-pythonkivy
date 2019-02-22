import urllib2
from BeautifulSoup import BeautifulSoup
response = urllib2.urlopen('https://www.mybobs.com/living-room-furniture/living-room-sets')
html = response.read()
print html



html = html[str(html).find("<!--------------- FIVE9 CHAT CODE END----->"):]
soup = BeautifulSoup(html)
#x = soup.body.find('script', attrs={'type' : "text/javascript"}).text
pos1 = html.find("staticImpressions['product_list'] = [")
pos2 = html[pos1:].find("</script>")
print pos1,pos2
print html[pos1:(pos1+pos2)]
staticImpressions = {}
exec(html[pos1:(pos1+pos2)])
#losdatos = html[pos1:(pos1+pos2)][len("staticImpressions['product_list'] = ["):]
print staticImpressions['product_list'][0]