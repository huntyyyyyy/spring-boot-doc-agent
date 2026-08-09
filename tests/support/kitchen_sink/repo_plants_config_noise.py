"""Cohesive suite from tests/support/kitchen_sink/repo_plants.py: plant_config_twins, plant_ledger_legacy_noise."""

from __future__ import annotations

from tests.support.kitchen_sink.constants import (
    BILLING,
    BOM_YML,
    CRLF_JAVA,
    CRLF_PROPS,
    DEEP_JAVA,
    DUP_BILLING,
    DUP_LEDGER,
    EMPTY_JAVA,
    EMPTY_YML,
    HUGE_JAVA,
    LATIN1_JAVA,
    LEDGER,
    LF_PROPS,
    MIXED_ENTITIES,
    MULTI_SEG_YML,
    NESTED_ENTITY,
    NOBOM_YML,
    NUL_JAVA,
    PLACEHOLDER_YML,
    RES,
    SECRETS_YML,
    SPACE_PATH,
    TWO_ENTITIES,
    UNICODE_DIR_JAVA,
    UNICODE_QUERY,
)
from tests.support.kitchen_sink.writers import _controller, _entity, _service, _w, _wb

def plant_config_twins(root: str) -> None:
    """BOM/CRLF config twins, secrets, placeholders."""
    # --- config: BOM vs no-BOM twins, CRLF vs LF twins, secrets, placeholders
    # The BOM file's line 1 is a *group header* on purpose. ﻿ is category
    # Cf — neither \s nor \w — so a plain utf-8 read leaves it in place, the
    # ^\s*-anchored key regex fails on line 1, the header never enters the
    # indent stack, and every descendant key silently loses its prefix.
    nobom_body = "spring:\n  jwt-secret: s3cr3tliteralvalue\n  datasource:\n    url: jdbc:h2:mem\n"
    _wb(root, BOM_YML, b"\xef\xbb\xbf" + nobom_body.encode("utf-8"))
    _wb(root, NOBOM_YML, nobom_body.encode("utf-8"))

    props_body = "acme.batch.size=100\nacme.batch.retries=3\n"
    _wb(root, CRLF_PROPS, props_body.replace("\n", "\r\n").encode("utf-8"))
    _wb(root, LF_PROPS, props_body.encode("utf-8"))

    _w(root, PLACEHOLDER_YML, """spring:
  application:
    name: billing-service
datasource:
  password: ${DB_PASSWORD}
  api-key: CHANGEME
  client-secret: <set-me>
""")
    _w(root, SECRETS_YML, "aws:\n  access-key-id: AKIAABCDEFGHIJKLMNOP\n"
                          "  password: hunter2literalvalue\n")
    _w(root, MULTI_SEG_YML, "spring:\n  datasource:\n"
                            "    password: multiSegLiteralSecret99\n")
    _wb(root, EMPTY_YML, b"")
    _w(root, f"{RES}/logback-spring.xml",
       "<configuration><root level=\"INFO\"/></configuration>\n")


def plant_ledger_legacy_noise(root: str) -> None:
    """Ledger collision, legacy encoding hazards, path/noise dirs."""
    from tests.support.kitchen_sink.repo_plants_legacy_parts import (
        plant_build_noise, plant_ledger_collision, plant_legacy_encoding_hazards, plant_path_hazards,
    )
    plant_ledger_collision(root)
    plant_legacy_encoding_hazards(root)
    plant_path_hazards(root)
    plant_build_noise(root)
