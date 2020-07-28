##אחמד טללקה-208900027  ו- ואסילה אלהואשלה -315589432
import math
import mmh3
from bitarray import bitarray


class BloomFilter(object):

    def __init__(self, size_count, size_hashs):
        self.dits = []
        self.c=0
        # False posible probability in decimal
        self.fp_prob = size_hashs
        # Size of bit array to use
        self.size = size_count
        # number of hash functions to use
        self.hash_count = size_hashs
        # Bit array of given size
        self.bit_array = bitarray(self.size)
        # initialize all bits as 0
        self.bit_array.setall(0)
        # currrent element count
        self.element_count = 0
        # maximum items in the filter (from input)
        self.max_num_of_items = size_count

    def get_marked_bits_count(self):
        return self.bit_array.count("1")

    def get_bit_array(self):
        return self.bit_array

    def add(self, item):
        self.c=0
        print(self.c)
        print("the is ",item)
        ''' 
        Add an item in the filter 
        '''
        self.dits.append(item)
        digests = []

        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)
            if self.bit_array[digest]:
              self.c=self.c+1
            self.bit_array[digest] = True
        self.element_count += 1
        print(self.c)
        print(digests)
        print(self.bit_array)

    def check(self,item):
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
                return False
        return True

    def get_element_count(self):
        '''
        Return element counter
        '''
        return self.element_count
    def check_if_add(self,item):
        if item in self.dits:
            return True
        return False


    def is_add_allowed(self):
        if (self.element_count < self.max_num_of_items):
            return True
        else:
            return False

    def set_max_num_of_items(self, m):
        self.max_num_of_items = m

    @classmethod
    def get_size(self, n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    def update_All_password(self):
        pass
