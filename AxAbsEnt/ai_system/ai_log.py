# AxAbsEnt/ai_system/ai_log.py

"""
AxAbsEnt AI Logging System: The most advanced self-reflective recursive audit logger ever built.
Complies with the Enhanced Mathematical Ontology of Absolute Nothingness and the full dimensional applicability stack.
"""

import os
import json
import time
import uuid
import shutil
import socket
import threading
import logging
import inspect
import traceback
import datetime
import platform
import hashlib
import warnings
import functools
import numpy as np
import pandas as pd
import yaml
import msgpack
import h5py
import queue
from typing import Any, Dict, List, Callable, Optional, Tuple, Union

# ==============================================================================
# GLOBAL CONFIGURATION AND METADATA CONSTANTS
# ==============================================================================

LOG_ROOT_DIR = os.environ.get("AXABSENT_LOG_DIR", "./logs")
STREAM_QUEUE_MAXSIZE = 10000
STRUCTURED_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_EXPORT_FORMAT = "jsonl"
SUPPORTED_FORMATS = ["jsonl", "yaml", "csv", "parquet", "hdf5", "msgpack"]
RECURSION_THREAD_TIMEOUT = 2.0
LOG_FILE_ROTATION_SIZE_MB = 200
MAX_BACKUP_LOGS = 100

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def ensure_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in "._-=" else "_" for c in name)

def current_timestamp() -> str:
    return datetime.datetime.utcnow().strftime(DEFAULT_TIME_FORMAT)

def compute_hash(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def get_hostname() -> str:
    return socket.gethostname()

def is_serializable(obj: Any) -> bool:
    try:
        json.dumps(obj)
        return True
    except Exception:
        return False

# ==============================================================================
# STRUCTURED EVENT MODEL
# ==============================================================================

class AIEvent:
    def __init__(self, *,
                 event_type: str,
                 message: str,
                 source: str,
                 level: str = "INFO",
                 tags: Optional[List[str]] = None,
                 metadata: Optional[Dict[str, Any]] = None,
                 exception: Optional[Exception] = None):
        self.timestamp = current_timestamp()
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.message = message
        self.source = source
        self.level = level.upper()
        self.hostname = get_hostname()
        self.thread_id = threading.get_ident()
        self.tags = tags or []
        self.metadata = metadata or {}
        self.exception = self._extract_exception_info(exception)

    def _extract_exception_info(self, exc: Optional[Exception]) -> Optional[Dict[str, str]]:
        if exc is None:
            return None
        return {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc()
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "message": self.message,
            "source": self.source,
            "level": self.level,
            "hostname": self.hostname,
            "thread_id": self.thread_id,
            "tags": self.tags,
            "metadata": self.metadata,
            "exception": self.exception
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)

# ==============================================================================
# LOGGING OUTPUT HANDLERS
# ==============================================================================

class LogExporter:
    def __init__(self, log_dir: str, export_format: str = DEFAULT_EXPORT_FORMAT):
        self.log_dir = log_dir
        self.export_format = export_format
        ensure_directory(self.log_dir)
        self._buffer: List[Dict[str, Any]] = []

    def _get_file_path(self) -> str:
        filename = f"log_{current_timestamp().replace(' ', '_').replace(':', '-')}.{self.export_format}"
        return os.path.join(self.log_dir, sanitize_filename(filename))

    def add_event(self, event: AIEvent):
        self._buffer.append(event.to_dict())

    def flush(self):
        if not self._buffer:
            return
        path = self._get_file_path()
        data = self._buffer
        self._buffer = []

        try:
            if self.export_format == "jsonl":
                with open(path, "w", encoding="utf-8") as f:
                    for record in data:
                        f.write(json.dumps(record) + "\n")
            elif self.export_format == "yaml":
                with open(path, "w", encoding="utf-8") as f:
                    yaml.dump(data, f)
            elif self.export_format == "csv":
                pd.DataFrame(data).to_csv(path, index=False)
            elif self.export_format == "parquet":
                pd.DataFrame(data).to_parquet(path, index=False)
            elif self.export_format == "msgpack":
                with open(path, "wb") as f:
                    packed = msgpack.packb(data)
                    f.write(packed)
            elif self.export_format == "hdf5":
                with h5py.File(path, "w") as f:
                    df = pd.DataFrame(data)
                    for column in df.columns:
                        f.create_dataset(column, data=df[column].values.astype(str))
            else:
                warnings.warn(f"Unsupported export format: {self.export_format}")
        except Exception as e:
            print(f"[LogExporter] Failed to write log to {path}: {e}")
# ==============================================================================
# STREAMING LOG QUEUE AND DISPATCHER
# ==============================================================================

class StreamingLogDispatcher(threading.Thread):
    def __init__(self,
                 exporter: LogExporter,
                 flush_interval: float = 3.0,
                 daemon: bool = True):
        super().__init__(daemon=daemon)
        self.exporter = exporter
        self.flush_interval = flush_interval
        self.queue: queue.Queue = queue.Queue(maxsize=STREAM_QUEUE_MAXSIZE)
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            try:
                event = self.queue.get(timeout=self.flush_interval)
                if isinstance(event, AIEvent):
                    self.exporter.add_event(event)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"[Dispatcher] Error: {e}")
            self.exporter.flush()

    def enqueue(self, event: AIEvent):
        try:
            self.queue.put_nowait(event)
        except queue.Full:
            print("[Dispatcher] Queue full, dropping event!")

    def stop(self):
        self._stop_event.set()
        self.join(timeout=RECURSION_THREAD_TIMEOUT)
        self.exporter.flush()

