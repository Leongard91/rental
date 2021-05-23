import re

filters = '[Cars,Trailers,Special Equipment,Agricultural Machinery,Buses,Air Transport]'
filters = re.findall(r'(\W+.?)?,', filters)
print(filters)