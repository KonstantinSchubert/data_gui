import dataframe_managers


def test_dataframe_manager

    dfm = dataframe_managers.DataFrameManagerROOT("../test.root")

    for col in  dfm.get_all_columns():
        print col

    a = dfm.get_DataFrame(["L0Global","B_s0_M12"])

    assert(len(a.columns) == 2)
    assert("L0Global" in a.columns)
    assert("B_s0_M12" in a.columns)


    a = dfm.get_DataFrame(["nCandidate","B_s0_M12"])

    assert("nCandidate" in a.columns)
    assert("B_s0_M12" in a.columns)

    a = dfm.get_DataFrame(["mu4_TRACK_Likelihood"])