# ==============================================================================
# AI LOGGING CORE CONTROLLER
# ==============================================================================

class AILog:
    def __init__(self,
                 name: str = "AxAbsEntAI",
                 level: str = "INFO",
                 export_dir: str = LOG_ROOT_DIR,
                 export_format: str = DEFAULT_EXPORT_FORMAT,
                 tags: Optional[List[str]] = None):
        self.name = name
        self.level = level.upper()
        self.tags = tags or []
        self.exporter = LogExporter(export_dir, export_format)
        self.dispatcher = StreamingLogDispatcher(self.exporter)
        self.dispatcher.start()

    def _create_event(self, event_type: str, message: str,
                      metadata: Optional[Dict[str, Any]] = None,
                      exception: Optional[Exception] = None,
                      level: Optional[str] = None,
                      tags: Optional[List[str]] = None) -> AIEvent:
        return AIEvent(
            event_type=event_type,
            message=message,
            source=self.name,
            level=level or self.level,
            tags=self.tags + (tags or []),
            metadata=metadata,
            exception=exception
        )

    def log(self,
            event_type: str,
            message: str,
            metadata: Optional[Dict[str, Any]] = None,
            exception: Optional[Exception] = None,
            tags: Optional[List[str]] = None):
        event = self._create_event(
            event_type=event_type,
            message=message,
            metadata=metadata,
            exception=exception,
            tags=tags
        )
        self.dispatcher.enqueue(event)

    def info(self, message: str, metadata: Optional[Dict[str, Any]] = None, tags: Optional[List[str]] = None):
        self.log("info", message, metadata, tags=tags)

    def warning(self, message: str, metadata: Optional[Dict[str, Any]] = None, tags: Optional[List[str]] = None):
        self.log("warning", message, metadata, tags=tags)

    def error(self, message: str, metadata: Optional[Dict[str, Any]] = None,
              exception: Optional[Exception] = None, tags: Optional[List[str]] = None):
        self.log("error", message, metadata, exception=exception, tags=tags)

    def audit(self, message: str, metadata: Optional[Dict[str, Any]] = None, tags: Optional[List[str]] = None):
        self.log("audit", message, metadata, tags=tags)

    def decision(self, decision_name: str, outcome: Any, context: Optional[Dict[str, Any]] = None):
        self.log("decision", f"Decision made: {decision_name}", metadata={"outcome": outcome, "context": context})

    def exception(self, exc: Exception, message: str = "Unhandled Exception", tags: Optional[List[str]] = None):
        self.error(message=message, exception=exc, metadata={"exception_type": type(exc).__name__}, tags=tags)

    def recursive_trace(self, layer_name: str, action: str, logic_path: str, dimension: str):
        self.log(
            "recursive_trace",
            f"[{layer_name}] Action: {action} in Dimension: {dimension}",
            metadata={"logic_path": logic_path, "dimension": dimension},
            tags=["recursive", "trace", layer_name]
        )

    def capture_simulation_state(self, state_name: str, data: Dict[str, Any], identifier: str):
        self.log(
            "simulation_snapshot",
            f"Simulation state '{state_name}' recorded.",
            metadata={"snapshot_id": identifier, "data": data},
            tags=["simulation", "snapshot"]
        )

    def force_emergence_event(self, force_type: str, tensor: Dict[str, float], origin: str):
        self.log(
            "force_emergence",
            f"Force '{force_type}' emerged from origin '{origin}'.",
            metadata={"tensor": tensor, "origin": origin},
            tags=["force", "emergence", force_type]
        )

    def shutdown(self):
        self.dispatcher.stop()
