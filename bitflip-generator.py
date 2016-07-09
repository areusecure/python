tlds = ['ac','ad','ae','aero','af','ag','ai','al','am','an','ao','aq','ar','arpa','as','asia','at','au','aw','ax','az','ba','bb','bd','be','bf','bg','bh','bi','biz','bj','bm','bn','bo','br','bs','bt','bv','bw','by','bz','ca','cat','cc','cd','cf','cg','ch','ci','ck','cl','cm','cn','co','com','coop','cr','cu','cv','cw','cx','cy','cz','de','dj','dk','dm','do','dz','ec','edu','ee','eg','er','es','et','eu','fi','fj','fk','fm','fo','fr','ga','gb','gd','ge','gf','gg','gh','gi','gl','gm','gn','gov','gp','gq','gr','gs','gt','gu','gw','gy','hk','hm','hn','hr','ht','hu','id','ie','il','im','in','info','int','io','iq','ir','is','it','je','jm','jo','jobs','jp','ke','kg','kh','ki','km','kn','kp','kr','kw','ky','kz','la','lb','lc','li','lk','lr','ls','lt','lu','lv','ly','ma','mc','md','me','mg','mh','mil','mk','ml','mm','mn','mo','mobi','mp','mq','mr','ms','mt','mu','museum','mv','mw','mx','my','mz','na','name','nc','ne','net','nf','ng','ni','nl','no','np','nr','nu','nz','om','org','pa','pe','pf','pg','ph','pk','pl','pm','pn','post','pr','pro','ps','pt','pw','py','qa','re','ro','rs','ru','rw','sa','sb','sc','sd','se','sg','sh','si','sj','sk','sl','sm','sn','so','sr','st','su','sv','sx','sy','sz','tc','td','tel','tf','tg','th','tj','tk','tl','tm','tn','to','tp','tr','travel','tt','tv','tw','tz','ua','ug','uk','us','uy','uz','va','vc','ve','vg','vi','vn','vu','wf','ws','xn--3e0b707e','xn--45brj9c','xn--80ao21a','xn--80asehdb','xn--80aswg','xn--90a3ac','xn--clchc0ea0b2g2a9gcd','xn--fiqs8s','xn--fiqz9s','xn--fpcrj9c3d','xn--fzc2c9e2c','xn--gecrj9c','xn--h2brj9c','xn--j1amh','xn--j6w193g','xn--kprw13d','xn--kpry57d','xn--l1acc','xn--lgbbat1ad8j','xn--mgb9awbf','xn--mgba3a4f16a','xn--mgbaam7a8h','xn--mgbayh7gpa','xn--mgbbh1a71e','xn--mgbc0a9azcg','xn--mgberp4a5d4ar','xn--mgbx4cd0ab','xn--ngbc5azd','xn--o3cw4h','xn--ogbpf8fl','xn--p1ai','xn--pgbs0dh','xn--s9brj9c','xn--unup4y','xn--wgbh1c','xn--wgbl6a','xn--xkc2al3hye2a','xn--xkc2dl3a5ee0h','xn--yfro4i67o','xn--ygbi2ammx','xxx','ye','yt','za','zm','zw']

# variable, replacement,index
def replace_char(src,replacement,index):
    src = str(src)
    replacement = str(replacement)[0]
    return_s = ''
    size = len(src)
    i = 0
    while(i != index and (i < size)):
        return_s += src[i]
        i+=1

    return_s += replacement
    return_s += src[(i+1):]
    return return_s

def i2b(value):
    return int(value,2)

def b2i(binvalue):
   return int(binvalue,2)

def isallowed(char):
    # -
    if b2i(char) == 45 or b2i(char) == 46:
        return True
    # A-Z
    elif b2i(char) > 64 and b2i(char) < 91:
        return True
    # a-z
    elif b2i(char) > 96 and b2i(char) < 123:
        return True
    else:
        return False

def flipit(bit):
    bit = int(bit)
    return(bit ^ (1 << 0))

def check_bitflips(byte):
	alternatives = []
	binr = str(bin(ord(byte))[2:])
	i=0
	while (i<len(binr)):
		newbin = replace_char(binr,flipit(binr[i]),i)
		if(isallowed(newbin)):
			alternatives.append(str(chr(b2i(newbin))))
		i += 1
	return alternatives
	
def main():
	alternative_bytes = []
	alternative_dns = []
	dns = "gstatic.com"
	index = 0
	while(index < len(dns)):
		alternative_bytes = check_bitflips(dns[index])
		for entry in alternative_bytes:
			new_dns = replace_char(dns,entry,index).lower()
			if new_dns not in alternative_dns:
				alternative_dns.append(new_dns)
		index += 1
	
	for dnsentry in alternative_dns:
		tld = dnsentry.split(".").pop()
		if tld in tlds:
			print dnsentry
	
	
if __name__ == '__main__':
	main()