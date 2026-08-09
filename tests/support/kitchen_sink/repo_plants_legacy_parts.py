"""Split plant helpers for ledger collision, legacy hazards, and build noise."""

from __future__ import annotations

from tests.support.kitchen_sink.constants import (
    CRLF_JAVA,
    DEEP_JAVA,
    DUP_LEDGER,
    EMPTY_JAVA,
    HUGE_JAVA,
    LATIN1_JAVA,
    LEDGER,
    NUL_JAVA,
    SPACE_PATH,
    UNICODE_DIR_JAVA,
    UNICODE_QUERY,
)
from tests.support.kitchen_sink.writers import _controller, _entity, _service, _w, _wb


def plant_ledger_collision(root: str) -> None:
    _w(root, DUP_LEDGER, _entity("com.acme.ledger", "Invoice", "ledger_invoice"))
    _w(
        root,
        UNICODE_QUERY,
        """package com.acme.ledger;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface LedgerRepository extends JpaRepository<Invoice, Long> {
    @Query("SELECT l FROM Invoice l WHERE l.nombre = 'ÁÍÝ спасибо café 日本語'")
    java.util.List<Invoice> byNombre();
}
""",
    )
    for i in range(2):
        _w(
            root,
            f"{LEDGER}/LedgerService{i}.java",
            _service("com.acme.ledger", f"LedgerService{i}"),
        )


def plant_legacy_encoding_hazards(root: str) -> None:
    _w(
        root,
        HUGE_JAVA,
        _controller("com.acme.legacy", "Huge", "huge")
        + ("// generated padding line kept well under any real size limit\n" * 180),
    )
    _wb(root, EMPTY_JAVA, b"")
    _wb(
        root,
        LATIN1_JAVA,
        b"package com.acme.legacy;\n// caf\xe9 latin-1 comment\nclass Latin1 { }\n",
    )
    _wb(root, NUL_JAVA, b"package com.acme.legacy;\nclass NulInside { }\n\x00// tail\n")
    _wb(
        root,
        CRLF_JAVA,
        _service("com.acme.legacy", "Crlf").replace("\n", "\r\n").encode("utf-8"),
    )
    _w(
        root,
        "services/legacy-batch/db/migration/V1__init.sql",
        "CREATE TABLE billing_invoice (id BIGINT PRIMARY KEY);\n",
    )


def plant_path_hazards(root: str) -> None:
    _w(root, SPACE_PATH, "# Guide\n\nA path segment with spaces in it.\n")
    _w(root, UNICODE_DIR_JAVA, _controller("com.acme.uni", "UniController", "uni"))
    _w(root, DEEP_JAVA, _service("com.acme.deep", "Leaf"))


def plant_build_noise(root: str) -> None:
    _w(root, "packages/ui/node_modules/leftpad/index.js", "module.exports = 1;\n")
    _w(
        root,
        "packages/ui/node_modules/leftpad/Leaked.java",
        _controller("com.acme.noise", "LeakedController", "leak"),
    )
    _w(
        root,
        "packages/ui/vendor/thirdparty/Vendored.java",
        _entity("com.acme.noise", "VendoredEntity", "vendored_table"),
    )
    _w(
        root,
        "packages/ui/build/generated/Generated.java",
        _entity("com.acme.noise", "GeneratedEntity", "generated_table"),
    )
    _w(
        root,
        "services/billing-service/target/generated-sources/Gen.java",
        _controller("com.acme.noise", "GenController", "gen"),
    )
    _w(root, "tools/venv/lib/site.py", "# venv noise\n")
    _w(root, "tools/dist/out.js", "// dist noise\n")
    _w(root, "coverage/report.xml", "<coverage/>\n")
    _w(root, "tools/out/Stale.java", _service("com.acme.noise", "Stale"))