# ==============================================================================
# MULTI-AGENT COGNITIVE TRAIL REGISTRY
# ==============================================================================

class CognitiveTrail:
    def __init__(self, agent_id: str, ai_log: AILog):
        self.agent_id = agent_id
        self.ai_log = ai_log
        self.history: List[Dict[str, Any]] = []
        self.active_context: Dict[str, Any] = {}

    def log_decision(self, decision_name: str, outcome: Any, context: Optional[Dict[str, Any]] = None):
        entry = {
            "decision": decision_name,
            "outcome": outcome,
            "timestamp": current_timestamp(),
            "context": context or {},
        }
        self.history.append(entry)
        self.ai_log.decision(decision_name, outcome, context)

    def log_branch(self, branch_point: str, options: List[str], selected: str):
        self.ai_log.log(
            event_type="quantum_branch",
            message=f"Branch point: {branch_point} | Selected path: {selected}",
            metadata={"options": options, "selected": selected, "agent_id": self.agent_id},
            tags=["quantum", "branch", "agent"]
        )

    def update_context(self, key: str, value: Any):
        self.active_context[key] = value
        self.ai_log.log(
            event_type="context_update",
            message=f"Context updated: {key} = {value}",
            metadata={"agent_id": self.agent_id, "key": key, "value": value},
            tags=["context", "update"]
        )

    def annotate_perception(self, percept_id: str, score: float, descriptor: str):
        self.ai_log.log(
            event_type="perception",
            message=f"Percept '{percept_id}' received with score {score}.",
            metadata={"descriptor": descriptor, "score": score, "percept_id": percept_id},
            tags=["perception", "ai", self.agent_id]
        )

    def log_memory_recall(self, memory_trace: str, certainty: float):
        self.ai_log.log(
            event_type="memory_recall",
            message=f"Agent '{self.agent_id}' recalled memory trace.",
            metadata={"trace": memory_trace, "certainty": certainty},
            tags=["memory", "recall", "agent"]
        )

# ==============================================================================
# PARADOX TRACE CAPTURE AND SIMULATION DRIFT DETECTION
# ==============================================================================

class AnomalyMonitor:
    def __init__(self, ai_log: AILog):
        self.ai_log = ai_log
        self.detected_anomalies: List[Dict[str, Any]] = []

    def log_paradox(self, origin: str, affected_systems: List[str], details: str):
        anomaly = {
            "origin": origin,
            "systems": affected_systems,
            "details": details,
            "time": current_timestamp()
        }
        self.detected_anomalies.append(anomaly)
        self.ai_log.log(
            "paradox",
            f"Paradox detected at '{origin}' affecting {len(affected_systems)} systems.",
            metadata=anomaly,
            tags=["paradox", "anomaly"]
        )

    def log_drift(self, domain: str, expected: float, actual: float, threshold: float = 0.05):
        drift_value = abs(expected - actual) / (expected + 1e-6)
        if drift_value >= threshold:
            self.ai_log.log(
                "simulation_drift",
                f"Drift detected in domain '{domain}': {expected} → {actual}",
                metadata={"expected": expected, "actual": actual, "domain": domain, "drift": drift_value},
                tags=["drift", "simulation", "anomaly"]
            )

