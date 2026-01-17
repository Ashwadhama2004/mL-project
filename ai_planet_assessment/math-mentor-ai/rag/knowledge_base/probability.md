# Probability - JEE Mathematics Knowledge Base

## Basic Concepts

### Definitions
- **Experiment**: Any process that produces well-defined outcomes
- **Sample Space (S)**: Set of all possible outcomes
- **Event**: Any subset of sample space
- **Probability**: P(E) = Number of favorable outcomes / Total outcomes

### Axioms of Probability
1. 0 ≤ P(E) ≤ 1 for any event E
2. P(S) = 1 (certainty)
3. P(∅) = 0 (impossible event)

---

## Fundamental Rules

### Addition Rule
- **Mutually Exclusive Events**: P(A ∪ B) = P(A) + P(B)
- **General Addition**: P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
- **Three Events**: P(A ∪ B ∪ C) = P(A) + P(B) + P(C) - P(A∩B) - P(B∩C) - P(A∩C) + P(A∩B∩C)

### Complement Rule
P(A') = 1 - P(A)
where A' is the complement of A

### Multiplication Rule
- **Independent Events**: P(A ∩ B) = P(A) × P(B)
- **Dependent Events**: P(A ∩ B) = P(A) × P(B|A)

---

## Conditional Probability

### Definition
P(A|B) = P(A ∩ B) / P(B), where P(B) > 0

### Properties
- P(A|B) + P(A'|B) = 1
- P(A ∩ B) = P(A|B) × P(B) = P(B|A) × P(A)

---

## Independent Events

### Definition
Events A and B are independent if P(A ∩ B) = P(A) × P(B)

### Equivalent Conditions
- P(A|B) = P(A)
- P(B|A) = P(B)

### Multiple Independent Events
P(A₁ ∩ A₂ ∩ ... ∩ Aₙ) = P(A₁) × P(A₂) × ... × P(Aₙ)

---

## Bayes' Theorem

### Formula
P(Aᵢ|B) = P(B|Aᵢ) × P(Aᵢ) / Σ[P(B|Aⱼ) × P(Aⱼ)]

### Total Probability Theorem
If A₁, A₂, ..., Aₙ are mutually exclusive and exhaustive:
P(B) = Σ P(B|Aᵢ) × P(Aᵢ)

---

## Permutations and Combinations in Probability

### Equally Likely Outcomes
P(E) = n(E) / n(S)
where n(E) = |E| and n(S) = |S|

### Common Counting Techniques
- **Ordered selection (Permutation)**: ⁿPᵣ = n!/(n-r)!
- **Unordered selection (Combination)**: ⁿCᵣ = n!/[r!(n-r)!]
- **With repetition**: n^r for r selections from n items

---

## Random Variables

### Discrete Random Variable
Takes countable number of values with associated probabilities

### Probability Distribution
Sum of all probabilities = 1: Σ P(X = xᵢ) = 1

### Mean (Expected Value)
E(X) = μ = Σ xᵢ × P(X = xᵢ)

### Variance
Var(X) = σ² = E(X²) - [E(X)]² = Σ xᵢ² × P(X = xᵢ) - μ²

### Standard Deviation
σ = √Var(X)

---

## Binomial Distribution

### Conditions
1. Fixed number of trials (n)
2. Each trial has two outcomes (success/failure)
3. Probability of success (p) is constant
4. Trials are independent

### Probability Mass Function
P(X = r) = ⁿCᵣ × pʳ × qⁿ⁻ʳ
where q = 1 - p

### Properties
- Mean: μ = np
- Variance: σ² = npq
- Mode: (n+1)p or floor value

---

## Bernoulli Distribution

### Single Trial
P(X = 1) = p (success)
P(X = 0) = q = 1 - p (failure)

### Properties
- Mean: E(X) = p
- Variance: Var(X) = pq

---

## Geometric Distribution

### Definition
Probability of first success on kth trial

### Formula
P(X = k) = q^(k-1) × p

### Mean
E(X) = 1/p

---

## Important Probability Results

### At Least One Success
P(at least one) = 1 - P(none)

### Drawing Without Replacement
Use combinations: P = (favorable combinations) / (total combinations)

### Drawing With Replacement
Use multiplication: P = pⁿ for n identical events

### Probability in Cards
- Total cards = 52
- 4 suits: Hearts, Diamonds (red), Clubs, Spades (black)
- 13 cards per suit: A, 2-10, J, Q, K
- Face cards = 12 (J, Q, K in each suit)

### Probability in Dice
- Single die: 6 outcomes
- Two dice: 36 outcomes
- Sum = 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) → 6 ways

---

## Odds and Probability

### Odds in Favor
Odds in favor of A = P(A) : P(A') = P(A) / [1 - P(A)]

### Odds Against
Odds against A = P(A') : P(A) = [1 - P(A)] / P(A)

---

## JEE-Specific Tips for Probability

1. **Always identify**: Sample space, favorable outcomes, and independence
2. **For "at least" problems**: Use complement: P(at least 1) = 1 - P(none)
3. **For conditional probability**: Draw tree diagrams for complex problems
4. **For Bayes' theorem**: Clearly identify prior and posterior probabilities
5. **For binomial**: Check if all four conditions are satisfied
6. **Common trap**: Confusing with/without replacement scenarios
7. **Verify your answer**: P must be between 0 and 1
