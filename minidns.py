import socket
import struct
import StringIO

# A request for jonathanj.com including transaction-id (first two bytes)
#data = "\x24\x9f\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x09\x6a\x6f\x6e\x61\x74\x68\x61\x6e\x6a\x03\x63\x6f\x6d\x00\x00\x01\x00\x01"
class DNSheader:
    def __init__(self):
        self.id = 0x1234
        self.bits = 0x0100
        self.qdCount = 0
        self.anCount = 0
        self.nsCount = 0
        self.arCount = 0
    def toBin(self):
        return struct.pack('!HHHHHH',
                        self.id,
                        self.bits,
                        self.qdCount,
                        self.anCount,
                        self.nsCount,
                        self.arCount);
    def fromBin(self,data):
        if data.read:
            data = data.read(12)
            (self.id,
             self.bits,
             self.qdCount,
             self.anCount,
             self.nsCount,
             self.arCount) = struct.unpack('!HHHHHH', data)
            return self
    def __repr__(self):
        return "Query ID %d, Questions: %d, Answers: %d" % (self.id, self.qdCount, self.anCount)

class BinReader(StringIO.StringIO):
    def unpack(self, fmt):
        size = struct.calcsize(fmt)
        bin = self.read(size)
        print bin.encode('hex')
        return struct.unpack(fmt, bin)

class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.host = ''
        reqtype = (ord(data[2]) >> 3) & 15   # Opcode bits
        #pdb.set_trace()
        print "reqtype: %d" % reqtype
        if reqtype == 0:  # Standard query
            ini = 12
            lon = ord(data[ini])
        while lon != 0:
            self.host += data[ini + 1:ini + lon + 1] + '.'
            ini += lon + 1
            lon = ord(data[ini])

    def dns_request(self, ip):
        packet = ''
        if self.host:
        #print self.host

            packet += self.data[:2] + "\x81\x80"
            packet += self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
            packet += self.data[12:]  # Original Domain Name Question
            packet += '\xc0\x0c'  # Pointer to domain name
            packet += '\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
            packet += str.join('', map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
            return packet


if __name__ == '__main__':
    resolution = {'zumahdistr.in.': '69.175.7.242', 'www.ip-adress.com.': '64.34.169.244',
                  'sqm.microsoft.com.': '65.55.7.141', 'forumity.com.': '103.246.248.135',
                  'positivtkn.in.ua.': '216.120.251.185', 'leavmauytdk.info.': '69.43.161.167',
                  'ichangasudskfoe.org.': '66.147.242.155', 'cupstuiakfuuasd.net.': '72.55.186.70',
                  'zoas.kiev.ua.': '72.55.186.66', 'olaum.kiev.ua.': '66.96.134.31', 'zemaucn.org.': '65.254.250.106',
                  'ww35.leavmauytdk.info.': '141.8.224.91', }
    usocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    usocket.bind(('', 53))

    try:
        print "Started."
        while 1:
            defaultip = "192.168.1.144"
            (data, addr) = usocket.recvfrom(1024)
            d = DNSheader()
            d.fromBin(BinReader(data))
            print d.__repr__()

            p = DNSQuery(data)
            if (p.host in resolution):
                print "Found matching host in resolution-table"
                usocket.sendto(p.dns_request(resolution[p.host]), addr)
                print 'Sent response: %s -> %s' % (p.host, resolution[p.host])
            else:
                usocket.sendto(p.dns_request(defaultip), addr)
                print 'Data: %s -> %s' % (p.host, defaultip)

    except KeyboardInterrupt:
        print 'End'
        usocket.close()