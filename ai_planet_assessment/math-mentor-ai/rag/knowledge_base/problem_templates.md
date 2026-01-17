# Problem Templates and Solution Patterns - JEE Mathematics

## Algebra Problem Templates

### Template 1: Quadratic Roots Problems
**Pattern**: Given conditions on roots α, β of ax² + bx + c = 0

**Solution Steps**:
1. Use Vieta's formulas: α + β = -b/a, αβ = c/a
2. Express given condition in terms of sum and product
3. Solve for unknowns

**Example**: If one root is twice the other, find k in x² + kx + 18 = 0
- Let roots be α and 2α
- Sum: 3α = -k
- Product: 2α² = 18 → α = ±3
- Answer: k = ∓9

---

### Template 2: AP/GP Word Problems
**Pattern**: Find terms or sum with given conditions

**Solution Steps**:
1. For 3 terms in AP: use (a-d), a, (a+d)
2. For 3 terms in GP: use a/r, a, ar
3. Apply given conditions
4. Solve system of equations

---

### Template 3: Inequality Problems
**Pattern**: Find range of x satisfying f(x) > g(x)

**Solution Steps**:
1. Rearrange to h(x) > 0 or h(x) < 0
2. Find critical points (zeros of h)
3. Use sign analysis or wavy curve method
4. Express answer in interval notation

---

## Calculus Problem Templates

### Template 4: Rate of Change
**Pattern**: Related rates or optimization

**Solution Steps**:
1. Identify given rate: dx/dt or similar
2. Find relationship between variables
3. Differentiate with respect to t
4. Substitute known values

**Example**: Ladder sliding down wall
- Given: dx/dt, find dy/dt
- Use: x² + y² = L²
- Differentiate: 2x(dx/dt) + 2y(dy/dt) = 0

---

### Template 5: Area Under Curve
**Pattern**: Find area bounded by curves

**Solution Steps**:
1. Sketch the curves
2. Find intersection points
3. Identify upper and lower curves
4. Integrate: Area = ∫[a to b](upper - lower)dx

---

### Template 6: Maxima/Minima
**Pattern**: Optimize function with constraints

**Solution Steps**:
1. Express quantity to optimize as f(x)
2. Find f'(x) = 0 → critical points
3. Use second derivative test or sign change
4. Check boundary values if interval is closed
5. Verify answer makes physical sense

---

## Coordinate Geometry Templates

### Template 7: Tangent to Conic
**Pattern**: Find tangent from external point / with given slope

**Solution Steps**:
1. For slope m: Use standard tangent form
   - Circle: y = mx ± r√(1+m²)
   - Parabola: y = mx + a/m
   - Ellipse: y = mx ± √(a²m² + b²)
2. For external point: Substitute and solve
3. Find point of contact if needed

---

### Template 8: Locus Problems
**Pattern**: Find equation of locus given geometric condition

**Solution Steps**:
1. Let P(h, k) be general point on locus
2. Apply given condition
3. Eliminate parameters
4. Replace h → x, k → y
5. Simplify to standard form

---

## Probability Templates

### Template 9: Conditional Probability
**Pattern**: Find P(A|B) or use Bayes' theorem

**Solution Steps**:
1. Define events clearly
2. For P(A|B): Use P(A|B) = P(A∩B)/P(B)
3. For Bayes: P(Aᵢ|B) = P(B|Aᵢ)P(Aᵢ) / ΣP(B|Aⱼ)P(Aⱼ)
4. Draw tree diagram if helpful

---

### Template 10: At Least Problems
**Pattern**: P(at least one success)

**Solution Steps**:
1. P(at least 1) = 1 - P(none)
2. Calculate P(none) which is often simpler
3. Subtract from 1

**Example**: P(at least one head in 3 tosses)
= 1 - P(no heads) = 1 - (1/2)³ = 7/8

---

## Trigonometry Templates

### Template 11: Prove Identity
**Pattern**: Prove LHS = RHS

**Solution Steps**:
1. Start with more complex side
2. Use standard identities
3. Convert to sines/cosines if stuck
4. Simplify step by step
5. Reach the other side

---

### Template 12: Trigonometric Equations
**Pattern**: Solve sin f(x) = k, etc.

**Solution Steps**:
1. Find principal solution θ
2. General solution:
   - sin x = k → x = nπ + (-1)ⁿθ
   - cos x = k → x = 2nπ ± θ
   - tan x = k → x = nπ + θ
3. Apply domain restrictions

---

## Complex Numbers Templates

### Template 13: Find Locus in Argand Plane
**Pattern**: |z - z₁| = k|z - z₂| or arg((z-z₁)/(z-z₂)) = θ

**Solution Steps**:
1. Let z = x + iy
2. Substitute and simplify
3. Identify geometric shape:
   - |z - z₁| = |z - z₂|: Perpendicular bisector
   - |z - z₁| + |z - z₂| = 2a: Ellipse
   - arg((z-z₁)/(z-z₂)) = θ: Arc of circle

---

### Template 14: nth Roots of Unity
**Pattern**: Solve zⁿ = 1 or zⁿ = w

**Solution Steps**:
1. Express in polar form: z = r^(1/n) · e^(i(θ+2kπ)/n)
2. k = 0, 1, 2, ..., n-1 gives n roots
3. Roots form regular polygon on circle

---

## Vectors Templates

### Template 15: Shortest Distance (Skew Lines)
**Pattern**: Find shortest distance between lines

**Solution Steps**:
1. Identify: r = a₁ + λb₁ and r = a₂ + μb₂
2. SD = |(a₂ - a₁) · (b₁ × b₂)| / |b₁ × b₂|
3. If parallel: SD = |b × (a₂ - a₁)| / |b|

---

### Template 16: Image/Foot in 3D
**Pattern**: Find image of point in line/plane

**Solution Steps**:
1. Find foot of perpendicular
   - Write line perpendicular to given line/plane through point
   - Find intersection
2. Image = 2(foot) - point

---

## Differential Equations Templates

### Template 17: Variable Separable
**Pattern**: dy/dx = f(x)g(y)

**Solution Steps**:
1. Separate: dy/g(y) = f(x)dx
2. Integrate both sides
3. Apply initial condition if given
4. Simplify for explicit solution if possible

---

### Template 18: Linear First Order
**Pattern**: dy/dx + P(x)y = Q(x)

**Solution Steps**:
1. Find IF = e^(∫P dx)
2. Solution: y × IF = ∫(Q × IF)dx + C
3. Divide by IF to get y

---

## General Problem-Solving Strategy

1. **Read Carefully**: Identify what's given and what's asked
2. **Classify Problem**: Match to known template
3. **Draw Diagram**: For geometry, coordinate geometry, 3D
4. **Choose Approach**: Algebraic vs geometric, direct vs complement
5. **Execute**: Follow template steps
6. **Verify**: Check answer satisfies original conditions
7. **Box Answer**: Present clearly
