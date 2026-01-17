# Algebra - JEE Mathematics Knowledge Base

## Quadratic Equations

### Standard Form
A quadratic equation is of the form: **ax² + bx + c = 0** where a ≠ 0

### Quadratic Formula
For ax² + bx + c = 0:
```
x = (-b ± √(b² - 4ac)) / (2a)
```

### Discriminant (D = b² - 4ac)
- **D > 0**: Two distinct real roots
- **D = 0**: Two equal real roots (repeated root)
- **D < 0**: Two complex conjugate roots

### Sum and Product of Roots
For roots α and β:
- **Sum of roots**: α + β = -b/a
- **Product of roots**: αβ = c/a

### Forming Quadratic from Roots
If α and β are roots: **x² - (α + β)x + αβ = 0**

---

## Polynomial Equations

### Factor Theorem
If P(a) = 0, then (x - a) is a factor of polynomial P(x)

### Remainder Theorem
When P(x) is divided by (x - a), remainder = P(a)

### Polynomial Division
P(x) = Q(x) × D(x) + R(x)
where deg(R) < deg(D)

### Cubic Equations (ax³ + bx² + cx + d = 0)
For roots α, β, γ:
- α + β + γ = -b/a
- αβ + βγ + γα = c/a
- αβγ = -d/a

---

## Arithmetic Progression (AP)

### nth Term
**aₙ = a + (n-1)d**
where a = first term, d = common difference

### Sum of n Terms
**Sₙ = n/2 × [2a + (n-1)d]** or **Sₙ = n/2 × (a + l)**
where l = last term

### Properties
- If a, b, c are in AP: 2b = a + c
- Arithmetic Mean (AM) of a and b: (a + b)/2

---

## Geometric Progression (GP)

### nth Term
**aₙ = ar^(n-1)**
where a = first term, r = common ratio

### Sum of n Terms
- For r ≠ 1: **Sₙ = a(rⁿ - 1)/(r - 1)** or **Sₙ = a(1 - rⁿ)/(1 - r)**
- For r = 1: **Sₙ = na**

### Sum to Infinity (|r| < 1)
**S∞ = a/(1 - r)**

### Properties
- If a, b, c are in GP: b² = ac
- Geometric Mean (GM) of a and b: √(ab)

---

## Harmonic Progression (HP)

### Definition
A sequence is in HP if its reciprocals form an AP.

### nth Term
If 1/a, 1/b, 1/c... are in AP with first term 1/a and common difference d:
**1/aₙ = 1/a + (n-1)d**

### Harmonic Mean
HM of a and b: **2ab/(a + b)**

### AM-GM-HM Inequality
For positive numbers: **AM ≥ GM ≥ HM**
Equality holds when all numbers are equal.

---

## Logarithms

### Definition
If aˣ = N, then x = logₐN (a > 0, a ≠ 1, N > 0)

### Basic Properties
- logₐ(MN) = logₐM + logₐN
- logₐ(M/N) = logₐM - logₐN
- logₐ(Mⁿ) = n × logₐM
- logₐa = 1
- logₐ1 = 0

### Change of Base
**logₐN = logᵦN / logᵦa**

### Important Results
- logₐb × logᵦa = 1
- logₐb = 1/logᵦa
- a^(logₐN) = N

---

## Inequalities

### Properties
- If a > b, then a + c > b + c
- If a > b and c > 0, then ac > bc
- If a > b and c < 0, then ac < bc (inequality reverses)

### AM-GM Inequality
For positive numbers a₁, a₂, ..., aₙ:
**(a₁ + a₂ + ... + aₙ)/n ≥ ⁿ√(a₁ × a₂ × ... × aₙ)**

### Cauchy-Schwarz Inequality
(a₁² + a₂² + ... + aₙ²)(b₁² + b₂² + ... + bₙ²) ≥ (a₁b₁ + a₂b₂ + ... + aₙbₙ)²

### Triangle Inequality
|a + b| ≤ |a| + |b|
|a - b| ≥ ||a| - |b||

---

## Modulus and Greatest Integer Function

### Modulus |x|
- |x| = x if x ≥ 0
- |x| = -x if x < 0

### Properties of Modulus
- |ab| = |a| × |b|
- |a/b| = |a|/|b| (b ≠ 0)
- |a + b| ≤ |a| + |b|

### Greatest Integer [x]
[x] = greatest integer ≤ x

### Fractional Part {x}
{x} = x - [x], where 0 ≤ {x} < 1

---

## JEE-Specific Tips for Algebra

1. **For sum of roots problems**: Always use Vieta's formulas instead of finding roots
2. **For inequalities**: Check the sign of multiplied terms carefully
3. **For logarithms**: Remember domain restrictions (argument > 0, base > 0, base ≠ 1)
4. **For AP/GP**: Use middle term substitution for 3 or 5 terms
5. **For AM-GM**: Look for terms that multiply to a constant
