from FiniteField import FiniteField
from EllipticCurve import EllipticCurve, EllipticCurvePoint
from random import *


#
# a = FiniteField([0, 1, 1, 0, 1, 1, 0, 1])
# b = FiniteField([1, 1, 0, 0, 1, 0, 1])


c = FiniteField([1, 1, 1, 1])
a = FiniteField([1])
b = FiniteField([1, 0, 0, 1, 1, 1, 0, 1])
d = FiniteField([1, 1])
#
# for i in range(1, 256):
#     f = FiniteField(FiniteField.get_coeffs_from_int(i))
#     print(hex(int(str(a / f), 2)))


test = FiniteField([0])
print(a*test)


#
# print(hex(int(str(a/b), 2)))
# print(a*b)

# test = FiniteField([1, 1, 0, 1, 1, 0, 0, 0, 1]) % FiniteField([1, 1, 0, 1, 1, 0, 0, 0, 1])
# print(test)

#print(a + b)
# print(a*b)
# print(a == b)
# for i in range(256):
#     f = FiniteField(FiniteField.get_coeffs_from_int(i))
#     print(b/f)

# curve = EllipticCurve(a, b)
# print(a_1)
# print(b_1)
# print(a_1 * b_1)
# count = 0
# for i in range(256):
#     b = FiniteField(FiniteField.get_coeffs_from_int(i))
#     for j in range(256):
#         c = FiniteField(FiniteField.get_coeffs_from_int(j))
#         if b * c == FiniteField([1]):
#             print(b)
#             count += 1
# print(count)


# print('test')
#
# z = list(range(1, 256));
# print(shuffle(z))
# test = 0
# x = FiniteField([1, 1, 0, 0, 1, 1, 0, 1])
# for i in z:
#     b = FiniteField(EllipticCurve.get_coeffs_from_int(i))
#     z = curve.workout_y(b)
#     if type(z) is FiniteField:
#         p = EllipticCurvePoint(b, z, curve)
#         break

# Let's find a good eliptic curve coefficient
x = FiniteField([randint(0, 1) for i in range(7)])
y = FiniteField([randint(0, 1) for i in range(7)])
a = FiniteField([randint(0, 1) for i in range(7)])
# x = FiniteField([1, 1])
# y = FiniteField([1, 0, 1])
# a = FiniteField([1])
# let's define the elliptic curve
curve = EllipticCurve(a, x, y)

# Let's find a point which belong to the elliptical curve


curve.workout_b()

print(curve.b)
p = EllipticCurvePoint(x, y, curve)
# p = FiniteField([1, 1, 1, 0, 1, 1, 1])
# print('-P')
# print(-p)
x = 1800*p
y = 1344*p
A = 1344*x
B = 1800*y
print(A)
print(B)

print(A==B)

#
# b
# 11010110
# z
# 100101
#
# b
# 11011011
# z
# 111100
#
# b
# 11011111
# z
# 101000
# b
# 11100000
# z
# 101111