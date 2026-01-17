# Common Mistakes in JEE Mathematics

## Algebra Mistakes

### Quadratic Equations
- **Mistake**: Forgetting to check discriminant before solving
- **Correct**: Always check D = b² - 4ac first

- **Mistake**: Assuming (x-a)(x-b) = 0 means x = a only
- **Correct**: x = a OR x = b (two solutions)

- **Mistake**: Cancelling x from both sides of x·f(x) = x·g(x)
- **Correct**: This loses solution x = 0. Factor instead: x(f(x) - g(x)) = 0

### Logarithms
- **Mistake**: log(a + b) = log(a) + log(b)
- **Correct**: log(ab) = log(a) + log(b), NOT log(a + b)

- **Mistake**: Forgetting domain restrictions
- **Correct**: Argument must be > 0, base must be > 0 and ≠ 1

- **Mistake**: log₂(8) = 4
- **Correct**: log₂(8) = 3 (since 2³ = 8)

### Inequalities
- **Mistake**: Not reversing inequality when multiplying by negative
- **Correct**: If a > b and c < 0, then ac < bc

- **Mistake**: √(x²) = x
- **Correct**: √(x²) = |x|

### Modulus
- **Mistake**: |a + b| = |a| + |b|
- **Correct**: |a + b| ≤ |a| + |b| (triangle inequality)

---

## Calculus Mistakes

### Limits
- **Mistake**: lim(x→0) (sin x)/x = 0
- **Correct**: lim(x→0) (sin x)/x = 1

- **Mistake**: Applying L'Hôpital when limit exists directly
- **Correct**: First try direct substitution

### Differentiation
- **Mistake**: d/dx(uv) = (du/dx)(dv/dx)
- **Correct**: d/dx(uv) = u(dv/dx) + v(du/dx) (Product Rule)

- **Mistake**: d/dx(u/v) = (du/dx)/(dv/dx)
- **Correct**: d/dx(u/v) = (v·du/dx - u·dv/dx)/v² (Quotient Rule)

- **Mistake**: d/dx(sin⁻¹x) = 1/sin x
- **Correct**: d/dx(sin⁻¹x) = 1/√(1-x²)

### Integration
- **Mistake**: Forgetting +C in indefinite integrals
- **Correct**: Always add constant of integration

- **Mistake**: ∫1/x dx = ln x + C
- **Correct**: ∫1/x dx = ln|x| + C (absolute value!)

- **Mistake**: ∫f(x)g(x) dx = (∫f dx)(∫g dx)
- **Correct**: No such rule exists. Use substitution or parts

### Maxima/Minima
- **Mistake**: f'(c) = 0 means c is a maximum or minimum
- **Correct**: c is only a critical point. Check second derivative or sign change

- **Mistake**: Forgetting to check endpoints for closed intervals
- **Correct**: Global extrema can occur at endpoints

---

## Trigonometry Mistakes

### Basic Identities
- **Mistake**: sin(A + B) = sin A + sin B
- **Correct**: sin(A + B) = sin A cos B + cos A sin B

- **Mistake**: sin⁻¹(sin x) = x for all x
- **Correct**: Only for x ∈ [-π/2, π/2]. Otherwise, use principal value

- **Mistake**: cos⁻¹(cos x) = x for all x
- **Correct**: Only for x ∈ [0, π]

### Inverse Trigonometric
- **Mistake**: tan⁻¹(1/x) = cot⁻¹x
- **Correct**: This is only true for x > 0

- **Mistake**: sin⁻¹x + cos⁻¹x = π
- **Correct**: sin⁻¹x + cos⁻¹x = π/2

### Triangle Problems
- **Mistake**: Using sine rule when cosine rule is needed
- **Correct**: Use cosine rule when you have SSS or SAS

---

## Coordinate Geometry Mistakes

### Straight Lines
- **Mistake**: Slope of vertical line is 0
- **Correct**: Slope of vertical line is undefined (∞)

- **Mistake**: Lines y = 2x + 1 and y = 2x + 3 intersect
- **Correct**: Parallel lines (same slope) never intersect

### Circles
- **Mistake**: Center of x² + y² + 4x - 6y + 4 = 0 is (4, -6)
- **Correct**: Center is (-2, 3). For x² + y² + 2gx + 2fy + c = 0, center = (-g, -f)

### Conics
- **Mistake**: For x²/16 + y²/25 = 1, major axis is along x
- **Correct**: Major axis is along y (since 25 > 16)

- **Mistake**: Eccentricity e = b/a for ellipse
- **Correct**: e = √(1 - b²/a²) = c/a where c² = a² - b²

---

## Probability Mistakes

### Basic Probability
- **Mistake**: P(A ∪ B) = P(A) + P(B)
- **Correct**: P(A ∪ B) = P(A) + P(B) - P(A ∩ B) for non-mutually exclusive events

- **Mistake**: P(A) × P(B) for any two events
- **Correct**: This only works for independent events

### Conditional Probability
- **Mistake**: P(A|B) = P(B|A)
- **Correct**: P(A|B) = P(A∩B)/P(B), may not equal P(B|A)

### Counting
- **Mistake**: Confusing permutation and combination
- **Correct**: Permutation when order matters, combination when it doesn't

---

## Complex Numbers Mistakes

- **Mistake**: |z₁ + z₂| = |z₁| + |z₂|
- **Correct**: |z₁ + z₂| ≤ |z₁| + |z₂| (triangle inequality)

- **Mistake**: arg(z₁ · z₂) during principal value calculation
- **Correct**: Adjust to keep result in (-π, π]

- **Mistake**: i² = 1
- **Correct**: i² = -1

---

## Matrices and Determinants Mistakes

- **Mistake**: AB = BA for matrices
- **Correct**: Matrix multiplication is NOT commutative in general

- **Mistake**: |A + B| = |A| + |B|
- **Correct**: No such property. But |AB| = |A||B|

- **Mistake**: (AB)⁻¹ = A⁻¹B⁻¹
- **Correct**: (AB)⁻¹ = B⁻¹A⁻¹ (order reverses)

---

## Vectors Mistakes

- **Mistake**: **a** × **b** = **b** × **a**
- **Correct**: **a** × **b** = -(**b** × **a**) (anti-commutative)

- **Mistake**: |**a** · **b**| = |**a**| × |**b**|
- **Correct**: |**a** · **b**| = |**a**| × |**b**| × |cos θ|

---

## General Problem-Solving Mistakes

1. **Not reading question carefully**: Missing "exactly", "at least", "integer solutions"
2. **Unit errors**: Mixing radians and degrees in trigonometry
3. **Sign errors**: Especially in long calculations
4. **Forgetting special cases**: Division by zero, domain restrictions
5. **Rushing to answer**: Not verifying by substitution
6. **Ignoring "and" vs "or"**: Changes the entire solution approach