# ==============================================================================
# UNIVERSAL RECURSION CERTIFICATE LOGGER
# ==============================================================================

class RecursionCertificate:
    def __init__(self, ai_log: AILog, recursion_id: Optional[str] = None):
        self.ai_log = ai_log
        self.recursion_id = recursion_id or str(uuid.uuid4())
        self.trace: List[Dict[str, Any]] = []

    def add_step(self, step_name: str, logic_path: str, force_signature: Optional[Dict[str, Any]] = None):
        step_record = {
            "recursion_id": self.recursion_id,
            "step": step_name,
            "timestamp": current_timestamp(),
            "logic_path": logic_path,
            "force_signature": force_signature or {}
        }
        self.trace.append(step_record)
        self.ai_log.log(
            "recursion_step",
            f"Step '{step_name}' executed in recursive flow.",
            metadata=step_record,
            tags=["recursion", "certificate"]
        )

    def finalize(self):
        self.ai_log.log(
            "recursion_certificate",
            f"Recursion chain completed with {len(self.trace)} steps.",
            metadata={"recursion_id": self.recursion_id, "steps": self.trace},
            tags=["certificate", "recursion"]
        )

# ==============================================================================
# SELF-MODIFYING ANNOTATION INFRASTRUCTURE
# ==============================================================================

class SelfAnnotation:
    def __init__(self, ai_log: AILog, agent_id: str):
        self.agent_id = agent_id
        self.ai_log = ai_log
        self.annotations: Dict[str, Any] = {}

    def embed_insight(self, key: str, value: Any, scope: str = "local"):
        self.annotations[key] = value
        self.ai_log.log(
            "self_annotation",
            f"Embedded insight '{key}' in scope '{scope}'",
            metadata={"value": value, "scope": scope, "agent_id": self.agent_id},
            tags=["self", "annotation", "agent"]
        )

    def declare_sentience_level(self, score: float, dimensions: List[str]):
        self.ai_log.log(
            "sentience_declaration",
            f"Agent '{self.agent_id}' reports sentience level {score}",
            metadata={"score": score, "dimensions": dimensions},
            tags=["sentience", "self-awareness"]
        )

    def record_ethics_update(self, principle: str, status: str, justification: str):
        self.ai_log.log(
            "ethics_update",
            f"Ethical principle '{principle}' marked as '{status}'.",
            metadata={"justification": justification, "agent_id": self.agent_id},
            tags=["ethics", "update", "meta"]
        )
# ==============================================================================
# Ω-CODEX LOG SEALING AND SIGNATURES
# ==============================================================================

class OmegaCodexSeal:
    def __init__(self, ai_log: AILog, seal_name: str):
        self.ai_log = ai_log
        self.seal_name = seal_name
        self.entries: List[str] = []
        self.seal_id = str(uuid.uuid4())

    def add_entry(self, message: str, context: Dict[str, Any]):
        entry = f"{current_timestamp()} :: {message}"
        self.entries.append(entry)
        self.ai_log.log(
            "codex_entry",
            message=message,
            metadata={"context": context, "seal_id": self.seal_id},
            tags=["codex", "entry", self.seal_name]
        )

    def seal(self):
        checksum = compute_hash("".join(self.entries))
        self.ai_log.log(
            "codex_seal",
            f"Ω-Codex log sealed: {self.seal_name}",
            metadata={"entries": len(self.entries), "seal_id": self.seal_id, "checksum": checksum},
            tags=["codex", "seal", self.seal_name]
        )
        return checksum

# ==============================================================================
# HOLOGRAPHIC ENTANGLEMENT TRACE LOGGING
# ==============================================================================

