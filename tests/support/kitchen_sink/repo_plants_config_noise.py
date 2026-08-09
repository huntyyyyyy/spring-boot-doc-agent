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
    # --- ledger service: name collision + non-ASCII in a matched query ------
    _w(root, DUP_LEDGER, _entity("com.acme.ledger", "Invoice", "ledger_invoice"))
    # 'Á' is C3 81 and 'с' is D1 81 — byte 0x81 is undefined in cp1252, so a
    # locale-decoded read of ast-grep's stdout dies here rather than merely
    # mangling. é / 日 decode to silent mojibake instead. Both are regressions
    # against the explicit encoding= on that subprocess call.
    _w(root, UNICODE_QUERY, """package com.acme.ledger;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface LedgerRepository extends JpaRepository<Invoice, Long> {
    @Query("SELECT l FROM Invoice l WHERE l.nombre = 'ÁÍÝ спасибо café 日本語'")
    java.util.List<Invoice> byNombre();
}
""")
    for i in range(2):
        _w(root, f"{LEDGER}/LedgerService{i}.java",
           _service("com.acme.ledger", f"LedgerService{i}"))

    # --- legacy batch: the encoding and size hazards ------------------------
    # ~12 KB, and it carries a @RestController so it is genuinely citable
    # evidence — which is the point of the Ch.5 divergence test.
    _w(root, HUGE_JAVA,
       _controller("com.acme.legacy", "Huge", "huge")
       + ("// generated padding line kept well under any real size limit\n" * 180))
    _wb(root, EMPTY_JAVA, b"")
    _wb(root, LATIN1_JAVA,
        b"package com.acme.legacy;\n// caf\xe9 latin-1 comment\nclass Latin1 { }\n")
    _wb(root, NUL_JAVA, b"package com.acme.legacy;\nclass NulInside { }\n\x00// tail\n")
    _wb(root, CRLF_JAVA,
        _service("com.acme.legacy", "Crlf").replace("\n", "\r\n").encode("utf-8"))
    _w(root, "services/legacy-batch/db/migration/V1__init.sql",
       "CREATE TABLE billing_invoice (id BIGINT PRIMARY KEY);\n")

    # --- path hazards -------------------------------------------------------
    _w(root, SPACE_PATH, "# Guide\n\nA path segment with spaces in it.\n")
    _w(root, UNICODE_DIR_JAVA, _controller("com.acme.uni", "UniController", "uni"))
    _w(root, DEEP_JAVA, _service("com.acme.deep", "Leaf"))

    # --- gitignored dir (empty until write-scope tests plant a stray) -------
    # Do not seed ignored untracked files here: check_pipeline_output lists
    # all ignored-untracked paths as write-scope violations, so a pre-seeded
    # Big.json would fail a clean run. Root-only /generated/ in .gitignore
    # keeps packages/ui/build/generated/ trackable for scan-exclusion tests.

    # --- build noise that must never be scanned, grouped, or cited ---------
    _w(root, "packages/ui/node_modules/leftpad/index.js", "module.exports = 1;\n")
    _w(root, "packages/ui/node_modules/leftpad/Leaked.java",
       _controller("com.acme.noise", "LeakedController", "leak"))
    _w(root, "packages/ui/vendor/thirdparty/Vendored.java",
       _entity("com.acme.noise", "VendoredEntity", "vendored_table"))
    _w(root, "packages/ui/build/generated/Generated.java",
       _entity("com.acme.noise", "GeneratedEntity", "generated_table"))
    _w(root, "services/billing-service/target/generated-sources/Gen.java",
       _controller("com.acme.noise", "GenController", "gen"))
    _w(root, "tools/venv/lib/site.py", "# venv noise\n")
    _w(root, "tools/dist/out.js", "// dist noise\n")
    _w(root, "coverage/report.xml", "<coverage/>\n")
    _w(root, "tools/out/Stale.java", _service("com.acme.noise", "Stale"))
