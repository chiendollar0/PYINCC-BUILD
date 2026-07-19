from src.models import EvidenceRecord, PluginResult, ScanContext, ScanResult, ScanTask, SoftwareRecord
from src.plugins.base import BasePlugin
from src.scanner import BaseScanner, EventType, ProgressState, ScanManager


class DemoScanner(BaseScanner):
    name = "demo"

    def prepare(self, context: ScanContext) -> list[ScanTask]:
        return [ScanTask(scanner_name=self.name, payload={"index": 1})]

    def scan(self, context: ScanContext, task: ScanTask) -> ScanResult:
        return ScanResult(
            task_id=task.task_id,
            scanner_name=self.name,
            software=[SoftwareRecord(name="Example", source=self.name)],
            evidence=[EvidenceRecord(source=self.name, kind="fixture", value="ok")],
        )


class EnrichmentPlugin(BasePlugin):
    name = "enrichment"

    def run(self, context: ScanContext, result: ScanResult) -> PluginResult:
        return PluginResult(
            plugin_name=self.name,
            evidence=[EvidenceRecord(source=self.name, kind="enriched", value=result.scanner_name)],
        )


class FailingScanner(BaseScanner):
    name = "failing"

    def scan(self, context: ScanContext, task: ScanTask) -> ScanResult:
        raise RuntimeError("scanner boom")


def test_scan_manager_runs_lifecycle_and_collects_plugin_results() -> None:
    manager = ScanManager(max_workers=2)
    events: list[EventType] = []
    for event_type in EventType:
        manager.event_bus.subscribe(event_type, lambda event, event_type=event_type: events.append(event.type))

    manager.register_scanner(DemoScanner())
    manager.register_plugin(EnrichmentPlugin())
    report = manager.run()

    assert report.session_id
    assert [record.name for record in report.software] == ["Example"]
    assert {record.kind for record in report.evidence} == {"fixture", "enriched"}
    assert manager.progress.snapshot.state == ProgressState.COMPLETED
    assert EventType.SCAN_STARTED in events
    assert EventType.TASK_STARTED in events
    assert EventType.TASK_FINISHED in events
    assert EventType.PLUGIN_LOADED in events
    assert EventType.SCAN_FINISHED in events


def test_scanner_error_becomes_warning_and_scan_continues() -> None:
    manager = ScanManager(max_workers=2)
    manager.register_scanner(FailingScanner())
    manager.register_scanner(DemoScanner())

    report = manager.run()

    assert any("scanner boom" in warning for warning in report.warnings)
    assert [record.name for record in report.software] == ["Example"]
    assert manager.progress.snapshot.state == ProgressState.COMPLETED
