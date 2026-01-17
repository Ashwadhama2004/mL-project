"""
Confidence Scoring for Math Mentor AI

This module provides utilities for calculating and aggregating confidence scores
across different components of the system.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ConfidenceLevel(Enum):
    """Confidence level categories."""
    VERY_LOW = "very_low"      # 0.0 - 0.3
    LOW = "low"                 # 0.3 - 0.5
    MEDIUM = "medium"           # 0.5 - 0.7
    HIGH = "high"               # 0.7 - 0.85
    VERY_HIGH = "very_high"     # 0.85 - 1.0


@dataclass
class ConfidenceScore:
    """Structured confidence score with metadata."""
    score: float
    level: ConfidenceLevel
    source: str
    factors: Dict[str, float]
    needs_hitl: bool
    hitl_reason: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "score": self.score,
            "level": self.level.value,
            "source": self.source,
            "factors": self.factors,
            "needs_hitl": self.needs_hitl,
            "hitl_reason": self.hitl_reason
        }


def get_confidence_level(score: float) -> ConfidenceLevel:
    """
    Map a numeric score to a confidence level.
    
    Args:
        score: Confidence score between 0 and 1
        
    Returns:
        Corresponding confidence level
    """
    if score < 0.3:
        return ConfidenceLevel.VERY_LOW
    elif score < 0.5:
        return ConfidenceLevel.LOW
    elif score < 0.7:
        return ConfidenceLevel.MEDIUM
    elif score < 0.85:
        return ConfidenceLevel.HIGH
    else:
        return ConfidenceLevel.VERY_HIGH


def calculate_confidence(
    factors: Dict[str, float],
    weights: Dict[str, float] = None,
    source: str = "unknown",
    hitl_threshold: float = 0.7
) -> ConfidenceScore:
    """
    Calculate weighted confidence score from multiple factors.
    
    Args:
        factors: Dictionary of factor names to scores (0-1)
        weights: Optional weights for each factor (default: equal weights)
        source: Source component name
        hitl_threshold: Threshold below which HITL is triggered
        
    Returns:
        ConfidenceScore object
    """
    if not factors:
        return ConfidenceScore(
            score=0.0,
            level=ConfidenceLevel.VERY_LOW,
            source=source,
            factors={},
            needs_hitl=True,
            hitl_reason="No confidence factors provided"
        )
    
    # Normalize weights
    if weights is None:
        weights = {k: 1.0 for k in factors.keys()}
    
    total_weight = sum(weights.get(k, 1.0) for k in factors.keys())
    
    # Calculate weighted average
    weighted_sum = sum(
        factors[k] * weights.get(k, 1.0) 
        for k in factors.keys()
    )
    final_score = weighted_sum / total_weight if total_weight > 0 else 0.0
    
    # Clamp to [0, 1]
    final_score = max(0.0, min(1.0, final_score))
    
    # Determine if HITL is needed
    needs_hitl = final_score < hitl_threshold
    hitl_reason = None
    
    if needs_hitl:
        # Find the weakest factor
        weakest = min(factors.items(), key=lambda x: x[1])
        hitl_reason = f"Low confidence in {weakest[0]}: {weakest[1]:.2f}"
    
    return ConfidenceScore(
        score=final_score,
        level=get_confidence_level(final_score),
        source=source,
        factors=factors,
        needs_hitl=needs_hitl,
        hitl_reason=hitl_reason
    )


def aggregate_confidences(
    scores: List[ConfidenceScore],
    method: str = "min"
) -> ConfidenceScore:
    """
    Aggregate multiple confidence scores.
    
    Args:
        scores: List of ConfidenceScore objects
        method: Aggregation method - "min", "mean", "weighted_mean"
        
    Returns:
        Aggregated ConfidenceScore
    """
    if not scores:
        return ConfidenceScore(
            score=0.0,
            level=ConfidenceLevel.VERY_LOW,
            source="aggregated",
            factors={},
            needs_hitl=True,
            hitl_reason="No scores to aggregate"
        )
    
    # Extract numeric scores
    numeric_scores = [s.score for s in scores]
    
    # Calculate aggregate
    if method == "min":
        final_score = min(numeric_scores)
    elif method == "mean":
        final_score = sum(numeric_scores) / len(numeric_scores)
    elif method == "weighted_mean":
        # Weight by level (higher confidence gets more weight)
        weights = [s.score for s in scores]  # Self-weighting
        total = sum(s * w for s, w in zip(numeric_scores, weights))
        final_score = total / sum(weights) if sum(weights) > 0 else 0.0
    else:
        final_score = sum(numeric_scores) / len(numeric_scores)
    
    # Collect all factors
    all_factors = {}
    for score in scores:
        for k, v in score.factors.items():
            key = f"{score.source}.{k}"
            all_factors[key] = v
    
    # Check if any component needs HITL
    needs_hitl = any(s.needs_hitl for s in scores)
    hitl_reasons = [s.hitl_reason for s in scores if s.hitl_reason]
    hitl_reason = "; ".join(hitl_reasons) if hitl_reasons else None
    
    return ConfidenceScore(
        score=final_score,
        level=get_confidence_level(final_score),
        source="aggregated",
        factors=all_factors,
        needs_hitl=needs_hitl,
        hitl_reason=hitl_reason
    )


def format_confidence_display(score: ConfidenceScore) -> str:
    """
    Format confidence score for display.
    
    Args:
        score: ConfidenceScore object
        
    Returns:
        Formatted string for UI display
    """
    # Create progress bar
    bar_length = 20
    filled = int(score.score * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    # Color coding (for terminal/markdown)
    if score.level in [ConfidenceLevel.VERY_HIGH, ConfidenceLevel.HIGH]:
        status = "✓"
    elif score.level == ConfidenceLevel.MEDIUM:
        status = "~"
    else:
        status = "⚠"
    
    display = f"{status} {bar} {score.score*100:.0f}% ({score.level.value})"
    
    if score.needs_hitl:
        display += f"\n  ⚡ HITL Required: {score.hitl_reason}"
    
    return display


# Threshold constants (can be overridden via environment)
DEFAULT_OCR_THRESHOLD = 0.75
DEFAULT_VERIFIER_THRESHOLD = 0.70
DEFAULT_PARSER_THRESHOLD = 0.80


def main():
    """Test confidence scoring."""
    print("=" * 60)
    print("Math Mentor AI - Confidence Scoring Test")
    print("=" * 60)
    
    # Test basic confidence calculation
    print("\nTest 1: Basic confidence calculation")
    factors = {
        "ocr_clarity": 0.85,
        "text_coherence": 0.90,
        "symbol_recognition": 0.75
    }
    score = calculate_confidence(factors, source="ocr")
    print(f"  Factors: {factors}")
    print(f"  Score: {score.score:.2f}")
    print(f"  Level: {score.level.value}")
    print(f"  Needs HITL: {score.needs_hitl}")
    
    # Test low confidence
    print("\nTest 2: Low confidence (triggers HITL)")
    factors = {
        "ocr_clarity": 0.45,
        "text_coherence": 0.60,
    }
    score = calculate_confidence(factors, source="ocr", hitl_threshold=0.7)
    print(f"  Score: {score.score:.2f}")
    print(f"  Needs HITL: {score.needs_hitl}")
    print(f"  Reason: {score.hitl_reason}")
    
    # Test display
    print("\nTest 3: Display format")
    print(format_confidence_display(score))
    
    # Test aggregation
    print("\nTest 4: Aggregation")
    scores = [
        calculate_confidence({"f1": 0.9, "f2": 0.85}, source="parser"),
        calculate_confidence({"f1": 0.75, "f2": 0.80}, source="solver"),
        calculate_confidence({"f1": 0.60, "f2": 0.65}, source="verifier"),
    ]
    
    for s in scores:
        print(f"  {s.source}: {s.score:.2f}")
    
    agg = aggregate_confidences(scores, method="min")
    print(f"  Aggregated (min): {agg.score:.2f}")
    
    agg = aggregate_confidences(scores, method="mean")
    print(f"  Aggregated (mean): {agg.score:.2f}")


if __name__ == "__main__":
    main()
