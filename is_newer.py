"""
functie is_newer(v1: str/int, v2: str/int) -> bool:
je moet asserts schrijven 2 IN 1 ->True
je moet asserts schrijven is 2,1 groter dan 1,2 -> True
2.1.1 > 2.1.0 -> True
2.1.1 > 10.1.1 -> False
1.b > 1.a -> True
1.b > 1.b -> True
1.b > 1.c -> False

"""
from unittest import result


def is_newer(v2: str or int, v1: str or int) -> bool:
    if not isinstance(v1, (str, int)):
        raise TypeError
    if not isinstance(v2, (str, int)):
        raise TypeError

    if type(v1)==int and type(v2)==int:
        if v2 >= v1:
            return True
        return False
    if type(v1)==str and type(v2)==str:
        v1 = v1.split('.')
        v2 = v2.split('.')
        result_v1 = []
        result_v2 = []
        for v,p in zip(v1,v2):
            if v.isdigit():
                result_v1.append(int(v))
            else:
                result_v1.append(v)
            if p.isdigit():
                result_v2.append(int(p))
            else:
                result_v2.append(p)
        result_v1 = tuple(result_v1)
        result_v2 = tuple(result_v2)
        if result_v1 == result_v2:
            raise AssertionError('v1 == v2')
        elif result_v1 < result_v2:
            return True

        return False

assert is_newer(2, 1) == True
assert is_newer('2.1', '1.2') == True
assert is_newer('2.1.1', '2.1.0') == True
assert is_newer('2.1.1', '12.1.1') == False
assert is_newer('2.b', '2.a') == True
