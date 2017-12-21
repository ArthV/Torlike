# @AUTHOR: Arthur Valingot
# @DATE: 27/11/2017

# This class implement the mathematical operation in order to manipulate a point with an Elliptic Curve

from FiniteField import FiniteField


class EllipticCurvePoint:
    def __init__(self, x, y, elliptic_curve):
        self.x = x
        self.y = y
        self.elliptic_curve = elliptic_curve

    def get_byte_string_from_coeffs(self):
        x_str = FiniteField.get_byte_string_from_coeffs(self.x.coeffs)
        y_str = FiniteField.get_byte_string_from_coeffs(self.y.coeffs)

        return str(int(x_str, 2)) + ':' + str(int(y_str, 2))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.elliptic_curve == other.elliptic_curve

    def __add__(self, other):
        # According to CryptoAvance.pdf, we use the definition of the addition
        # Erratum: These following formula come from the https://www.hyperelliptic.org/EFD/g12o/auto-shortw.html
        if self == -other:
            return EllipticCurveNeutralEl(self.elliptic_curve)
        elif self == other:
            alpha = self.x + self.y/self.x
            new_x = alpha * alpha + alpha + self.elliptic_curve.a
            new_y = alpha * alpha * alpha + (self.x + self.elliptic_curve.a + FiniteField([1])) * alpha + self.elliptic_curve.a + self.y

            return EllipticCurvePoint(new_x, new_y, self.elliptic_curve)
        else:
            R = (other.y + self.y)/(other.x + self.x)
            new_x = R * R + R + self.x + other.x + self.elliptic_curve.a
            new_y = R * R * R + (other.x + self.elliptic_curve.a + FiniteField([1]))*R + self.x + other.x + self.elliptic_curve.a + self.y

            return EllipticCurvePoint(new_x, new_y, self.elliptic_curve)

    def __radd__(self, other):
        if type(other) is EllipticCurveNeutralEl:
            return self

    def __neg__(self):
        return EllipticCurvePoint(self.x, self.x + self.y, self.elliptic_curve)

    def __rmul__(self, constant):
        # According to CryptoAvance, we implement the multiplication with a constant
        if type(constant) is int:
            if constant == 2:
                alpha = self.x + self.y / self.x
                new_x = alpha * alpha + alpha + self.elliptic_curve.a
                new_y = alpha * alpha * alpha + (self.x + self.elliptic_curve.a + FiniteField([1])) * alpha + self.elliptic_curve.a + self.y

                return EllipticCurvePoint(new_x, new_y, self.elliptic_curve)
            else:
                # the constant will be turn in binary as a string of 0 and 1
                cst_bin = bin(constant)[2:]
                q = EllipticCurveNeutralEl(self.elliptic_curve)

                # The following code will go through the string cst_bin
                for i in cst_bin:
                    q = q + q
                    if i == '1':
                        q = q + self

                return q
        else:
            raise NotImplementedError('Operator not implemented for this type of data')

    def __str__(self):
        return 'x:' + str(self.x) + '\n' + 'y:' + str(self.y)


# In order to have the good behaviour of the neutral element, The neutral element class is defined


class EllipticCurveNeutralEl:
    def __init__(self, elliptic_curve):
        self.elliptic_curve = elliptic_curve

    def __add__(self, other):
        if type(other) is EllipticCurvePoint:
            return other
        else:
            return self

    # The behaviour of the neutral element is not to change the value of the other element in the case of addition
    def __radd__(self, other):
        if type(other) is EllipticCurvePoint:
            return other
        else:
            raise NotImplementedError('This operator has to be used with an Elliptic Curve')

# In oder to implement the elliptic curve we use the following kind of Elliptic curve:
# y^2 + x*y = x^3 + a*x^2 + b
# This kind of elliptic curve is recommended in the document CryptoAvance.pdf


class EllipticCurve:
    def __init__(self, a, x, y):
        self.a = a
        self.x = x
        self.y = y

        self.b = None

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b
    # we want to work out the point of the elliptic curve for a given x
    # This function return x if the point x doesn't belong to the elliptic curve

    def workout_b(self):

        zero = FiniteField([0])
        beta = self.y * self.y + self.x * self.y + self.x * self.x * self.x + self.a * self.x * self.x

        for i in range(1, 256):
            b = FiniteField(self.get_coeffs_from_int(i))
            if beta + b == zero:
                self.b = b

    # this function is duplication and can be used in the finiteField
    # TODO: Create a static class which contains every method created in the code
    
    @staticmethod
    def get_coeffs_from_int(byte):
        bin_str = bin(byte)[2:]
        coeffs = []
        for i in bin_str[::-1]:
            coeffs.append(int(i))

        return coeffs