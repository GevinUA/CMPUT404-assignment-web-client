import urllib.parse


args = {'a':'aaaaaaaaaaaaa',
                'b':'bbbbbbbbbbbbbbbbbbbbbb',
                'c':'c',
                'd':'012345\r67890\n2321321\n\r'}
o = urllib.parse.urlencode(args)                
print(o)