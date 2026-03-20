# Approximation polynomial root finder !
# By Jesse M, 30/05/2025

# This program approximates the roots of any length polynomial - a curious
# problem for which me and my friend Sean designed the algorithm for, and
# I implemented.

# default offset for outer roots of polynomial
STD_OFST = 1
# max iterations for newton's method.
MAX_ITERS = 99999
# decimal place precision value
DP_PRECISION = 4

class Polynomial:
    def __init__(self, coeffs=[]):
        # From lowest order to highest - e.g. 1 + x + x^2 + x^3 + ...
        self.set_info(coeffs)
        
    def set_info(self, coeffs):
        # If the highest degree term has coefficient 0, then remove that term.
        while coeffs and coeffs[-1] == 0:
            coeffs.pop(-1)

        self.coeffs = coeffs
        self.deg = len(coeffs) - 1

    def prompt_coeffs(self):
        coeffs = []
        exp = 0

        while True:
            print(f"Input the x^{exp} coefficient as a float. Input nothing to stop.")
            inp = input(" > ")

            if not inp:
                break
            
            try:
                num = float(inp)
                coeffs.append(num)
            except:
                print("Error - Try again.")
                print()

            exp += 1

        self.set_info(coeffs)
    
    def print_poly(self):
        terms = []
        for exp, coeff in enumerate(self.coeffs):
            if coeff != 0:
                if exp == 0:
                    terms.append(f"{coeff}")
                elif exp == 1:
                    terms.append(f"{coeff}x")
                else:
                    terms.append(f"{coeff}x^{exp}")

        print(" + ".join(terms[::-1]))

    def print_roots(self):
        roots = self.get_roots()

        if roots == []:
            print("No roots.")

        for r in roots:
            print(f"x = {round(r, DP_PRECISION):.{DP_PRECISION}f}")

    def f(self, x):
        total = 0
        for exp, coeff in enumerate(self.coeffs):
            total += coeff * x ** exp

        # Consider it 0 if its close enough to avoid errors.
        if abs(total) < 10 ** (-DP_PRECISION):
            return 0
        
        return total
    
    def get_roots(self):
        if self.deg == 1:
            return [-self.coeffs[0] / self.coeffs[1], ]
        if self.deg < 1:
            return []
        
        roots = []

        dpoly = self.get_derivative()
        droots = dpoly.get_roots()

        # if there are no statinoary points, then this function must have a single x-int somewhere.
        if droots == []:
            return [self.newtons_method(0, dpoly), ]

        # if any stationary points are a root, add them now
        for r in droots:
            if self.f(r) == 0:
                roots.append(r)

        xl_ofst = droots[0] - STD_OFST
        xr_ofst = droots[-1] + STD_OFST

        # determines if we will have a root on the left of the leftmost solution.
        if dpoly.f(xl_ofst) * self.f(droots[0]) > 0:
            roots.append(self.newtons_method(xl_ofst, dpoly))
        # same shit for right
        if dpoly.f(xr_ofst) * self.f(droots[-1]) < 0:
            roots.append(self.newtons_method(xr_ofst, dpoly))

        # loop over every pair of points to determine if there's a solution between them
        for x1, x2 in zip(droots, droots[1:]):
            if self.f(x1) * self.f(x2) < 0:
                # note: newton's method DOES NOT work, we have to use bisection method
                roots.append(self.bisect_method(x1, x2))

        # roots MUST be ordered.
        return sorted(roots)

    def bisect_method(self, xl, xr):
        if self.f(xl) * self.f(xr) > 0:
            raise Exception("Bisection method error - no possible solution between bounds.")
        
        for _ in range(MAX_ITERS):
            xc = (xl + xr) / 2

            f_xc = self.f(xc)
            if f_xc == 0: # self.f() will automatically return 0 if it's small enough.
                return xc
            
            f_xl = self.f(xl)
            
            if f_xl * f_xc > 0:
                xl = xc
            else:
                xr = xc

        raise Exception("Bisection method error - too many iterations.")

    def newtons_method(self, xi, dpoly=None):
        if dpoly == None:
            dpoly = self.get_derivative()
        
        x_cur = xi
        
        for _ in range(MAX_ITERS):
            df = dpoly.f(x_cur)
            if df == 0:
                raise Exception("Newton's method error - tangent horizontal to x-axis; no x-int.")
            
            x_prev, x_cur = x_cur, x_cur - self.f(x_cur) / df

            if abs(x_prev - x_cur) < 10 ** (-DP_PRECISION):
                return x_cur

        raise Exception("Newton's method error - too many iterations.")

    def get_derivative(self):
        dcoeffs = []
        for exp, coeff in enumerate(self.coeffs[1:], 1):
            dcoeffs.append(exp * coeff)

        return Polynomial(dcoeffs)


# example polynomial
poly = Polynomial([-0.1, -0.6, 1.8, 2.8, 0.915])
poly.print_poly()
poly.print_roots()
print()

# example polynomial with roots: −1, -1/2, -1/4, 3/5, 1
poly1 = Polynomial([3,13,-9,-53,6,40])
poly1.print_poly()
poly1.print_roots()
print()

# user input
poly2 = Polynomial()
poly2.prompt_coeffs()
poly2.print_poly()
poly2.print_roots()

# this broke the program when it only used newton's method for finding roots between stationary points
# -> fixed by using bisection method in between stps instead (it's 100% stable).
# p = Polynomial([0.16716027340115014, 0.39133920305664616, -0.05899258689994402, 0.1613918437280356, -0.27730433529636633, -0.3327396133034415, -0.2757858568737508, -0.15160942613574635, 0.09438564771094382, 0.062136313383475694])
# p.print_poly()
# p.print_roots()
