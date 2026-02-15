from overrides import override
from chromadb.telemetry.product import ProductTelemetryClient, ProductTelemetryEvent


class NoopTelemetry(ProductTelemetryClient):
    @override
    def capture(self, event: ProductTelemetryEvent) -> None:
        return
