# Permutations and Combinations - JEE Mathematics Knowledge Base

## Fundamental Principles

### Addition Principle
If a task can be done in m ways OR n ways: Total = m + n

### Multiplication Principle
If a task requires doing A AND B, where A can be done in m ways and B in n ways: Total = m × n

---

## Factorial

### Definition
**n! = n × (n-1) × (n-2) × ... × 3 × 2 × 1**

### Special Values
- 0! = 1
- 1! = 1
- n! = n × (n-1)!

### Properties
- (n+1)! = (n+1) × n!
- n!/r! = n(n-1)(n-2)...(r+1) for n > r

---

## Permutations

### Definition
Arrangement of objects where ORDER MATTERS

### Formula
**ⁿPᵣ = n!/(n-r)! = n(n-1)(n-2)...(n-r+1)**

Number of ways to arrange r objects from n distinct objects

### Special Cases
- ⁿP₀ = 1
- ⁿPₙ = n!
- ⁿP₁ = n

---

## Permutations with Repetition

### All Objects Repeated
Arranging r objects from n types with unlimited repetition: **nʳ**

### Some Identical Objects
Arranging n objects where p are of type 1, q of type 2, etc.:
**n!/(p! × q! × r! × ...)**

---

## Circular Permutations

### Distinct Objects
**Number of arrangements = (n-1)!**

### When Clockwise ≠ Anticlockwise
All (n-1)! arrangements are distinguishable

### When Clockwise = Anticlockwise
Number = **(n-1)!/2**
(e.g., necklace, garland)

---

## Combinations

### Definition
Selection of objects where ORDER DOESN'T MATTER

### Formula
**ⁿCᵣ = n!/[r!(n-r)!] = ⁿPᵣ/r!**

### Properties
- ⁿC₀ = ⁿCₙ = 1
- ⁿC₁ = ⁿCₙ₋₁ = n
- ⁿCᵣ = ⁿCₙ₋ᵣ
- ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ (Pascal's identity)
- ⁿCᵣ = (n/r) × ⁿ⁻¹Cᵣ₋₁
- ⁿC₀ + ⁿC₁ + ⁿC₂ + ... + ⁿCₙ = 2ⁿ

### Combinations with Repetition
Selecting r objects from n types with repetition:
**ⁿ⁺ʳ⁻¹Cᵣ = ⁿ⁺ʳ⁻¹Cₙ₋₁**

---

## Distribution Problems

### Distributing Distinct Objects
n distinct objects into r distinct groups:
- Any group can be empty: rⁿ
- No group empty: r! × S(n,r) (Stirling number)

### Distributing Identical Objects
n identical objects into r distinct groups:
- Groups can be empty: ⁿ⁺ʳ⁻¹Cᵣ₋₁
- Each group gets at least 1: ⁿ⁻¹Cᵣ₋₁

### Distributing to Identical Groups
Use partition theory (more complex)

---

## Division into Groups

### Into Groups of Unequal Size
Dividing n objects into groups of n₁, n₂, ..., nₖ (where n₁+n₂+...+nₖ=n):
**n!/(n₁! × n₂! × ... × nₖ!)**

### Into Equal Groups (Distinct)
Dividing mn objects into m groups of n each (groups distinguishable):
**(mn)!/[(n!)ᵐ]**

### Into Equal Groups (Identical)
Dividing mn objects into m groups of n each (groups indistinguishable):
**(mn)!/[(n!)ᵐ × m!]**

---

## Arrangements with Restrictions

### Certain Objects Always Together
Treat them as one unit, arrange, then arrange within unit

### Certain Objects Never Together
Total arrangements - Arrangements with them together

### Certain Objects at Specific Positions
Fix those positions, arrange rest

### Relative Arrangement
Objects A, B in specific order: Total/2
(if A before B, or A left of B, etc.)

---

## Derangements

### Definition
Arrangement where no object is in its original position

### Formula
**Dₙ = n![1 - 1/1! + 1/2! - 1/3! + ... + (-1)ⁿ/n!]**
**Dₙ = n! × Σ(k=0 to n) (-1)ᵏ/k!**

### Approximation
Dₙ ≈ n!/e for large n

### Values
- D₁ = 0
- D₂ = 1
- D₃ = 2
- D₄ = 9
- D₅ = 44

---

## Geometry Applications

### Selecting Points
From n points, combinations for:
- Straight lines: ⁿC₂ (minus collinear adjustments)
- Triangles: ⁿC₃ (minus collinear adjustments)

### Collinearity Adjustment
If m points are collinear (no three from n points collinear):
- Lines: ⁿC₂ - ᵐC₂ + 1
- Triangles: ⁿC₃ - ᵐC₃

### Diagonals of Polygon
In n-sided polygon: **ⁿC₂ - n = n(n-3)/2**

### Intersection Points of Diagonals
In convex n-gon (no three concurrent): **ⁿC₄**

---

## Chessboard Problems

### Squares on Chessboard
Total squares on 8×8 board: Σ(k=1 to 8) k² = 204

General n×n: Σk² = n(n+1)(2n+1)/6

### Rectangles on Chessboard
Total rectangles: ⁿ⁺¹C₂ × ᵐ⁺¹C₂
For 8×8: ⁹C₂ × ⁹C₂ = 1296

### Non-attacking Rooks
Placing n non-attacking rooks on n×n: n!

---

## Word Arrangements

### Distinct Letters
Word with n distinct letters: n! arrangements

### Repeated Letters
"MISSISSIPPI": 11!/(4! × 4! × 2!)

### Words with Vowels Together
Treat vowels as unit, arrange, then arrange vowels

### Dictionary Order (Rank)
Count words before given word alphabetically

---

## Sum of Numbers

### Sum of All Numbers Formed
From digits d₁, d₂, ..., dₙ:
- Each digit appears (n-1)! times in each position
- Sum = (n-1)! × (d₁+d₂+...+dₙ) × (111...1)ₙ ₜᵢₘₑₛ

---

## JEE-Specific Tips for P&C

1. **Identify**: Permutation (order matters) vs Combination (order doesn't)
2. **Use cases**: Break complex problems into mutually exclusive cases
3. **Complement**: Sometimes easier to count what you DON'T want
4. **Bijection**: Map to equivalent simpler problem
5. **Check constraints**: Repetition allowed? Objects identical?
6. **For circular**: Remember (n-1)! for arrangements
7. **For "at least"**: Use complement method
8. **Draw diagrams**: For geometry and distribution problems