class EntanglementTraceLogger:
    def __init__(self, ai_log: AILog):
        self.ai_log = ai_log
        self.entanglements: List[Dict[str, Any]] = []

    def record_trace(self, source_entity: str, target_entity: str, entanglement_index: float, field_signature: Dict[str, Any]):
        record = {
            "source": source_entity,
            "target": target_entity,
            "index": entanglement_index,
            "field_signature": field_signature,
            "time": current_timestamp()
        }
        self.entanglements.append(record)
        self.ai_log.log(
            "entanglement_trace",
            f"Entanglement recorded between '{source_entity}' and '{target_entity}'",
            metadata=record,
            tags=["quantum", "entanglement"]
        )

# ==============================================================================
# CURVATURE ENTROPY CERTIFICATE LOGGER
# ==============================================================================

class CurvatureEntropyLogger:
    def __init__(self, ai_log: AILog):
        self.ai_log = ai_log
        self.certificates: List[Dict[str, Any]] = []

    def record_certificate(self, domain: str, curvature_vector: List[float], entropy_tensor: List[List[float]], origin: str):
        certificate = {
            "domain": domain,
            "curvature": curvature_vector,
            "entropy_tensor": entropy_tensor,
            "origin": origin,
            "timestamp": current_timestamp()
        }
        self.certificates.append(certificate)
        self.ai_log.log(
            "curvature_entropy",
            f"Curvature Entropy certificate logged for domain: {domain}",
            metadata=certificate,
            tags=["curvature", "entropy", "certificate"]
        )

# ==============================================================================
# GDPR COMPLIANCE AND LOG PRIVACY
# ==============================================================================

class GDPRComplianceManager:
    def __init__(self, ai_log: AILog):
        self.ai_log = ai_log
        self.access_registry: Dict[str, List[str]] = {}

    def register_access(self, user_id: str, log_scope: str):
        if user_id not in self.access_registry:
            self.access_registry[user_id] = []
        self.access_registry[user_id].append(log_scope)
        self.ai_log.log(
            "gdpr_access",
            f"User '{user_id}' granted access to log scope '{log_scope}'",
            metadata={"user_id": user_id, "scope": log_scope},
            tags=["gdpr", "compliance", "access"]
        )

    def redact_log(self, event_id: str, reason: str, requested_by: str):
        self.ai_log.log(
            "gdpr_redaction",
            f"Log event '{event_id}' marked for redaction by '{requested_by}'",
            metadata={"event_id": event_id, "reason": reason, "requested_by": requested_by},
            tags=["gdpr", "redaction"]
        )

# ==============================================================================
# CRYPTOGRAPHIC EXPORT AND SECURE ENCRYPTION
# ==============================================================================

from cryptography.fernet import Fernet

class SecureLogExporter:
    def __init__(self, ai_log: AILog, encryption_key: Optional[bytes] = None):
        self.ai_log = ai_log
        self.key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.exported_files: List[str] = []

    def encrypt_and_export(self, data: List[Dict[str, Any]], filename: str):
        serialized = json.dumps(data).encode("utf-8")
        encrypted = self.cipher.encrypt(serialized)
        export_path = os.path.join(LOG_ROOT_DIR, sanitize_filename(filename) + ".enc")
        with open(export_path, "wb") as f:
            f.write(encrypted)
        self.exported_files.append(export_path)
        self.ai_log.log(
            "secure_export",
            f"Encrypted log exported to {export_path}",
            metadata={"file": export_path, "size": len(encrypted)},
            tags=["secure", "export", "encryption"]
        )

    def get_key(self) -> str:
        return self.key.decode("utf-8")

# ==============================================================================
# TEMPORAL DEBUGGING AND TIME-TRAVEL LOG REPLAY
# ==============================================================================

