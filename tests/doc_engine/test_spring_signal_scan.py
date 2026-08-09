"""Spring signal scan suites (split by concern).

See `test_spring_signal_scan_core.py`, `test_spring_signal_scan_sql_lineage.py`,
`test_spring_signal_scan_jpql_lineage.py`, and
`test_spring_signal_scan_build_astgrep.py`.
"""

import pytest

pytestmark = pytest.mark.domain_stage0

