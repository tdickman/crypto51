from crypto51.libs.mtc import MTC


def test_get_gh_hash_rate():
    mtc = MTC()
    assert mtc.get_gh_hash_rate('80.11 GH/s') == 80.11
    assert mtc.get_gh_hash_rate('87,222.223 TH/s') == 87222223.0
    assert mtc.get_gh_hash_rate('87.23 MH/s') == 0.08723
