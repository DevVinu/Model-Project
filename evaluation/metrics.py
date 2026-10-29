import numpy as np
from typing import Dict, Any, List


def calculate_mape(actual: np.ndarray, predicted: np.ndarray) -> float:
    """Computes Mean Absolute Percentage Error (MAPE)."""
    actual, predicted = np.array(actual, dtype=float), np.array(predicted, dtype=float)
    # Avoid zero division
    mask = actual != 0
    if not np.any(mask):
        return 0.0
    return float(np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100.0)


def calculate_classification_metrics(ground_truth_squeeze: List[bool], predicted_squeeze: List[bool]) -> Dict[str, float]:
    """Computes Precision, Recall, and F1-score on liquidity squeeze events."""
    y_true = np.array(ground_truth_squeeze, dtype=bool)
    y_pred = np.array(predicted_squeeze, dtype=bool)

    tp = int(np.sum(y_true & y_pred))
    fp = int(np.sum(~y_true & y_pred))
    fn = int(np.sum(y_true & ~y_pred))
    tn = int(np.sum(~y_true & ~y_pred))

    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 1.0
    recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 1.0
    f1 = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
    }
