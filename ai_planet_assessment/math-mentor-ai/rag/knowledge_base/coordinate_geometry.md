# Coordinate Geometry - JEE Mathematics Knowledge Base

## Basics of Coordinate System

### Distance Formula
Distance between P(x₁, y₁) and Q(x₂, y₂):
**d = √[(x₂ - x₁)² + (y₂ - y₁)²]**

### Section Formula
Point dividing line joining (x₁, y₁) and (x₂, y₂):
- **Internal division (m:n)**: ((mx₂ + nx₁)/(m+n), (my₂ + ny₁)/(m+n))
- **External division (m:n)**: ((mx₂ - nx₁)/(m-n), (my₂ - ny₁)/(m-n))
- **Midpoint**: ((x₁ + x₂)/2, (y₁ + y₂)/2)

### Area of Triangle
For vertices (x₁, y₁), (x₂, y₂), (x₃, y₃):
**Area = (1/2)|x₁(y₂ - y₃) + x₂(y₃ - y₁) + x₃(y₁ - y₂)|**

### Collinearity Condition
Three points are collinear if area = 0

---

## Straight Lines

### Slope
**m = (y₂ - y₁)/(x₂ - x₁) = tan θ**
where θ is angle with positive x-axis

### Forms of Line Equation
- **Slope-intercept**: y = mx + c
- **Point-slope**: y - y₁ = m(x - x₁)
- **Two-point**: (y - y₁)/(y₂ - y₁) = (x - x₁)/(x₂ - x₁)
- **Intercept**: x/a + y/b = 1
- **Normal**: x cos α + y sin α = p
- **General**: ax + by + c = 0, slope = -a/b

### Distance from Point to Line
Distance from (x₁, y₁) to ax + by + c = 0:
**d = |ax₁ + by₁ + c| / √(a² + b²)**

### Distance Between Parallel Lines
For ax + by + c₁ = 0 and ax + by + c₂ = 0:
**d = |c₁ - c₂| / √(a² + b²)**

### Angle Between Lines
**tan θ = |(m₁ - m₂)/(1 + m₁m₂)|**
- Parallel: m₁ = m₂
- Perpendicular: m₁ × m₂ = -1

### Family of Lines
Lines through intersection of L₁ = 0 and L₂ = 0:
**L₁ + λL₂ = 0**

### Angle Bisectors
For lines a₁x + b₁y + c₁ = 0 and a₂x + b₂y + c₂ = 0:
**(a₁x + b₁y + c₁)/√(a₁² + b₁²) = ±(a₂x + b₂y + c₂)/√(a₂² + b₂²)**

---

## Circles

### Standard Form
**(x - h)² + (y - k)² = r²**
Center: (h, k), Radius: r

### General Form
**x² + y² + 2gx + 2fy + c = 0**
- Center: (-g, -f)
- Radius: √(g² + f² - c)
- Condition for real circle: g² + f² - c > 0

### Parametric Form
x = h + r cos θ, y = k + r sin θ

### Position of Point
For x² + y² + 2gx + 2fy + c = 0 and point (x₁, y₁):
- S₁ = x₁² + y₁² + 2gx₁ + 2fy₁ + c
- S₁ < 0: Inside, S₁ = 0: On circle, S₁ > 0: Outside

### Tangent to Circle
At point (x₁, y₁) on x² + y² = r²:
**xx₁ + yy₁ = r²**

Condition for y = mx + c to be tangent:
**c = ±r√(1 + m²)**

### Length of Tangent
From external point (x₁, y₁): **√S₁**

### Chord of Contact
From (x₁, y₁) to x² + y² = r²:
**xx₁ + yy₁ = r²**

### Common Chord
Equation: **S₁ - S₂ = 0**

### Radical Axis
Locus of points with equal tangent lengths to two circles:
**S₁ - S₂ = 0**

---

## Parabola

### Standard Forms
- y² = 4ax (opens right): Focus (a, 0), Directrix x = -a
- y² = -4ax (opens left): Focus (-a, 0), Directrix x = a
- x² = 4ay (opens up): Focus (0, a), Directrix y = -a
- x² = -4ay (opens down): Focus (0, -a), Directrix y = a

### Properties
- Vertex: (0, 0)
- Axis: y = 0 (for y² = 4ax)
- Latus Rectum: |4a|, endpoints (a, ±2a)

### Parametric Form
For y² = 4ax: x = at², y = 2at

### Tangent
At (at², 2at): **ty = x + at²**
With slope m: **y = mx + a/m**

### Normal
At (at², 2at): **y + tx = 2at + at³**

### Focal Chord
If P(at₁², 2at₁) and Q(at₂², 2at₂) lie on focal chord: **t₁t₂ = -1**

---

## Ellipse

### Standard Form
**x²/a² + y²/b² = 1** (a > b)

### Properties
- Center: (0, 0)
- Foci: (±ae, 0) where e = √(1 - b²/a²)
- Directrices: x = ±a/e
- Vertices: (±a, 0), (0, ±b)
- Latus Rectum: 2b²/a

### Eccentricity
**e = √(1 - b²/a²)** where 0 < e < 1

### Relationship
**b² = a²(1 - e²)** or **a²e² = a² - b²**

### Parametric Form
x = a cos θ, y = b sin θ

### Tangent
At (x₁, y₁): **xx₁/a² + yy₁/b² = 1**
At (a cos θ, b sin θ): **(x cos θ)/a + (y sin θ)/b = 1**
With slope m: **y = mx ± √(a²m² + b²)**

### Normal
At (a cos θ, b sin θ): **ax/cos θ - by/sin θ = a² - b²**

### Focal Property
Sum of distances from any point to foci = 2a

---

## Hyperbola

### Standard Form
**x²/a² - y²/b² = 1**

### Properties
- Center: (0, 0)
- Foci: (±ae, 0) where e = √(1 + b²/a²)
- Directrices: x = ±a/e
- Vertices: (±a, 0)
- Transverse axis: 2a
- Conjugate axis: 2b
- Latus Rectum: 2b²/a

### Eccentricity
**e = √(1 + b²/a²)** where e > 1

### Relationship
**b² = a²(e² - 1)** or **a²e² = a² + b²**

### Asymptotes
**y = ±(b/a)x** or **x²/a² - y²/b² = 0**

### Parametric Form
x = a sec θ, y = b tan θ

### Tangent
At (x₁, y₁): **xx₁/a² - yy₁/b² = 1**

### Rectangular Hyperbola
When a = b: xy = c² (after 45° rotation)

### Focal Property
|PF₁ - PF₂| = 2a (difference of distances to foci)

---

## JEE-Specific Tips for Coordinate Geometry

1. **For circles**: Use S = 0 form for tangent, chord of contact, radical axis
2. **For conics**: Remember parametric forms for tangent/normal problems
3. **For locus**: Eliminate parameter systematically
4. **For tangent condition**: Use discriminant = 0 when line touches curve
5. **For common tangent**: Set tangent equations equal and solve
6. **Remember**: a > b for horizontal major axis (ellipse), transverse axis along x for x²/a² - y²/b² = 1
