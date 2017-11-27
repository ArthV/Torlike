# @AUTHOR: Arthur Valingot
# @DATE: 27/11/2017
# This class defines a finite field operation. We actually use the representation and the mechanisms showed in the
# law.pdf page 125, in order to define the operation on GF(256) which is represented by Z/2Z/X^8+X^4+X^3+X+1
# This means that we use a polynomial representation, ie we use the operation addition and multiplication defined on
# the polynomial space, but the coefficient belong to the ring Z/2Z, ie the for i = 1 and j = 1 i + j = 0 mod 2
# To be sure that the multiplication of two polynomials will give an order greater than 7, we each time considering the
# remainder with the polynomial X^8+X^4+X^3+X+1

class FiniteField:
    def __init__(self, coeffs):
        #the bit are defined with str to be concatenate
        self.coeffs = coeffs

    def get_byte(self):
        str_a = ''
        for i in reversed(self.coeffs):
            str_a += str(i)
        return str_a

    def get_byte_string_from_coeffs(self, coeffs):
        str_a = ''
        for i in reversed(coeffs):
            str_a += str(i)
        return str_a

    @staticmethod
    def get_coeffs_from_int(byte):
        bin_str = bin(byte)[2:]
        coeffs = []
        for i in bin_str[::-1]:
            coeffs.append(int(i))

        return coeffs

    # In order to implement the division of an element of the Finite field, we look for the an other element
    # which belongs to to GF(256) and multiplied by the first element equals to 1 = 0*X^8+0*X^7+0*X^6 ... +0*X^1+1
    # which is the neutral element for the multiplication of the finite field.

    def __truediv__(self, other):
        for i in range(256):
            b = FiniteField(self.get_coeffs_from_int(i))
            if b * other == FiniteField([1]):
                return self * b

        return None

    def __mod__(self, other):
        higher_coef_other = 0
        higher_coef_self = 0
        byte_b = self.coeffs
        for i in reversed(range(len(other.coeffs))):
            if other.coeffs[i] == 1:
                higher_coef_other = i
                break

        for i in reversed(range(len(self.coeffs))):
            if self.coeffs[i] == 1:
                higher_coef_self = i
                break
        diff = higher_coef_self - higher_coef_other
        if diff < 0:
            return self
        while diff >= 0:
            coeffs = []
            for i in range(diff + 1):
                if i != diff:
                    coeffs.append(0)
                else:
                    coeffs.append(1)

            mul = self.mul(other.get_byte(), self.get_byte_string_from_coeffs(coeffs))
            byte_b = self.add(self.get_coeffs_from_int(mul), byte_b)

            for i in reversed(range(len(byte_b))):
                if byte_b[i] == 1:
                    higher_coef_add = i
                    break
            diff = higher_coef_add - higher_coef_other

        return FiniteField(byte_b)

    def __mul__(self, other):
        byte_a = int(self.get_byte(), 2)
        byte_b = other.get_byte()
        byte = 0

        for i in range(len(byte_b)):
            t = len(byte_b) - i - 1
            if byte_b[t] == '1':
                byte = byte ^ (byte_a << i)
        r = FiniteField(self.get_coeffs_from_int(byte)) % FiniteField([1, 1, 0, 1, 1, 0, 0, 0, 1])
        #FiniteField([1, 1, 0, 1, 1, 0, 0, 0, 1] this polynome is used to divide the value, we are in Z/2Z/X^8+X^4+X^3+X+1
        return r

    def mul(self, byte_a, byte_b):
        byte_a = int(byte_a, 2)
        byte = 0
        for i in range(len(byte_b)):
            t = len(byte_b) - i - 1
            if byte_b[t] == '1':
                byte = byte ^ (byte_a << i)
        return byte

    def add(self, coeffs1, coeffs2):
        coeffs = []
        max_len = max(len(coeffs1), len(coeffs2))
        for i in range(max_len):
            a = coeffs1[i] if i < len(coeffs1) else 0
            b = coeffs2[i] if i < len(coeffs2) else 0

            coeffs.append((a + b) % 2)

        return coeffs

    def __add__(self, other):
        coeffs = []
        max_len  = max(len(self.coeffs), len(other.coeffs))

        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            coeffs.append((a + b) % 2)

        return FiniteField(coeffs)

    def __eq__(self, other):
        max_len = max(len(self.coeffs), len(other.coeffs))
        answer = True
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            answer &= a == b
        return answer

    def __str__(self):
        return self.get_byte()