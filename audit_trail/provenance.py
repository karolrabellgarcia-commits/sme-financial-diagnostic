# audit_trail/provenance.py
import hashlib
import json
from dataclasses import asdict
from typing import Any, Dict


class ProvenanceTracker:

    @staticmethod
    def classify_metric_certainty(is_derived: bool, has_approximations: bool) -> str:
        """Clasifica la certidumbre del dato según la Especificación Maestra."""
        if not is_derived:
            return "OBSERVADO — ALTA"
        elif is_derived and not has_approximations:
            return "DERIVADO — ALTA"
        elif is_derived and has_approximations:
            return "DERIVADO — MEDIA"
        return "ESTIMADO — CONDICIONAL"

    @staticmethod
    def generate_reproducibility_hash(data_payload: Dict[str, Any]) -> str:
        """Genera un hash SHA-256 canónico del paquete de datos y metodología

        para garantizar la trazabilidad y reproducibilidad del informe.
        """
        # Serializamos ordenadamente para asegurar que el hash sea determinista
        canonical_string = json.dumps(
            data_payload, sort_keys=True, ensure_ascii=False, default=str
        )
        return hashlib.sha256(canonical_string.encode("utf-8")).hexdigest()