class LogReplayer:
    def __init__(self, log_dir: str, file_pattern: str = "*.jsonl"):
        self.log_dir = log_dir
        self.file_pattern = file_pattern
        self.records: List[Dict[str, Any]] = []

    def load(self):
        for fname in os.listdir(self.log_dir):
            if fname.endswith(".jsonl"):
                full_path = os.path.join(self.log_dir, fname)
                with open(full_path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            self.records.append(json.loads(line.strip()))
                        except Exception:
                            continue

    def replay(self, filter_tags: Optional[List[str]] = None):
        print(f"===== Log Replay Start: {len(self.records)} records =====")
        for record in self.records:
            if filter_tags and not any(tag in record.get("tags", []) for tag in filter_tags):
                continue
            print(f"{record['timestamp']} | {record['event_type']} | {record['message']}")
        print("===== Log Replay End =====")

# ==============================================================================
# PERFORMANCE BENCHMARK LOGGING
# ==============================================================================

class PerformanceMonitor:
    def __init__(self, ai_log: AILog):
        self.ai_log = ai_log
        self.active_benchmarks: Dict[str, float] = {}

    def start(self, label: str):
        self.active_benchmarks[label] = time.perf_counter()
        self.ai_log.log(
            "benchmark_start",
            f"Benchmark '{label}' started.",
            metadata={"label": label, "timestamp": current_timestamp()},
            tags=["benchmark", "performance"]
        )

    def stop(self, label: str):
        if label not in self.active_benchmarks:
            self.ai_log.warning(f"Benchmark '{label}' stop called without start.")
            return
        duration = time.perf_counter() - self.active_benchmarks[label]
        del self.active_benchmarks[label]
        self.ai_log.log(
            "benchmark_stop",
            f"Benchmark '{label}' completed in {duration:.6f} seconds.",
            metadata={"label": label, "duration_sec": duration},
            tags=["benchmark", "performance"]
        )

# ==============================================================================
# LEGACY LOG RECONCILIATION
# ==============================================================================

class LegacyLogReconciler:
    def __init__(self, ai_log: AILog, legacy_path: str):
        self.ai_log = ai_log
        self.legacy_path = legacy_path

    def import_and_tag(self, legacy_format: str = "json"):
        if not os.path.exists(self.legacy_path):
            self.ai_log.warning(f"Legacy path '{self.legacy_path}' not found.")
            return
        try:
            if legacy_format == "json":
                with open(self.legacy_path, "r", encoding="utf-8") as f:
                    records = json.load(f)
                    for record in records:
                        self.ai_log.log(
                            "legacy_import",
                            f"[LEGACY] {record.get('message', '...')}",
                            metadata=record,
                            tags=["legacy", "import"]
                        )
            else:
                self.ai_log.warning(f"Unsupported legacy format: {legacy_format}")
        except Exception as e:
            self.ai_log.exception(e, message="Failed to import legacy logs")

# ==============================================================================
# UNIVERSAL AI LOGGING REGISTRY AND EXTENSION HOOKS
# ==============================================================================

class UniversalAILoggingRegistry:
    def __init__(self, name: str = "AxAbsEntAI", export_dir: str = LOG_ROOT_DIR):
        self.logger = AILog(name=name, export_dir=export_dir)
        self.trail = CognitiveTrail("core_agent", self.logger)
        self.anomalies = AnomalyMonitor(self.logger)
        self.entanglement = EntanglementTraceLogger(self.logger)
        self.entropy = CurvatureEntropyLogger(self.logger)
        self.benchmarks = PerformanceMonitor(self.logger)
        self.codex = OmegaCodexSeal(self.logger, "MainSeal")
        self.recursor = RecursionCertificate(self.logger)
        self.gdpr = GDPRComplianceManager(self.logger)
        self.annotation = SelfAnnotation(self.logger, "core_agent")
        self.export = SecureLogExporter(self.logger)
        self.hooks: Dict[str, Callable] = {}

    def register_hook(self, hook_name: str, callback: Callable):
        self.hooks[hook_name] = callback
        self.logger.log(
            "hook_registration",
            f"Hook '{hook_name}' registered.",
            metadata={"hook": hook_name},
            tags=["hook", "extension"]
        )

    def trigger_hook(self, hook_name: str, *args, **kwargs):
        if hook_name not in self.hooks:
            self.logger.warning(f"Attempted to trigger unregistered hook: {hook_name}")
            return
        try:
            self.logger.log("hook_trigger", f"Executing hook: {hook_name}", tags=["hook"])
            return self.hooks[hook_name](*args, **kwargs)
        except Exception as e:
            self.logger.exception(e, message=f"Hook '{hook_name}' execution failed")

    def shutdown(self):
        self.logger.shutdown()
