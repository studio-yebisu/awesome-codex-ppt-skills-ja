"""Check the host's independently authored content obligations against a map.

The host derives obligations from the brief and inspected image. This module
cannot discover meaning or decide whether that inventory is complete.
"""
from __future__ import annotations


def content_obligation_errors(entities: list[dict], handoff: dict, groups: list[dict] | None = None) -> list[dict]:
    obligations = handoff.get("content_obligations", [])
    if not isinstance(obligations, list):
        return [{"reason": "content_obligations_must_be_a_list"}]
    lookup = {item.get("id"): item for item in entities}
    group_lookup = {item.get("id"): item for item in groups or []}

    def valid_group(identifier: str, ancestors: frozenset[str] = frozenset()) -> bool:
        # A semantic group can own an endpoint without emitting its own shape.
        # Its members still have to resolve to actual entities through an
        # acyclic, nonempty group tree. Ordinary entity obligations stay below.
        if identifier in ancestors:
            return False
        children = group_lookup[identifier].get("children")
        if not isinstance(children, list) or not children:
            return False
        return all(isinstance(child, str) and (
            child in lookup or child in group_lookup and valid_group(child, ancestors | {identifier})
        ) for child in children)

    errors = []
    seen = set()
    for obligation in obligations:
        if not isinstance(obligation, dict):
            errors.append({"reason": "content_obligation_must_be_an_object"})
            continue
        identity = obligation.get("id")
        if not isinstance(identity, str) or not identity.strip() or identity in seen:
            errors.append({"reason": "content_obligation_requires_unique_id", "obligation": identity})
            continue
        seen.add(identity)
        def fail(reason, **details):
            errors.append({"reason": reason, "obligation": identity, **details})
        if not isinstance(obligation.get("description"), str) or not obligation["description"].strip():
            fail("content_obligation_requires_description")
        members = obligation.get("entity_ids")
        if not isinstance(members, list) or not members or any(not isinstance(v, str) for v in members):
            fail("content_obligation_requires_entity_bindings")
            continue
        for member in members:
            if member not in lookup:
                fail("required_content_entity_missing", entity=member)
            elif lookup[member].get("meaningful_visible") is False:
                fail("required_content_marked_nonmeaningful", entity=member)
        connection = obligation.get("connection")
        if connection is None:
            continue
        if not isinstance(connection, dict):
            fail("required_connection_must_be_an_object")
            continue
        connector = lookup.get(connection.get("entity_id"), {})
        if connector.get("kind") != "connector" or connector.get("id") not in members:
            fail("required_connection_missing", entity=connection.get("entity_id"))
            continue
        if connector.get("reconstruction_significance", "independent_object") in {
            "measurement_evidence", "owned_content", "non_authoritative_glyph"
        }:
            fail("required_connection_must_emit_geometry", entity=connector["id"])
        intent = connector.get("connector_intent", {})
        for field in ("source_entities", "target_entities"):
            expected = connection.get(field)
            if not isinstance(expected, list) or not expected or any(not isinstance(v, str) for v in expected):
                fail("required_connection_needs_endpoints", field=field)
            elif set(expected) != set(intent.get(field, [])):
                fail("required_connection_endpoints_changed", field=field)
            elif any(v not in lookup and v not in group_lookup for v in expected):
                fail("required_connection_owner_missing", field=field)
            else:
                for owner in expected:
                    if owner not in lookup and not valid_group(owner):
                        fail("required_connection_group_invalid", field=field, group=owner)
        if not isinstance(connection.get("directed"), bool) or intent.get("directed") is not connection["directed"]:
            fail("required_connection_direction_changed")
    return errors
