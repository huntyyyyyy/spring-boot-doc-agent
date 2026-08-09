"""Cohesive suite from tests/support/kitchen_sink/repo_plants.py: plant_root_and_billing."""

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

def plant_root_and_billing(root: str) -> None:
    """Root scaffolding plus billing Java entities/services."""

    _w(root, "README.md", "# Acme Platform\n\nPre-existing overview.\n")
    _w(root, "pom.xml", "<project><modules/></project>\n")
    _w(root, "build.gradle", """plugins {
    id 'org.springframework.boot' version '3.2.0'
    id 'java'
}
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10'
}
sourceCompatibility = '17'
""")
    _w(root, "settings.gradle", "include 'billing'\ninclude ':ledger'\n")
    _w(root, "gradle/libs.versions.toml", """
[versions]
spring-boot = "3.2.0"
[libraries]
starter = { module = "org.springframework.boot:spring-boot-starter", version.ref = "spring-boot" }
""")
    _w(root, ".gitignore", "/generated/\n*.log\n")
    _w(root, "Dockerfile", "FROM eclipse-temurin:21-jre\nCOPY app.jar /app.jar\n")
    _w(root, "docker-compose.yml", "services:\n  db:\n    image: postgres:16\n")
    _w(root, "ops/k8s/deployment.yaml",
       "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: billing\n")

    # --- billing service ----------------------------------------------------
    _w(root, f"{BILLING}/BillingController.java",
       _controller("com.acme.billing", "BillingController", "billing"))
    _w(root, DUP_BILLING, _entity("com.acme.billing", "Invoice", "billing_invoice"))
    _w(root, f"{BILLING}/InvoiceRepository.java", """package com.acme.billing;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface InvoiceRepository extends JpaRepository<Invoice, Long> {
    @Query("SELECT i FROM Invoice i WHERE i.status = :status")
    java.util.List<Invoice> byStatus(String status);

    @Query(value = "SELECT * FROM billing_invoice_audit WHERE ts > ?1", nativeQuery = true)
    java.util.List<Object[]> auditSince(String ts);
}
""")

    # Two sibling @Entity classes in ONE file. README.md's stated fix is that
    # each resolves to its own @Table rather than the first @Table in the file
    # being paired with the first class in it. No other fixture in this repo
    # has two entity classes in one file, so that claim was untested.
    _w(root, TWO_ENTITIES, """package com.acme.billing;

import jakarta.persistence.*;

@Entity
@Table(name = "alpha_tbl")
public class Alpha {
    @Id
    private Long id;
}

@Entity
@Table(name = "beta_tbl")
class Beta {
    @Id
    private Long id;
}
""")

    # The sharper form of the same regression: the second entity has no @Table
    # at all, so it must fall back to inferred default naming rather than
    # scavenging the first class's explicit table name.
    _w(root, MIXED_ENTITIES, """package com.acme.billing;

import jakarta.persistence.*;

@Entity
@Table(name = "gamma_explicit")
public class Gamma {
    @Id
    private Long id;
}

@Entity
class Delta {
    @Id
    private Long id;
}
""")

    # Exploratory: the persistence rule uses stopBy: end, so an outer class
    # wrapping a nested @Entity may also match. Characterized by the test
    # rather than assumed.
    _w(root, NESTED_ENTITY, """package com.acme.billing;

import jakarta.persistence.*;

public class NestedEntityHolder {
    @Entity
    @Table(name = "nested_inner")
    public static class InnerEntity {
        @Id
        private Long id;
    }
}
""")

    # Skew: many tiny services in one module and almost none in another, so
    # partitioning has a genuinely lopsided distribution to cope with.
    for i in range(40):
        _w(root, f"{BILLING}/Filler{i:02d}.java",
           _service("com.acme.billing", f"Filler{i:02d}"))

    _w(root, "services/billing-service/src/test/java/com/acme/billing/BillingControllerTest.java",
       "package com.acme.billing;\n\nimport org.junit.jupiter.api.Test;\n\n"
       "class BillingControllerTest {\n    @Test void works() { }\n}\n")
