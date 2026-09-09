from dataclasses import dataclass, field

@dataclass
class CapabilityState:
    can: set[str] = field(default_factory=set)
    may: set[str] = field(default_factory=set)
    did: list[str] = field(default_factory=list)
    knows_not: set[str] = field(default_factory=set)

    def allowed(self, capability: str) -> bool:
        return capability in self.can and capability in self.may

    def record(self, capability: str) -> None:
        if not self.allowed(capability):
            raise PermissionError(f"capability not authorized: {capability}")
        self.did.append(capability)

    def declare_unknown(self, capability: str) -> None:
        if capability not in self.can:
            self.knows_not.add(capability)

    def snapshot(self) -> dict:
        return {
            "CAN": sorted(self.can),
            "MAY": sorted(self.may),
            "DID": list(self.did),
            "KNOWS_NOT": sorted(self.knows_not),
        }
