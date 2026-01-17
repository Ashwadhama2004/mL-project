# Complex Numbers - JEE Mathematics Knowledge Base

## Basic Concepts

### Definition
A complex number z = a + ib where:
- a = Real part = Re(z)
- b = Imaginary part = Im(z)
- i = √(-1), i² = -1

### Powers of i
- i¹ = i
- i² = -1
- i³ = -i
- i⁴ = 1
- i^(4k+r) = iʳ

### Equality
a + ib = c + id ⟺ a = c and b = d

---

## Representations

### Cartesian Form
z = x + iy

### Polar/Trigonometric Form
z = r(cos θ + i sin θ) = r cis θ
where:
- r = |z| = √(x² + y²) (modulus)
- θ = arg(z) = tan⁻¹(y/x) (argument)

### Exponential Form
z = re^(iθ) (Euler's form)

### Argand Plane
Complex number z = x + iy represented as point (x, y)

---

## Operations

### Addition/Subtraction
(a + ib) ± (c + id) = (a ± c) + i(b ± d)

### Multiplication
(a + ib)(c + id) = (ac - bd) + i(ad + bc)

In polar form: z₁z₂ = r₁r₂[cos(θ₁ + θ₂) + i sin(θ₁ + θ₂)]

### Division
(a + ib)/(c + id) = (a + ib)(c - id)/(c² + d²)

In polar form: z₁/z₂ = (r₁/r₂)[cos(θ₁ - θ₂) + i sin(θ₁ - θ₂)]

---

## Conjugate and Modulus

### Complex Conjugate
z̄ = a - ib (if z = a + ib)

### Properties of Conjugate
- z + z̄ = 2Re(z)
- z - z̄ = 2i Im(z)
- z × z̄ = |z|² = a² + b²
- (z̄)̄ = z
- z₁ + z₂ = z̄₁ + z̄₂
- z₁z₂ = z̄₁z̄₂
- (z₁/z₂) = z̄₁/z̄₂
- z̄ = z ⟺ z is real
- z̄ = -z ⟺ z is purely imaginary

### Modulus
|z| = √(x² + y²) = √(zz̄)

### Properties of Modulus
- |z| ≥ 0, |z| = 0 ⟺ z = 0
- |z̄| = |z|
- |z₁z₂| = |z₁||z₂|
- |z₁/z₂| = |z₁|/|z₂|
- |z₁ + z₂| ≤ |z₁| + |z₂| (Triangle inequality)
- ||z₁| - |z₂|| ≤ |z₁ - z₂|
- |z₁ + z₂|² + |z₁ - z₂|² = 2(|z₁|² + |z₂|²) (Parallelogram law)

---

## Argument

### Definition
arg(z) = θ where z = |z|(cos θ + i sin θ)

### Principal Argument
θ ∈ (-π, π] or [0, 2π)

### Properties
- arg(z₁z₂) = arg(z₁) + arg(z₂)
- arg(z₁/z₂) = arg(z₁) - arg(z₂)
- arg(zⁿ) = n × arg(z)
- arg(z̄) = -arg(z)

### Quadrant-wise Principal Argument
For z = x + iy:
- Q1 (x > 0, y > 0): θ = tan⁻¹(y/x)
- Q2 (x < 0, y > 0): θ = π + tan⁻¹(y/x)
- Q3 (x < 0, y < 0): θ = -π + tan⁻¹(y/x)
- Q4 (x > 0, y < 0): θ = tan⁻¹(y/x)

---

## De Moivre's Theorem

### Statement
(cos θ + i sin θ)ⁿ = cos(nθ) + i sin(nθ)

### Applications
- Finding powers of complex numbers
- Finding nth roots

---

## Roots of Unity

### nth Roots of Unity
Solutions of zⁿ = 1:
z = e^(2πik/n) = cos(2πk/n) + i sin(2πk/n)
for k = 0, 1, 2, ..., n-1

### Cube Roots of Unity
z³ = 1: z = 1, ω, ω²
where ω = (-1 + i√3)/2

**Properties of ω**:
- ω³ = 1
- 1 + ω + ω² = 0
- ω² = ω̄
- ω² = (-1 - i√3)/2

### Fourth Roots of Unity
1, i, -1, -i

---

## nth Roots of Complex Numbers

### Formula
For zⁿ = w where w = r(cos α + i sin α):
z = r^(1/n)[cos((α + 2πk)/n) + i sin((α + 2πk)/n)]
for k = 0, 1, 2, ..., n-1

---

## Geometry of Complex Numbers

### Distance
|z₁ - z₂| = distance between z₁ and z₂

### Midpoint
(z₁ + z₂)/2

### Section Formula
Internal division in ratio m:n: (mz₂ + nz₁)/(m + n)

### Centroid of Triangle
(z₁ + z₂ + z₃)/3

### Equation of Line
- Im[(z - z₁)/(z₂ - z₁)] = 0 (line through z₁, z₂)
- z̄a + za̅ + b = 0 (general line, b is real)

### Equation of Circle
|z - z₀| = r (center z₀, radius r)
or zz̄ + az̄ + āz + b = 0 where b is real

### Perpendicular Bisector
|z - z₁| = |z - z₂|

---

## Important Loci

### |z - z₁| = |z - z₂|
Perpendicular bisector of z₁z₂

### |z - z₁| + |z - z₂| = 2a
Ellipse with foci z₁, z₂ (if 2a > |z₁ - z₂|)

### |z - z₁| - |z - z₂| = 2a
Hyperbola with foci z₁, z₂

### arg(z - z₁) = θ
Ray from z₁ at angle θ

### arg[(z - z₁)/(z - z₂)] = α
Arc of circle (constant)

---

## JEE-Specific Tips for Complex Numbers

1. **For multiplication/division**: Use polar form for easier calculation
2. **For powers and roots**: Use De Moivre's theorem
3. **For geometric problems**: Convert to |z - a| form
4. **For ω problems**: Use 1 + ω + ω² = 0 extensively
5. **For arguments**: Be careful about quadrant
6. **For minimum |z + a|**: Geometric interpretation is often faster
