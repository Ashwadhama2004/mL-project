# Linear Algebra - JEE Mathematics Knowledge Base

## Vectors

### Definition
A vector has both magnitude and direction.
Notation: **a** or →a, with magnitude |**a**| or ||**a**||

### Types of Vectors
- **Zero Vector**: Magnitude = 0, arbitrary direction
- **Unit Vector**: Magnitude = 1, denoted â = **a**/|**a**|
- **Position Vector**: Vector from origin to a point
- **Co-initial Vectors**: Same starting point
- **Collinear Vectors**: Parallel or anti-parallel
- **Coplanar Vectors**: Lie in the same plane

### Standard Unit Vectors
- î = (1, 0, 0) along x-axis
- ĵ = (0, 1, 0) along y-axis
- k̂ = (0, 0, 1) along z-axis

Any vector: **r** = xî + yĵ + zk̂

---

## Vector Operations

### Addition and Subtraction
**a** + **b** = (a₁ + b₁)î + (a₂ + b₂)ĵ + (a₃ + b₃)k̂
**a** - **b** = (a₁ - b₁)î + (a₂ - b₂)ĵ + (a₃ - b₃)k̂

### Scalar Multiplication
k**a** = ka₁î + ka₂ĵ + ka₃k̂

### Magnitude
|**a**| = √(a₁² + a₂² + a₃²)

---

## Dot Product (Scalar Product)

### Definition
**a** · **b** = |**a**| |**b**| cos θ
where θ is angle between vectors

### Component Form
**a** · **b** = a₁b₁ + a₂b₂ + a₃b₃

### Properties
- **a** · **b** = **b** · **a** (commutative)
- **a** · (**b** + **c**) = **a** · **b** + **a** · **c** (distributive)
- **a** · **a** = |**a**|²
- Perpendicular vectors: **a** · **b** = 0
- Parallel vectors: **a** · **b** = ±|**a**||**b**|

### Angle Between Vectors
cos θ = (**a** · **b**) / (|**a**| |**b**|)

### Projection
Projection of **a** on **b** = (**a** · **b**) / |**b**|
Vector projection = [(**a** · **b**) / |**b**|²] **b**

---

## Cross Product (Vector Product)

### Definition
**a** × **b** = |**a**| |**b**| sin θ n̂
where n̂ is unit vector perpendicular to both (right-hand rule)

### Component Form
**a** × **b** = |î   ĵ   k̂ |
               |a₁  a₂  a₃|
               |b₁  b₂  b₃|

= (a₂b₃ - a₃b₂)î - (a₁b₃ - a₃b₁)ĵ + (a₁b₂ - a₂b₁)k̂

### Properties
- **a** × **b** = -(**b** × **a**) (anti-commutative)
- **a** × **a** = **0**
- Parallel vectors: **a** × **b** = **0**
- î × ĵ = k̂, ĵ × k̂ = î, k̂ × î = ĵ

### Magnitude
|**a** × **b**| = |**a**| |**b**| sin θ = Area of parallelogram

### Area of Triangle
Area = (1/2)|**a** × **b**| for vectors from same vertex

---

## Scalar Triple Product

### Definition
[**a** **b** **c**] = **a** · (**b** × **c**)

### Component Form
[**a** **b** **c**] = |a₁  a₂  a₃|
                        |b₁  b₂  b₃|
                        |c₁  c₂  c₃|

### Properties
- Cyclic permutation: [**a** **b** **c**] = [**b** **c** **a**] = [**c** **a** **b**]
- Anti-cyclic: [**a** **b** **c**] = -[**a** **c** **b**]
- Coplanar vectors: [**a** **b** **c**] = 0

### Volume of Parallelepiped
Volume = |[**a** **b** **c**]|

### Volume of Tetrahedron
Volume = (1/6)|[**a** **b** **c**]|

---

## Vector Triple Product

### Formula
**a** × (**b** × **c**) = (**a** · **c**)**b** - (**a** · **b**)**c**
(**a** × **b**) × **c** = (**a** · **c**)**b** - (**b** · **c**)**a**

---

## Lines in Vector Form

### Equation of Line
Through point **a** in direction **b**:
**r** = **a** + λ**b**

Through two points **a** and **b**:
**r** = **a** + λ(**b** - **a**) = (1-λ)**a** + λ**b**

### Angle Between Lines
cos θ = |(**b₁** · **b₂**) / (|**b₁**| |**b₂**|)|
where **b₁**, **b₂** are direction vectors

### Shortest Distance Between Parallel Lines
d = |(**a₂** - **a₁**) × **b**| / |**b**|

### Shortest Distance Between Skew Lines
d = |[(**a₂** - **a₁**) · (**b₁** × **b₂**)]| / |**b₁** × **b₂**|

---

## Planes in Vector Form

### Equation of Plane
Normal form: **r** · **n** = d
where **n** is normal vector, d is distance from origin

Through point **a** with normal **n**:
(**r** - **a**) · **n** = 0

Through three points:
**r** = **a** + λ(**b** - **a**) + μ(**c** - **a**)

### Angle Between Planes
cos θ = |(**n₁** · **n₂**) / (|**n₁**| |**n₂**|)|

### Angle Between Line and Plane
sin θ = |(**b** · **n**) / (|**b**| |**n**|)|
where **b** is direction of line, **n** is normal to plane

### Distance from Point to Plane
d = |**a** · **n** - d| / |**n**|
where **a** is position vector of point

---

## Section Formula

### Internal Division
Point dividing **a** and **b** in ratio m:n internally:
**r** = (n**a** + m**b**) / (m + n)

### External Division
**r** = (m**b** - n**a**) / (m - n)

### Midpoint
**r** = (**a** + **b**) / 2

### Centroid of Triangle
**G** = (**a** + **b** + **c**) / 3

---

## JEE-Specific Tips for Vectors

1. **For perpendicularity**: Use dot product = 0
2. **For parallelism**: Use cross product = 0 or proportional components
3. **For coplanarity**: Check scalar triple product = 0
4. **For shortest distance**: Identify line type (parallel vs skew) first
5. **For plane problems**: Find normal vector using cross product
6. **Remember**: Direction ratios need not be unit vectors
