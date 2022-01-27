import urllib3
import sys
import re
http = urllib3.PoolManager()

base_url = "http://library.bracu.ac.bd:9292/cgi-bin/koha/"
#login = {'userid' : '', 'password': ''}

userid = input("Enter Userid: ")
password = input("Password: ")
login = {'userid' : userid , 'password': password}

login_req = http.request('POST', base_url+"opac-user.pl", fields=login)
if not login_req.status==200:
  print("Error Occurred during Login.\nPlease Check Your login detail and network connection")
  sys.exit(0)
login_header = {'cookie': login_req.getheader('set-cookie')}
raw_html = login_req.data.decode("utf-8")

wrong_login_pattern = re.compile(r'You entered an incorrect username or password')
match_result = wrong_login_pattern.findall(raw_html)
if not match_result :
  print("Login  Successfull !!")
else:
  print("You entered an incorrect username or password")
  sys.exit(0)

renew_urls_pattern = re.compile(r'(opac-renew.pl\?from=opac_user&amp;item=\d+&amp;borrowernumber=\d+)')
renew_urls = renew_urls_pattern.findall(raw_html)
for i, url in enumerate(renew_urls):
  renew_req = http.request('GET', base_url+url, headers=login_header)
  if renew_req.status == 200:
    print(f"Book {i+1}: Renewed")
  else:
    print('Error During Renew Process')
