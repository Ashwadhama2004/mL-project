# Statistics - JEE Mathematics Knowledge Base

## Measures of Central Tendency

### Mean (Arithmetic Mean)

**For Raw Data**:
x̄ = Σxᵢ/n

**For Frequency Distribution**:
x̄ = Σfᵢxᵢ/Σfᵢ = Σfᵢxᵢ/N

**Short-cut Method**:
x̄ = A + Σfᵢdᵢ/N
where dᵢ = xᵢ - A (A is assumed mean)

**Step Deviation Method**:
x̄ = A + h × (Σfᵢuᵢ/N)
where uᵢ = (xᵢ - A)/h

### Properties of Mean
- Σ(xᵢ - x̄) = 0
- Σ(xᵢ - x̄)² is minimum
- If all values change by constant k: new mean = old mean + k
- If all values multiplied by k: new mean = k × old mean

### Combined Mean
For groups with means x̄₁, x̄₂ and sizes n₁, n₂:
**x̄ = (n₁x̄₁ + n₂x̄₂)/(n₁ + n₂)**

---

### Median

**For Ungrouped Data**:
Arrange in order, then:
- n odd: Median = ((n+1)/2)th term
- n even: Median = average of (n/2)th and (n/2 + 1)th terms

**For Grouped Data**:
**Median = L + h × ((N/2 - F)/f)**
where:
- L = lower limit of median class
- h = class width
- F = cumulative frequency before median class
- f = frequency of median class
- N = total frequency

---

### Mode

**For Ungrouped Data**: Most frequent value

**For Grouped Data**:
**Mode = L + h × ((f₁ - f₀)/(2f₁ - f₀ - f₂))**
where:
- L = lower limit of modal class
- h = class width
- f₁ = frequency of modal class
- f₀ = frequency of class before modal class
- f₂ = frequency of class after modal class

### Relationship
For moderately symmetric distribution:
**Mode = 3 × Median - 2 × Mean**

---

## Measures of Dispersion

### Range
**Range = Maximum value - Minimum value**

### Mean Deviation
**About Mean**: MD = Σfᵢ|xᵢ - x̄|/N
**About Median**: MD = Σfᵢ|xᵢ - M|/N

Mean deviation about median is minimum.

---

### Variance

**For Population**:
σ² = Σ(xᵢ - μ)²/N = (Σxᵢ²/N) - μ²

**For Sample**:
s² = Σ(xᵢ - x̄)²/(n-1)

**For Frequency Distribution**:
σ² = (Σfᵢxᵢ²/N) - x̄² = (Σfᵢxᵢ²/N) - (Σfᵢxᵢ/N)²

**Short-cut Formula**:
σ² = (Σfᵢdᵢ²/N) - (Σfᵢdᵢ/N)²
where dᵢ = xᵢ - A

**Step Deviation Formula**:
σ² = h² × [(Σfᵢuᵢ²/N) - (Σfᵢuᵢ/N)²]
where uᵢ = (xᵢ - A)/h

---

### Standard Deviation

**σ = √Variance**

### Properties
- σ ≥ 0
- If all values same, σ = 0
- Adding constant: σ unchanged
- Multiplying by k: new σ = |k| × old σ

### Combined Standard Deviation
For two groups with means x̄₁, x̄₂ and variances σ₁², σ₂²:
**σ² = (n₁σ₁² + n₂σ₂² + n₁d₁² + n₂d₂²)/(n₁ + n₂)**
where d₁ = x̄₁ - x̄, d₂ = x̄₂ - x̄

---

### Coefficient of Variation

**CV = (σ/x̄) × 100%**

Used to compare variability of different datasets.
Lower CV = more consistent.

---

## Quartiles and Percentiles

### Quartiles
- Q₁ (First Quartile): 25th percentile
- Q₂ (Second Quartile): Median (50th percentile)
- Q₃ (Third Quartile): 75th percentile

### Inter-Quartile Range
**IQR = Q₃ - Q₁**

### Quartile Deviation (Semi-IQR)
**QD = (Q₃ - Q₁)/2**

### For Grouped Data
**Qₖ = L + h × ((kN/4 - F)/f)**
where k = 1, 2, or 3

---

## Percentiles and Deciles

### Percentile
Pₖ divides data into k% below and (100-k)% above

### Decile
D₁, D₂, ..., D₉ divide data into 10 equal parts
Dₖ = Pₖ₀

---

## Skewness and Kurtosis

### Skewness
Measure of asymmetry:
- Positive skew: Mean > Median > Mode (tail to right)
- Negative skew: Mean < Median < Mode (tail to left)
- Symmetric: Mean = Median = Mode

### Pearson's Coefficient
**Skewness = (Mean - Mode)/σ = 3(Mean - Median)/σ**

---

## Correlation and Regression

### Correlation Coefficient (r)
**r = Σ(xᵢ - x̄)(yᵢ - ȳ) / √[Σ(xᵢ - x̄)² × Σ(yᵢ - ȳ)²]**

Or: **r = (Σxᵢyᵢ - nx̄ȳ) / √[(Σxᵢ² - nx̄²)(Σyᵢ² - nȳ²)]**

### Properties of r
- -1 ≤ r ≤ 1
- r = 1: Perfect positive correlation
- r = -1: Perfect negative correlation
- r = 0: No linear correlation
- r² = coefficient of determination

### Regression Lines
**Line of y on x**: y - ȳ = bᵧₓ(x - x̄)
where bᵧₓ = r(σᵧ/σₓ)

**Line of x on y**: x - x̄ = bₓᵧ(y - ȳ)
where bₓᵧ = r(σₓ/σᵧ)

### Properties
- Both lines pass through (x̄, ȳ)
- bᵧₓ × bₓᵧ = r²
- If r = ±1, both lines coincide

---

## Probability Distributions

### Mean of Random Variable
**μ = E(X) = Σ xᵢP(X = xᵢ)**

### Variance of Random Variable
**σ² = E(X²) - [E(X)]² = Σ xᵢ²P(X = xᵢ) - μ²**

### Binomial Distribution
- Mean: μ = np
- Variance: σ² = npq
- Standard deviation: σ = √(npq)

---

## JEE-Specific Tips for Statistics

1. **For mean**: Use step-deviation for class intervals
2. **For variance**: Remember σ² = (Σfᵢxᵢ²/N) - x̄²
3. **For combined statistics**: Use appropriate formulas for combined mean/variance
4. **For comparison**: Use coefficient of variation
5. **For correlation**: Check sign (positive/negative) and magnitude
6. **Transformation effects**:
   - Adding constant: mean changes, variance unchanged
   - Multiplying by constant: both change
7. **Quick check**: Mean deviation about median is minimum
