# Binomial Theorem - JEE Mathematics Knowledge Base

## General Binomial Expansion

### Statement
For any positive integer n:
**(a + b)ⁿ = Σ(r=0 to n) ⁿCᵣ aⁿ⁻ʳ bʳ**

### Expanded Form
(a + b)ⁿ = ⁿC₀aⁿ + ⁿC₁aⁿ⁻¹b + ⁿC₂aⁿ⁻²b² + ... + ⁿCₙbⁿ

### Number of Terms
n + 1 terms in expansion

### General Term (Tᵣ₊₁)
**Tᵣ₊₁ = ⁿCᵣ aⁿ⁻ʳ bʳ**

---

## Special Expansions

### (1 + x)ⁿ
(1 + x)ⁿ = ⁿC₀ + ⁿC₁x + ⁿC₂x² + ... + ⁿCₙxⁿ

### (1 - x)ⁿ
(1 - x)ⁿ = ⁿC₀ - ⁿC₁x + ⁿC₂x² - ⁿC₃x³ + ... + (-1)ⁿⁿCₙxⁿ

### Sum and Difference
- (1 + x)ⁿ + (1 - x)ⁿ = 2[ⁿC₀ + ⁿC₂x² + ⁿC₄x⁴ + ...] (even terms)
- (1 + x)ⁿ - (1 - x)ⁿ = 2[ⁿC₁x + ⁿC₃x³ + ⁿC₅x⁵ + ...] (odd terms)

---

## Binomial Coefficients

### Notation
**ⁿCᵣ = n! / [r!(n-r)!] = C(n,r) = (n r)**

### Properties
- ⁿC₀ = ⁿCₙ = 1
- ⁿCᵣ = ⁿCₙ₋ᵣ
- ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ (Pascal's identity)
- ⁿCᵣ/ⁿCᵣ₋₁ = (n-r+1)/r

### Sum of Coefficients
- Put x = 1: (1+1)ⁿ = 2ⁿ = ⁿC₀ + ⁿC₁ + ⁿC₂ + ... + ⁿCₙ
- Put x = -1: 0 = ⁿC₀ - ⁿC₁ + ⁿC₂ - ... = (sum of even) - (sum of odd)

### Important Sums
- ⁿC₀ + ⁿC₁ + ⁿC₂ + ... + ⁿCₙ = 2ⁿ
- ⁿC₀ + ⁿC₂ + ⁿC₄ + ... = 2ⁿ⁻¹ (sum of even coefficients)
- ⁿC₁ + ⁿC₃ + ⁿC₅ + ... = 2ⁿ⁻¹ (sum of odd coefficients)

---

## Middle Term

### When n is Even
One middle term: T₍ₙ/₂₎₊₁ = ⁿCₙ/₂ aⁿ/² bⁿ/²

### When n is Odd
Two middle terms: T₍ₙ₊₁₎/₂ and T₍ₙ₊₃₎/₂

---

## Greatest Term

### Method
Compare ratio Tᵣ₊₁/Tᵣ with 1:
- If ratio > 1: terms increasing
- If ratio < 1: terms decreasing
- If ratio = 1: two consecutive terms are equal and greatest

### Formula for (1 + x)ⁿ
Tᵣ₊₁/Tᵣ = (n-r+1)/r × x

Greatest term when r = ⌊(n+1)x/(1+x)⌋ or ⌈...⌉

---

## Greatest Coefficient

### For (1 + x)ⁿ
- n even: Greatest coefficient = ⁿCₙ/₂
- n odd: Two greatest = ⁿC₍ₙ₋₁₎/₂ = ⁿC₍ₙ₊₁₎/₂

---

## Multinomial Theorem

### Statement
(x₁ + x₂ + ... + xₖ)ⁿ = Σ [n!/(n₁!n₂!...nₖ!)] x₁ⁿ¹x₂ⁿ²...xₖⁿᵏ

where n₁ + n₂ + ... + nₖ = n

### Number of Terms
Number of non-negative integer solutions = ⁿ⁺ᵏ⁻¹Cₖ₋₁

---

## Binomial Theorem for Negative/Fractional Index

### General Expansion (|x| < 1)
**(1 + x)ⁿ = 1 + nx + n(n-1)x²/2! + n(n-1)(n-2)x³/3! + ...**

Valid for any real n when |x| < 1 (infinite series)

### Special Cases
- (1 + x)⁻¹ = 1 - x + x² - x³ + ... = Σ(-1)ʳxʳ
- (1 - x)⁻¹ = 1 + x + x² + x³ + ... = Σxʳ
- (1 + x)⁻² = 1 - 2x + 3x² - 4x³ + ... = Σ(-1)ʳ(r+1)xʳ
- (1 - x)⁻² = 1 + 2x + 3x² + 4x³ + ... = Σ(r+1)xʳ
- (1 + x)⁻ⁿ = Σ(-1)ʳ ⁿ⁺ʳ⁻¹Cᵣ xʳ
- (1 - x)⁻ⁿ = Σ ⁿ⁺ʳ⁻¹Cᵣ xʳ

### General Term for Negative Index
In (1 + x)⁻ⁿ:
Tᵣ₊₁ = (-1)ʳ × [n(n+1)(n+2)...(n+r-1)/r!] × xʳ
     = (-1)ʳ × ⁿ⁺ʳ⁻¹Cᵣ × xʳ

---

## Applications

### Finding Coefficient of xʳ
In (a + bx)ⁿ: Coefficient of xʳ is ⁿCᵣ aⁿ⁻ʳ bʳ

### Finding Term Independent of x
Set power of x = 0 and solve for r

### Approximations
(1 + x)ⁿ ≈ 1 + nx for small x (first-order approximation)

### Divisibility Problems
Expand and analyze remainder when divided by n

---

## Summation of Series Using Binomial

### Differentiation Method
Differentiate (1+x)ⁿ = Σ ⁿCᵣ xʳ to get:
n(1+x)ⁿ⁻¹ = Σ r × ⁿCᵣ xʳ⁻¹

At x = 1: n × 2ⁿ⁻¹ = Σ r × ⁿCᵣ

### Integration Method
Integrate (1+x)ⁿ = Σ ⁿCᵣ xʳ to get series involving ⁿCᵣ/(r+1)

### Multiplication and Division
Multiply by x before differentiating for other patterns

---

## Important Series Results

### Sum of Products
- Σ ⁿCᵣ² = ²ⁿCₙ
- Σ r × ⁿCᵣ = n × 2ⁿ⁻¹
- Σ r² × ⁿCᵣ = n(n+1) × 2ⁿ⁻²
- Σ ⁿCᵣ × ⁿCᵣ₊₁ = ²ⁿCₙ₊₁

### Vandermonde's Identity
ᵐCᵣ × ⁿCₛ₋ᵣ summed for r = ᵐ⁺ⁿCₛ

---

## JEE-Specific Tips for Binomial Theorem

1. **For general term**: Use Tᵣ₊₁ formula, not Tᵣ
2. **For term independent of x**: Set total power = 0
3. **For coefficient problems**: Extract coefficient after finding term
4. **For sum of coefficients**: Put all variables = 1
5. **For alternating series**: Use (1-x)ⁿ or x = -1
6. **For greatest term**: Use ratio method
7. **Remember**: (n choose r) notation starts from r = 0
