# Matrices and Determinants - JEE Mathematics Knowledge Base

## Matrices - Basic Concepts

### Definition
A matrix is a rectangular array of numbers arranged in rows and columns.
Order: m × n (m rows, n columns)

### Types of Matrices
- **Row Matrix**: 1 × n
- **Column Matrix**: m × 1
- **Square Matrix**: n × n
- **Diagonal Matrix**: aᵢⱼ = 0 for i ≠ j
- **Scalar Matrix**: Diagonal with all diagonal elements equal
- **Identity Matrix (I)**: Diagonal with all 1s
- **Zero/Null Matrix (O)**: All elements 0
- **Upper Triangular**: aᵢⱼ = 0 for i > j
- **Lower Triangular**: aᵢⱼ = 0 for i < j

### Equality
A = B iff both have same order and aᵢⱼ = bᵢⱼ for all i, j

---

## Matrix Operations

### Addition/Subtraction
(A ± B)ᵢⱼ = aᵢⱼ ± bᵢⱼ (must have same order)

### Scalar Multiplication
(kA)ᵢⱼ = k × aᵢⱼ

### Matrix Multiplication
If A is m×n and B is n×p, then AB is m×p
(AB)ᵢⱼ = Σ(k=1 to n) aᵢₖbₖⱼ

### Properties
- AB ≠ BA in general (not commutative)
- (AB)C = A(BC) (associative)
- A(B + C) = AB + AC (distributive)
- AI = IA = A
- AO = OA = O

---

## Transpose

### Definition
(Aᵀ)ᵢⱼ = aⱼᵢ (interchange rows and columns)

### Properties
- (Aᵀ)ᵀ = A
- (A + B)ᵀ = Aᵀ + Bᵀ
- (kA)ᵀ = kAᵀ
- (AB)ᵀ = BᵀAᵀ

### Special Matrices
- **Symmetric**: Aᵀ = A
- **Skew-symmetric**: Aᵀ = -A
- Any matrix = (1/2)(A + Aᵀ) + (1/2)(A - Aᵀ) (symmetric + skew-symmetric)

---

## Determinants

### 2×2 Determinant
|a b|
|c d| = ad - bc

### 3×3 Determinant (Sarrus/Cofactor)
|a₁ b₁ c₁|
|a₂ b₂ c₂| = a₁(b₂c₃-b₃c₂) - b₁(a₂c₃-a₃c₂) + c₁(a₂b₃-a₃b₂)
|a₃ b₃ c₃|

### Minor (Mᵢⱼ)
Determinant of submatrix obtained by deleting row i and column j

### Cofactor (Cᵢⱼ)
Cᵢⱼ = (-1)^(i+j) × Mᵢⱼ

### Expansion
det(A) = Σ aᵢⱼCᵢⱼ along any row or column

---

## Properties of Determinants

### Basic Properties
1. det(Aᵀ) = det(A)
2. Interchanging rows/columns changes sign
3. If two rows/columns identical: det = 0
4. Multiplying row/column by k multiplies det by k
5. det(kA) = kⁿ det(A) for n×n matrix
6. Adding multiple of one row to another doesn't change det
7. det(AB) = det(A) × det(B)
8. det(A⁻¹) = 1/det(A)

### Special Determinants
- det(I) = 1
- det(diagonal matrix) = product of diagonal elements
- det(triangular matrix) = product of diagonal elements

---

## Adjoint and Inverse

### Adjoint (Adjugate)
adj(A) = transpose of cofactor matrix

### Properties of Adjoint
- A × adj(A) = adj(A) × A = det(A) × I
- adj(AB) = adj(B) × adj(A)
- adj(Aᵀ) = (adj(A))ᵀ
- |adj(A)| = |A|^(n-1) for n×n matrix
- adj(adj(A)) = |A|^(n-2) × A

### Inverse Matrix
**A⁻¹ = adj(A) / det(A)** (exists only if det(A) ≠ 0)

### Properties of Inverse
- AA⁻¹ = A⁻¹A = I
- (A⁻¹)⁻¹ = A
- (AB)⁻¹ = B⁻¹A⁻¹
- (Aᵀ)⁻¹ = (A⁻¹)ᵀ
- (kA)⁻¹ = (1/k)A⁻¹

### Singular and Non-singular
- **Singular**: det(A) = 0, no inverse
- **Non-singular**: det(A) ≠ 0, inverse exists

---

## System of Linear Equations

### Matrix Form
AX = B

### Cramer's Rule (n equations, n unknowns)
x = Dₓ/D, y = Dᵧ/D, z = D_z/D
where D = det(A), Dₓ = det(A with column replaced by B)

### Consistency Conditions
For AX = B:
- **D ≠ 0**: Unique solution
- **D = 0, Dₓ = Dᵧ = D_z = 0**: Infinite solutions
- **D = 0, at least one Dᵢ ≠ 0**: No solution

### Homogeneous System (AX = 0)
- Always consistent (trivial solution X = 0)
- **D ≠ 0**: Only trivial solution
- **D = 0**: Infinite non-trivial solutions

### Rank Method
For augmented matrix [A|B]:
- rank(A) = rank([A|B]) = n: Unique solution
- rank(A) = rank([A|B]) < n: Infinite solutions
- rank(A) ≠ rank([A|B]): No solution

---

## Elementary Operations

### Row Operations
- Rᵢ ↔ Rⱼ (interchange rows)
- Rᵢ → kRᵢ (multiply row by non-zero k)
- Rᵢ → Rᵢ + kRⱼ (add multiple of one row to another)

### Row Echelon Form
- First non-zero entry (pivot) of each row is to the right of pivot above
- All zero rows at bottom

### Rank
Number of non-zero rows in echelon form

---

## Special Matrices

### Orthogonal Matrix
AᵀA = AAᵀ = I
- det(A) = ±1
- A⁻¹ = Aᵀ

### Idempotent Matrix
A² = A

### Nilpotent Matrix
Aᵏ = O for some positive integer k
(smallest such k is index of nilpotency)

### Involutory Matrix
A² = I (A = A⁻¹)

### Hermitian Matrix
A* = A (where A* is conjugate transpose)

### Unitary Matrix
A*A = AA* = I

---

## Important Determinant Results

### Product of Roots
For cubic ax³ + bx² + cx + d = 0:
Product = -d/a = -(constant term)/(leading coefficient)

### Vandermonde Determinant
|1  a  a²|
|1  b  b²| = (b-a)(c-a)(c-b)
|1  c  c²|

### Circulant Determinant
Special patterns with cyclic elements

---

## JEE-Specific Tips for Matrices/Determinants

1. **For calculating determinants**: Use row/column operations to create zeros
2. **For inverse**: Direct formula for 2×2, cofactor method for 3×3
3. **For system of equations**: Check D first to determine solution type
4. **For proving identities**: Use properties, not direct expansion
5. **For rank**: Reduce to echelon form
6. **Remember**: |AB| = |A||B|, not |A + B| = |A| + |B|
7. **Common trap**: Order of multiplication matters in matrix inverse
