# Sequences and Series - JEE Mathematics Knowledge Base

## Arithmetic Progression (AP)

### Definition
A sequence where difference between consecutive terms is constant.
a, a+d, a+2d, a+3d, ...

### nth Term
**aₙ = a + (n-1)d**

### Sum of First n Terms
**Sₙ = n/2[2a + (n-1)d] = n/2(a + l)**
where l = last term

### Properties
- If a, b, c are in AP: 2b = a + c
- Common difference: d = aₙ - aₙ₋₁
- nth term from end: l - (n-1)d
- Sum of n terms from end: n/2[2l - (n-1)d]

### Arithmetic Mean
AM of a and b = (a + b)/2

### Insertion of Arithmetic Means
n AMs between a and b: common difference = (b-a)/(n+1)

---

## Geometric Progression (GP)

### Definition
A sequence where ratio of consecutive terms is constant.
a, ar, ar², ar³, ...

### nth Term
**aₙ = ar^(n-1)**

### Sum of First n Terms
- r ≠ 1: **Sₙ = a(rⁿ - 1)/(r - 1) = a(1 - rⁿ)/(1 - r)**
- r = 1: Sₙ = na

### Sum to Infinity (|r| < 1)
**S∞ = a/(1 - r)**

### Properties
- If a, b, c are in GP: b² = ac
- Product of n terms: aⁿ × r^[n(n-1)/2]

### Geometric Mean
GM of a and b = √(ab)

### Insertion of Geometric Means
n GMs between a and b: common ratio = (b/a)^(1/(n+1))

---

## Harmonic Progression (HP)

### Definition
A sequence is HP if reciprocals form an AP.
1/a, 1/(a+d), 1/(a+2d), ...

### nth Term
**1/aₙ = 1/a + (n-1)d** where d is CD of reciprocal AP

### Harmonic Mean
HM of a and b = **2ab/(a + b)**

### Relationship
For positive numbers: **AM ≥ GM ≥ HM**
Equality when all numbers are equal.

Also: **AM × HM = GM²**

---

## Arithmetico-Geometric Progression (AGP)

### Definition
Each term = (AP term) × (GP term)
a, (a+d)r, (a+2d)r², ...

### Sum to n Terms
Method: Multiply by r and subtract

### Sum to Infinity (|r| < 1)
**S∞ = a/(1-r) + dr/(1-r)²**

---

## Special Series

### Sum of First n Natural Numbers
**Σn = 1 + 2 + 3 + ... + n = n(n+1)/2**

### Sum of Squares
**Σn² = 1² + 2² + ... + n² = n(n+1)(2n+1)/6**

### Sum of Cubes
**Σn³ = 1³ + 2³ + ... + n³ = [n(n+1)/2]² = (Σn)²**

### Sum of Fourth Powers
**Σn⁴ = n(n+1)(2n+1)(3n²+3n-1)/30**

### Sum of Fifth Powers
**Σn⁵ = n²(n+1)²(2n²+2n-1)/12**

---

## Method of Differences

### First Order Differences
If aₙ - aₙ₋₁ = f(n) is expressible simply:
aₙ = a₁ + Σf(k) for k = 2 to n

### Second Order Differences
If second differences are constant, general term is quadratic:
aₙ = An² + Bn + C

### Vₙ Method
If Tₙ = Vₙ - Vₙ₋₁:
Σ Tₙ = Vₙ - V₀

---

## Summation Techniques

### Partial Fractions
1/[n(n+1)] = 1/n - 1/(n+1)
1/[n(n+1)(n+2)] = (1/2)[1/n(n+1) - 1/(n+1)(n+2)]

### Telescoping Series
Sum collapses when consecutive terms cancel

### Common Decompositions
- 1/(n(n+k)) = (1/k)[1/n - 1/(n+k)]
- n = (1/2)[(n(n+1)) - ((n-1)n)]
- n² = (1/6)[(n)(n+1)(n+2) - (n-1)(n)(n+1)]

---

## Exponential and Logarithmic Series

### Exponential Series
**eˣ = 1 + x + x²/2! + x³/3! + ...**

### Special Values
- e = 1 + 1/1! + 1/2! + 1/3! + ...
- e⁻¹ = 1 - 1/1! + 1/2! - 1/3! + ...

### Logarithmic Series
**ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ...** (|x| ≤ 1, x ≠ -1)
**ln(1-x) = -x - x²/2 - x³/3 - ...** (|x| < 1)

### Useful Results
- ln 2 = 1 - 1/2 + 1/3 - 1/4 + ...
- ln[(1+x)/(1-x)] = 2[x + x³/3 + x⁵/5 + ...]

---

## Binomial Series

### For Any Index n
**(1+x)ⁿ = 1 + nx + n(n-1)x²/2! + n(n-1)(n-2)x³/3! + ...**
(valid for |x| < 1 when n is not a positive integer)

### Special Cases
- (1+x)⁻¹ = 1 - x + x² - x³ + ...
- (1-x)⁻¹ = 1 + x + x² + x³ + ...
- (1+x)⁻² = 1 - 2x + 3x² - 4x³ + ...
- (1-x)⁻² = 1 + 2x + 3x² + 4x³ + ...
- (1+x)^(1/2) = 1 + x/2 - x²/8 + ...
- (1+x)^(-1/2) = 1 - x/2 + 3x²/8 - ...

---

## Convergence Tests

### Geometric Series
Converges if |r| < 1

### Comparison Test
Compare with known convergent/divergent series

### Ratio Test
If lim|aₙ₊₁/aₙ| = L:
- L < 1: Converges
- L > 1: Diverges
- L = 1: Inconclusive

### Root Test
If lim|aₙ|^(1/n) = L:
- L < 1: Converges
- L > 1: Diverges
- L = 1: Inconclusive

---

## JEE-Specific Tips for Sequences & Series

1. **For finding nth term**: Use Tₙ = Sₙ - Sₙ₋₁
2. **For product in GP**: Take terms as a/r, a, ar for 3 terms
3. **For AP with constraint**: Take terms as a-d, a, a+d for 3 terms
4. **For infinite series**: Check convergence condition first
5. **For mixed series**: Look for pattern in differences
6. **Remember**: AM ≥ GM is crucial for optimization problems
