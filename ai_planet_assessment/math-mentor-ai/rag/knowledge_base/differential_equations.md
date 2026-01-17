# Differential Equations - JEE Mathematics Knowledge Base

## Basic Concepts

### Definition
An equation involving derivatives of a dependent variable with respect to independent variable(s).

### Order
Highest order derivative present in the equation.

### Degree
Power of highest order derivative (when equation is polynomial in derivatives).
- Must be free from radicals and fractions in derivatives
- Not defined if transcendental functions of derivatives present

---

## Formation of Differential Equations

### From General Solution
Given y = f(x, c₁, c₂, ..., cₙ) with n arbitrary constants:
1. Differentiate n times
2. Eliminate all n constants
Result: Differential equation of order n

### Example
y = Ae^(2x) + Be^(-x) has 2 constants
- Differentiate twice to get y', y''
- Eliminate A, B to get: y'' - y' - 2y = 0

---

## First Order Differential Equations

### Variable Separable
**Form**: f(x)dx = g(y)dy

**Method**:
1. Separate variables
2. Integrate both sides
3. ∫f(x)dx = ∫g(y)dy + C

### Homogeneous Equations
**Form**: dy/dx = F(y/x) or M(x,y)dx + N(x,y)dy = 0
where M, N are homogeneous of same degree

**Method**:
1. Substitute y = vx (so dy/dx = v + x dv/dx)
2. Reduce to variable separable
3. Solve and substitute back

### Equations Reducible to Homogeneous
**Form**: dy/dx = (ax + by + c)/(dx + ey + f)

**Method**:
- If a/d = b/e, substitute ax + by = t
- Otherwise, shift origin to intersection point

### Linear First Order
**Form**: dy/dx + P(x)y = Q(x)

**Method**:
1. Integrating Factor (IF) = e^(∫P dx)
2. Solution: y × IF = ∫(Q × IF)dx + C

### Bernoulli Equation
**Form**: dy/dx + P(x)y = Q(x)yⁿ (n ≠ 0, 1)

**Method**:
1. Divide by yⁿ
2. Substitute z = y^(1-n)
3. Get linear equation in z

---

## Second Order Linear Equations

### Constant Coefficients
**Form**: ay'' + by' + cy = 0

**Method**: Assume y = e^(mx), get auxiliary equation:
**am² + bm + c = 0**

### Three Cases

**Case 1**: Two distinct real roots m₁, m₂
y = C₁e^(m₁x) + C₂e^(m₂x)

**Case 2**: Equal real roots m = m₁ = m₂
y = (C₁ + C₂x)e^(mx)

**Case 3**: Complex conjugate roots m = α ± iβ
y = e^(αx)(C₁ cos βx + C₂ sin βx)

---

## Special Types

### Exact Differential Equations
**Form**: M(x,y)dx + N(x,y)dy = 0
**Condition**: ∂M/∂y = ∂N/∂x

**Solution**: Find F(x,y) such that ∂F/∂x = M and ∂F/∂y = N
Then F(x,y) = C

### Reducible to Exact
If (∂M/∂y - ∂N/∂x)/N = f(x) alone, IF = e^(∫f(x)dx)
If (∂N/∂x - ∂M/∂y)/M = g(y) alone, IF = e^(∫g(y)dy)

---

## Applications

### Growth and Decay
**Model**: dy/dt = ky
**Solution**: y = y₀e^(kt)
- k > 0: Exponential growth
- k < 0: Exponential decay

### Newton's Law of Cooling
dT/dt = -k(T - Tₛ)
where Tₛ = surrounding temperature

**Solution**: T - Tₛ = (T₀ - Tₛ)e^(-kt)

### Population Models

**Malthusian**: dP/dt = kP
Solution: P = P₀e^(kt)

**Logistic**: dP/dt = kP(1 - P/K)
where K = carrying capacity

### Orthogonal Trajectories
Given family F(x, y, c) = 0:
1. Find dy/dx = f(x, y)
2. Replace by dx/dy = -1/f(x, y) or dy/dx = -1/f(x, y)
3. Solve new equation

---

## Geometrical Applications

### Tangent and Normal
At point (x, y) on curve:
- Slope of tangent: dy/dx
- Equation of tangent: Y - y = (dy/dx)(X - x)
- Equation of normal: Y - y = -(dx/dy)(X - x)

### Length Formulas
- Length of tangent: |y√(1 + (dx/dy)²)|
- Length of normal: |y√(1 + (dy/dx)²)|
- Length of subtangent: |y(dx/dy)|
- Length of subnormal: |y(dy/dx)|

---

## Important Standard Forms

### dy/dx = y/x
Solution: y = Cx

### dy/dx = -x/y
Solution: x² + y² = C²

### dy/dx = (y-a)/(x-b)
Solution: y - a = C(x - b)

### dy/dx = tan(y/x)
Substitute y = vx, solve for v

### x dy - y dx = 0
Solution: y/x = C

### x dy + y dx = 0
Solution: xy = C

### x dx + y dy = 0
Solution: x² + y² = C

---

## Initial Value Problems

### Definition
Differential equation + initial condition(s)

### Method
1. Find general solution with arbitrary constant(s)
2. Apply initial conditions to find specific values
3. Write particular solution

---

## JEE-Specific Tips for Differential Equations

1. **Identify type first**: Check for separable, homogeneous, linear, Bernoulli
2. **For linear equations**: Always find IF = e^(∫P dx)
3. **For homogeneous**: Check if substitution y = vx simplifies
4. **For applications**: Set up equation from physical conditions first
5. **For order/degree**: Ensure equation is polynomial in derivatives
6. **Check solution**: Substitute back to verify
7. **Common mistake**: Forgetting +C in indefinite integration
