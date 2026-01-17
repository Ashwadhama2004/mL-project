# Calculus - JEE Mathematics Knowledge Base

## Limits

### Definition
lim(x→a) f(x) = L means f(x) approaches L as x approaches a

### Standard Limits
- lim(x→0) (sin x)/x = 1
- lim(x→0) (tan x)/x = 1
- lim(x→0) (1 - cos x)/x² = 1/2
- lim(x→0) (eˣ - 1)/x = 1
- lim(x→0) (aˣ - 1)/x = ln a
- lim(x→0) (ln(1 + x))/x = 1
- lim(x→0) ((1 + x)^(1/x)) = e
- lim(x→∞) (1 + 1/x)ˣ = e
- lim(x→0) (xⁿ - aⁿ)/(x - a) = n × a^(n-1)

### L'Hôpital's Rule
If lim f(x)/g(x) gives 0/0 or ∞/∞ form:
**lim f(x)/g(x) = lim f'(x)/g'(x)**

### Sandwich/Squeeze Theorem
If g(x) ≤ f(x) ≤ h(x) and lim g(x) = lim h(x) = L, then lim f(x) = L

---

## Continuity

### Definition
f(x) is continuous at x = a if:
1. f(a) is defined
2. lim(x→a) f(x) exists
3. lim(x→a) f(x) = f(a)

### Types of Discontinuities
- **Removable**: limit exists but ≠ f(a)
- **Jump**: left and right limits exist but are different
- **Infinite**: function approaches ±∞

### Intermediate Value Theorem
If f is continuous on [a, b] and k is between f(a) and f(b), 
then there exists c ∈ (a, b) such that f(c) = k

---

## Differentiation

### First Principles
**f'(x) = lim(h→0) [f(x + h) - f(x)]/h**

### Basic Derivatives
- d/dx(xⁿ) = nxⁿ⁻¹
- d/dx(eˣ) = eˣ
- d/dx(aˣ) = aˣ ln a
- d/dx(ln x) = 1/x
- d/dx(logₐx) = 1/(x ln a)
- d/dx(sin x) = cos x
- d/dx(cos x) = -sin x
- d/dx(tan x) = sec²x
- d/dx(cot x) = -csc²x
- d/dx(sec x) = sec x tan x
- d/dx(csc x) = -csc x cot x

### Inverse Trigonometric Derivatives
- d/dx(sin⁻¹x) = 1/√(1 - x²)
- d/dx(cos⁻¹x) = -1/√(1 - x²)
- d/dx(tan⁻¹x) = 1/(1 + x²)
- d/dx(cot⁻¹x) = -1/(1 + x²)
- d/dx(sec⁻¹x) = 1/(|x|√(x² - 1))
- d/dx(csc⁻¹x) = -1/(|x|√(x² - 1))

### Rules of Differentiation
- **Product Rule**: (uv)' = u'v + uv'
- **Quotient Rule**: (u/v)' = (u'v - uv')/v²
- **Chain Rule**: d/dx[f(g(x))] = f'(g(x)) × g'(x)

### Implicit Differentiation
For F(x, y) = 0: dy/dx = -Fₓ/Fᵧ

### Parametric Differentiation
If x = f(t), y = g(t): dy/dx = (dy/dt)/(dx/dt)

### Logarithmic Differentiation
Take ln of both sides, differentiate, useful for y = f(x)^g(x)

---

## Applications of Derivatives

### Tangent and Normal
At point (x₁, y₁):
- **Tangent**: y - y₁ = m(x - x₁) where m = dy/dx at (x₁, y₁)
- **Normal**: y - y₁ = (-1/m)(x - x₁)

### Increasing/Decreasing Functions
- f'(x) > 0 → f is increasing
- f'(x) < 0 → f is decreasing
- f'(x) = 0 → f is constant (locally)

### Maxima and Minima
**First Derivative Test**:
- f'(x) changes from + to - → local maximum
- f'(x) changes from - to + → local minimum

