#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

def generate_pins(length, count, alphabet=string.digits):
    alphabet = ''.join(set(alphabet))
    if count > len(alphabet)**length:
        raise ValueError("Can't generate more than %s > %s pins of length %d out of %r" %
                      count, len(alphabet)**length, length, alphabet)
    def onepin(length):
        return ''.join(random.choice(alphabet) for x in xrange(length))
    result = set(onepin(length) for x in xrange(count))
    while len(result) < count:
        result.add(onepin(length))
    return list(result)
    

print generate_pins(10,1)