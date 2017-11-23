from FiniteField import FiniteField
from EllipticCurve import EllipticCurve, EllipticCurvePoint

a = FiniteField([0, 1, 0, 0, 1, 1])
b = FiniteField([1, 0, 0, 1])
#print(a + b)
# print(a*b)
# print(a == b)
# for i in range(256):
#     f = FiniteField(FiniteField.get_coeffs_from_int(i))
#     print(b/f)

curve = EllipticCurve(a, b)

a_1 = FiniteField(FiniteField.get_coeffs_from_int(0x2))
b_1 = FiniteField(FiniteField.get_coeffs_from_int(0x8d))
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
# x = FiniteField([1, 1, 0, 0, 1, 1, 0, 1])
# for i in range(256):
#     b = FiniteField(x.get_coeffs_from_int(i))
#     z = curve.workout_y(b)
#     print('b')
#     print(b)
#     print('z')
#     print(z)

p = EllipticCurvePoint(FiniteField([0, 1, 1, 0, 1, 0, 1, 1]), FiniteField([1, 0, 1, 0, 0, 1]), curve)

print(p)
print(-p)
print(10*p)


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