**Second Derivative Test**:
- f'(c) = 0 and f''(c) < 0 → local maximum at c
- f'(c) = 0 and f''(c) > 0 → local minimum at c

### Concavity and Points of Inflection
- f''(x) > 0 → concave up
- f''(x) < 0 → concave down
- f''(x) = 0 and changes sign → point of inflection

### Mean Value Theorem
If f is continuous on [a, b] and differentiable on (a, b):
**f'(c) = [f(b) - f(a)]/(b - a)** for some c ∈ (a, b)

### Rolle's Theorem
If f(a) = f(b), then f'(c) = 0 for some c ∈ (a, b)

---

## Integration

### Basic Integrals
- ∫xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ -1)
- ∫1/x dx = ln|x| + C
- ∫eˣ dx = eˣ + C
- ∫aˣ dx = aˣ/ln a + C
- ∫sin x dx = -cos x + C
- ∫cos x dx = sin x + C
- ∫sec²x dx = tan x + C
- ∫csc²x dx = -cot x + C
- ∫sec x tan x dx = sec x + C
- ∫csc x cot x dx = -csc x + C

### Important Integrals
- ∫1/(1 + x²) dx = tan⁻¹x + C
- ∫1/√(1 - x²) dx = sin⁻¹x + C
- ∫1/(x√(x² - 1)) dx = sec⁻¹|x| + C
- ∫tan x dx = ln|sec x| + C
- ∫cot x dx = ln|sin x| + C
- ∫sec x dx = ln|sec x + tan x| + C
- ∫csc x dx = ln|csc x - cot x| + C

### Integration by Parts
**∫u dv = uv - ∫v du**

ILATE rule for choosing u:
I - Inverse trig, L - Logarithmic, A - Algebraic, T - Trigonometric, E - Exponential

### Integration by Substitution
If ∫f(g(x))g'(x) dx, let u = g(x), then du = g'(x)dx

### Partial Fractions
For rational functions P(x)/Q(x) where deg(P) < deg(Q):
- Linear factors: A/(x - a)
- Repeated linear: A/(x - a) + B/(x - a)²
- Quadratic: (Ax + B)/(x² + px + q)

---

## Definite Integration

### Fundamental Theorem of Calculus
**∫[a to b] f(x) dx = F(b) - F(a)** where F'(x) = f(x)

### Properties
- ∫[a to b] f(x) dx = -∫[b to a] f(x) dx
- ∫[a to b] f(x) dx = ∫[a to c] f(x) dx + ∫[c to b] f(x) dx
- ∫[a to b] f(x) dx = ∫[a to b] f(a + b - x) dx
- ∫[0 to a] f(x) dx = ∫[0 to a] f(a - x) dx

### Even and Odd Functions
- ∫[-a to a] f(x) dx = 2∫[0 to a] f(x) dx if f is even
- ∫[-a to a] f(x) dx = 0 if f is odd

### Leibniz Rule
d/dx[∫[a(x) to b(x)] f(t) dt] = f(b(x))b'(x) - f(a(x))a'(x)

---

## Applications of Integration

### Area Under Curve
Area = ∫[a to b] f(x) dx (when f(x) ≥ 0)

### Area Between Curves
Area = ∫[a to b] |f(x) - g(x)| dx

### Volume of Revolution
- **Disk method** (about x-axis): V = π∫[a to b] y² dx
- **Shell method** (about y-axis): V = 2π∫[a to b] xy dx

---

## JEE-Specific Tips for Calculus

1. **For limits**: First try direct substitution, then factorize or use L'Hôpital
2. **For derivatives**: Use logarithmic differentiation for x^x type problems
3. **For maxima/minima**: Always check boundary values for closed intervals
4. **For integration**: Look for derivative of denominator in numerator
5. **For definite integrals**: Use symmetry properties whenever possible
