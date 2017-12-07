# @AUTHOR: Arthur Valingot
# @DATE: 27/11/2017
#This class implement the mathematical operation in order to manipulate a point with an Elliptic Curve
from FiniteField import FiniteField


class EllipticCurvePoint:
    def __init__(self, x, y, elliptic_curve):
        self.x = x
        self.y = y
        self.elliptic_curve = elliptic_curve

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.elliptic_curve == other.elliptic_curve

    def __add__(self, other):
        # According to CryptoAvance.pdf, we use the definition of the addition
        if self == -other:
            return EllipticCurveNeutralEl(self.elliptic_curve)
        elif self == other:
            v = self.x + self.y / self.x
            new_x = v * v + v + self.elliptic_curve.a
            new_y = new_x * new_x + v * new_x + new_x

            return EllipticCurvePoint(new_x, new_y, self.elliptic_curve)
        else:
            v = self.x + other.x
            z = (self.y + other.y)/v
            new_x = z*z + z + v + self.elliptic_curve.a
            new_y = (z + FiniteField([1]))*new_x + z*self.x + self.y

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
                v = self.x + self.y/self.x
                new_x = v * v + v + self.elliptic_curve.a
                new_y = new_x * new_x + v * new_x + new_x

                return EllipticCurvePoint(new_x, new_y, self.elliptic_curve)
            else:
                #the constant will be turn in binary as a string of 0 and 1
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
        return 'x :' + str(self.x) + '\n' + 'y:' + str(self.y)

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
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    # we want to work out the point of the elliptic curve for a given x
    # This function return x if the point x doesn't belong to the elliptic curve
    def workout_y(self, x):

        zero = FiniteField([0])
        beta = x * x * x + self.a * x * x + self.b

        for i in range(256):
            f = FiniteField(self.get_coeffs_from_int(i))
            if f * f + x * f + beta == zero:

                return f

        return None

    # this function is duplication and can be used in the finiteFiel
    # TODO: Create a static class which contains every method created in the code
    @staticmethod
    def get_coeffs_from_int(byte):
        bin_str = bin(byte)[2:]
        coeffs = []
        for i in bin_str[::-1]:
            coeffs.append(int(i))

        return coeffs