# Vectors and 3D Geometry - JEE Mathematics Knowledge Base

## Three-Dimensional Coordinate System

### Distance Formula
Distance between P(x₁, y₁, z₁) and Q(x₂, y₂, z₂):
**d = √[(x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²]**

### Section Formula
Point dividing PQ in ratio m:n:
**((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n), (mz₂+nz₁)/(m+n))**

### Direction Cosines
For direction making angles α, β, γ with axes:
- l = cos α, m = cos β, n = cos γ
- **l² + m² + n² = 1**

### Direction Ratios
Any numbers a, b, c proportional to l, m, n:
l = a/√(a²+b²+c²), etc.

### Direction Cosines from Two Points
l = (x₂-x₁)/d, m = (y₂-y₁)/d, n = (z₂-z₁)/d

---

## Straight Lines in 3D

### Equation Forms

**Symmetric Form** (through point (x₁,y₁,z₁) with DR a,b,c):
**(x-x₁)/a = (y-y₁)/b = (z-z₁)/c**

**Vector Form** (through point **a** in direction **b**):
**r = a + λb**

**Parametric Form**:
x = x₁ + aλ, y = y₁ + bλ, z = z₁ + cλ

**Two-Point Form**:
(x-x₁)/(x₂-x₁) = (y-y₁)/(y₂-y₁) = (z-z₁)/(z₂-z₁)

### Angle Between Lines
If DRs are (a₁,b₁,c₁) and (a₂,b₂,c₂):
**cos θ = (a₁a₂+b₁b₂+c₁c₂) / (√(a₁²+b₁²+c₁²) × √(a₂²+b₂²+c₂²))**

### Conditions
- **Parallel**: a₁/a₂ = b₁/b₂ = c₁/c₂
- **Perpendicular**: a₁a₂ + b₁b₂ + c₁c₂ = 0

### Skew Lines
Lines that are neither parallel nor intersecting.

### Shortest Distance Between Skew Lines
For lines r = a₁ + λb₁ and r = a₂ + μb₂:
**d = |(a₂-a₁) · (b₁×b₂)| / |b₁×b₂|**

### Shortest Distance Between Parallel Lines
**d = |b × (a₂-a₁)| / |b|**
where b is common direction vector

---

## Planes in 3D

### Equation Forms

**General Form**:
**ax + by + cz + d = 0**
Normal: (a, b, c)

**Normal Form**:
**lx + my + nz = p**
where (l,m,n) are DCs of normal, p = perpendicular distance from origin

**Intercept Form**:
**x/a + y/b + z/c = 1**
Intercepts: a, b, c on axes

**Point-Normal Form** (through (x₁,y₁,z₁) with normal (a,b,c)):
**a(x-x₁) + b(y-y₁) + c(z-z₁) = 0**

**Vector Form**:
**r · n = d** or **(r-a) · n = 0**

**Three-Point Form** (through A, B, C):
|x-x₁  y-y₁  z-z₁|
|x₂-x₁ y₂-y₁ z₂-z₁| = 0
|x₃-x₁ y₃-y₁ z₃-z₁|

### Distance from Point to Plane
From (x₁,y₁,z₁) to ax+by+cz+d=0:
**D = |ax₁+by₁+cz₁+d| / √(a²+b²+c²)**

### Angle Between Planes
**cos θ = |a₁a₂+b₁b₂+c₁c₂| / (√(a₁²+b₁²+c₁²) × √(a₂²+b₂²+c₂²))**

### Conditions
- **Parallel**: a₁/a₂ = b₁/b₂ = c₁/c₂
- **Perpendicular**: a₁a₂ + b₁b₂ + c₁c₂ = 0

### Family of Planes
Plane through intersection of P₁=0 and P₂=0:
**P₁ + λP₂ = 0**

---

## Line and Plane

### Angle Between Line and Plane
Line with DR (a,b,c), plane ax'+by'+cz'+d=0:
**sin θ = |aa'+bb'+cc'| / (√(a²+b²+c²) × √(a'²+b'²+c'²))**

### Conditions
- Line parallel to plane: aa' + bb' + cc' = 0
- Line perpendicular to plane: a/a' = b/b' = c/c'

### Line in Plane
Line lies in plane if:
1. Any point of line satisfies plane equation
2. Line direction is perpendicular to plane normal

### Intersection of Line and Plane
Substitute parametric equations in plane equation, solve for λ

---

## Sphere

### Equation
Center (h,k,l), radius r:
**(x-h)² + (y-k)² + (z-l)² = r²**

### General Form
**x² + y² + z² + 2ux + 2vy + 2wz + d = 0**
- Center: (-u, -v, -w)
- Radius: √(u² + v² + w² - d)

### Tangent Plane
At (x₁,y₁,z₁) on sphere x²+y²+z²=r²:
**xx₁ + yy₁ + zz₁ = r²**

---

## Coplanarity

### Four Points Coplanar
Points A, B, C, D are coplanar if:
**[AB AC AD] = 0** (scalar triple product)

Or determinant form:
|x₂-x₁ y₂-y₁ z₂-z₁|
|x₃-x₁ y₃-y₁ z₃-z₁| = 0
|x₄-x₁ y₄-y₁ z₄-z₁|

### Two Lines Coplanar
Lines r=a+λb and r=c+μd are coplanar if:
**[c-a, b, d] = 0**

---

## Projection

### Projection of Point on Line
Foot of perpendicular from (x₀,y₀,z₀) to line:
1. Write general point on line
2. Apply perpendicularity condition

### Projection of Point on Plane
Foot of perpendicular from (x₀,y₀,z₀) to plane:
1. Write line through point perpendicular to plane
2. Find intersection with plane

### Image of Point
Image of A in plane = 2(foot) - A

---

## Tetrahedron

### Volume
For vertices A, B, C, D:
**V = (1/6)|[AB AC AD]|**

### Centroid
G = (A + B + C + D)/4

---

## JEE-Specific Tips for 3D Geometry

1. **For shortest distance**: Use vector formula with cross product
2. **For coplanarity**: Scalar triple product = 0
3. **For foot of perpendicular**: Parametric point + perpendicularity
4. **For image**: foot = midpoint of point and image
5. **For angle**: Use dot product formula
6. **Direction cosines vs ratios**: DCs satisfy l²+m²+n²=1
